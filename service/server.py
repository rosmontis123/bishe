#!/usr/bin/python
# author bluenor
# -*- coding: utf-8 -*-
import datetime
import os
import pickle
import threading
from distutils.command.check import check
from functools import partial
from math import ceil
from os import makedirs, path, remove
import json

import mne
from PyQt5.QtCore import QProcess, QEventLoop, QTimer
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QApplication

from service.socketServer import socketServer


class server(socketServer):
    def __init__(self, s_ip, s_port, dbUtilH, appUtilH, curUserH):
        super().__init__(s_ip, s_port)
        self.tabV_model = QStandardItemModel(0, 5)
        self.dbUtil = dbUtilH
        self.appUtil = appUtilH
        self.curUser = curUserH
        self.model_path = appUtilH.model_path
        self.training_mutex = threading.Lock()
        self.testing_mutex = threading.Lock()
        self.diag_mutex = threading.Lock()
        self.filename_mutex = threading.Lock()
        self.permission_mutex = threading.Lock()
    def appMain(self, clientAddr, REQmsg):
        userID = REQmsg[2]
        macAddr = REQmsg[3][0]
        REQmsg[3] = REQmsg[3][1:]
        if userID == 0:
            # 登录
            userAccount = REQmsg[3][0]
            pwd = REQmsg[3][1]
            tipmsg, ret = self.login(userAccount, pwd, macAddr)
            REQmsg[3] = ret
            self.myTip(REQmsg[1], tipmsg)
            print(f'REQmsg: {REQmsg}')
            return REQmsg
        else:
            cmd = REQmsg[0]
            cmdID = REQmsg[1]
            self.permission_mutex.acquire()
            pret=self.curUser.permission(userID, macAddr, cmd)
            self.permission_mutex.release()
            if not pret:
                REQmsg[3] = ['0', REQmsg[1], f'权限不足']
                tipmsg = [REQmsg[2], f"应答{REQmsg[0]} ", f'权限不足', '']
                self.myTip(REQmsg[1], tipmsg)
                return REQmsg

            if cmd == "quit" and cmdID == 1:
                # 系统退出时注销用户
                tipmsg, ret = self.logout(REQmsg, macAddr)
                REQmsg[3] = ret
            elif cmd == "logout" and cmdID == 1:
                # 切换用户时注销用户
                tipmsg, ret = self.logout(REQmsg, macAddr)
                REQmsg[3] = ret
            # 修改密码
            elif cmd == "pwd" and cmdID == 1:
                tipmsg, ret = self.changePwd(REQmsg)
                REQmsg[3] = ret

            # 获取用户信息
            elif cmd == 'userManager' and cmdID == 1:
                tipmsg, ret = self.getUserInfo(macAddr, REQmsg)
                REQmsg[3] = ret
            # 新增用户信息
            elif cmd == 'userManager' and cmdID == 2:
                tipmsg, ret = self.addUserInfo(macAddr, REQmsg)
                REQmsg[3] = ret
            # 删除用户信息
            elif cmd == 'userManager' and cmdID == 3:
                tipmsg, ret = self.delUserInfo(macAddr, REQmsg)
                REQmsg[3] = ret
            # 编辑用户信息
            elif cmd == 'userManager' and cmdID == 4:
                tipmsg, ret = self.updateUserInfo(macAddr, REQmsg)
                REQmsg[3] = ret
            elif cmd == 'userManager' and cmdID == 5:
                tipmsg, ret = self.userPaging(macAddr, REQmsg)
                REQmsg[3] = ret
            elif cmd == 'userManager' and cmdID == 6:
                tipmsg, ret = self.inquiryUserInfo(macAddr, REQmsg)
                REQmsg[3] = ret


            # 获取导联配置信息
            elif cmd == 'montage' and cmdID == 1:
                tipmsg, ret = self.getMontage(macAddr, REQmsg)
                REQmsg[3] = ret
            # 添加导联方案
            elif cmd == 'montage' and cmdID == 2:
                tipmsg, ret = self.addMontageScheme(macAddr, REQmsg)
                REQmsg[3] = ret
            # 编辑导联方案
            elif cmd == 'montage' and cmdID == 3:
                tipmsg, ret = self.editMontageScheme(macAddr, REQmsg)
                REQmsg[3] = ret
            # 编辑导联方案
            elif cmd == 'montage' and cmdID == 4:
                tipmsg, ret = self.delMontageScheme(macAddr, REQmsg)
                REQmsg[3] = ret
            # 保存导联方案通道
            elif cmd == 'montage' and cmdID == 5:
                tipmsg, ret = self.saveMontageChannel(macAddr, REQmsg)
                REQmsg[3] = ret


            # 标注类型
            # 获取标注类型信息
            elif cmd == 'labelType' and cmdID == 1:
                tipmsg, ret = self.getTypeInfo(REQmsg)
                REQmsg[3] = ret

            # 增加标注类型信息
            elif cmd == 'labelType' and cmdID == 2:
                tipmsg, ret = self.addTypeInfo(REQmsg)
                REQmsg[3] = ret

            # 删除标注类型信息
            elif cmd == 'labelType' and cmdID == 3:
                tipmsg, ret = self.delTypeInfo(REQmsg)
                REQmsg[3] = ret

            # 更新标注类型信息
            elif cmd == 'labelType' and cmdID == 4:
                tipmsg, ret = self.updateTypeInfo(REQmsg)
                REQmsg[3] = ret

            # 获取基本配置数据
            elif cmd == 'basicConfig' and cmdID == 1:
                tipmsg, ret = self.getConfigData(cmdID)
                REQmsg[3] = ret
            elif cmd == 'basicConfig' and cmdID == 2:
                tipmsg, ret = self.addBasicConfig(cmdID, REQmsg[3])
                REQmsg[3] = ret
            elif cmd == 'basicConfig' and cmdID == 3:
                tipmsg, ret = self.delBasicConfig(cmdID, REQmsg[3][0])
                REQmsg[3] = ret
            elif cmd == 'basicConfig' and cmdID == 4:
                tipmsg, ret = self.updateBasicConfig(cmdID, REQmsg[3])
                REQmsg[3] = ret

            elif cmd == 'configOptions' and cmdID == 1:
                tipmsg, ret = self.getCurConfigData(cmdID, userID)
                REQmsg[3] = ret
            elif cmd == 'configOptions' and cmdID == 2:
                tipmsg, ret = self.getAllConfigData(cmdID, REQmsg[3])
                REQmsg[3] = ret
            elif cmd == 'configOptions' and cmdID == 3:
                tipmsg, ret = self.chgCurUserConfigData(cmdID, userID, REQmsg[3])
                REQmsg[3] = ret


            # 诊断查询/提取诊断信息
            elif cmd == 'manualQuery' and cmdID == 1:
                tipmsg, ret = self.mq_get_diags_Diagnosed(clientAddr, REQmsg)
                REQmsg[3] = ret
            # 诊断查询/类型、用户信息
            elif cmd == 'manualQuery' and cmdID == 4:
                tipmsg, ret = self.get_type_info(clientAddr, REQmsg)
                REQmsg[3] = ret
            # 诊断查询/类 /脑电文件
            # 诊断查询/设置
            elif cmd == 'manualQuery' and cmdID == 16:
                tipmsg, ret = self.init_SampleList(clientAddr, REQmsg)
                REQmsg[3] = ret
            # 诊断查询/提取诊断信息
            elif cmd == 'manualQuery' and cmdID == 25:
                tipmsg, ret = self.diag_get(clientAddr, REQmsg)
                REQmsg[3] = ret
            # 诊断查询/查询、分页
            elif cmd == 'manualQuery' and cmdID == 30:
                tipmsg, ret = self.mq_paging(clientAddr, REQmsg)
                REQmsg[3] = ret


            else:
                REQmsg[3] = ['0', REQmsg[1], f'未定义命令{REQmsg[1]}']
                tipmsg = [REQmsg[2], f"应答{REQmsg[0]} ", f'未定义命令{REQmsg[1]}', '']
        self.myTip(REQmsg[1], tipmsg)
        return REQmsg




    def login(self, userAccount, pwd, macAddr):
        case, msg, userInfo = self.curUser.login(userAccount, pwd, macAddr)
        ret = [case, msg, userInfo]
        print(f'RET: {ret}')
        msgtip = ['1', msg, userAccount, '']
        return msgtip, ret

    def logout(self, REQmsg, macAddr):
        userID = REQmsg[2]
        account = REQmsg[3][0]
        result = self.curUser.logout(userID, macAddr)
        if result:
            msg = result[2]
            if result[0] == 1:
                msgtip = [account, msg, '', '']
                ret = ['1', REQmsg[1], msg, '']
            else:
                msgtip = [account, msg, '', '']
                ret = ['0', REQmsg[1], msg, '']
        else:
            msgtip = [account, f"获取当前用户信息错误，退出失败！！！", '', '']
            ret = ['0', REQmsg[1], f"获取当前用户信息错误，退出失败！！！", '']
        return msgtip, ret

    # 修改密码
    def changePwd(self, REQmsg):
        try:
            uid = REQmsg[3][0]
            account = REQmsg[3][1]
            oldPwd = REQmsg[3][2]
            newPwd = REQmsg[3][3]
            cmdID = REQmsg[1]
            user_info = self.dbUtil.getUserInfo('uid', uid)
            if user_info:
                if oldPwd != user_info[0][2]:
                    msgtip = [account, f"原密码错误", '', '']
                    ret = ['0', cmdID, f"原密码错误", False]
                else:
                    user_msg = [uid, newPwd]
                    result = self.dbUtil.update_userInfo(user_msg, flag='1')
                    if result:
                        msgtip = [account, f"修改密码成功", '', '']
                        ret = ['1', cmdID, f"修改密码成功", True]
                    else:
                        msgtip = [account, f"修改密码失败", '', '']
                        ret = ['1', cmdID, f"修改密码失败", True]
            return msgtip, ret
        except Exception as e:
            print("changePwd", e)
            account = REQmsg[3][1]
            cmdID = REQmsg[1]
            msgtip = [account, f"修改密码失败:{e}", '', '']
            ret = ['1', cmdID, f"修改密码失败:{e}", True]
            return msgtip, ret

    # 用户管理模块
    # 根据传入参数获取数据库用户信息
    def getUserInfo(self, macAddr, REQmsg):
        try:
            _curPageIndex = REQmsg[3][0]
            if _curPageIndex <= 0:
                _curPageIndex = 1
            _Pagerows = REQmsg[3][1]
            if _Pagerows <= 0:
                _Pagerows = 12
            reset = REQmsg[3][2]
            ui_size = self.dbUtil.getUserInfoLen()
            ptotal = ceil(ui_size[0][0] / _Pagerows)
            if _curPageIndex > ptotal:
                _curPageIndex = ptotal
            if _curPageIndex == 1:
                result = self.dbUtil.getUserInfoByPage(offset=(_curPageIndex - 1) * _Pagerows, psize=_Pagerows + 1)
            else:
                result = self.dbUtil.getUserInfoByPage(offset=((_curPageIndex - 1) * _Pagerows + 1), psize=_Pagerows)
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '数据库操作成功', "", '']
            ret = ['1', REQmsg[1], result, ptotal, reset]
            return msgtip, ret
        except Exception as e:
            print('getUserInfo', e)
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '数据库操作不成功', "", '']
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}数据库操作不成功"]
            return msgtip, ret

    # 根据传入参数添加数据库用户信息
    def addUserInfo(self, macAddr, REQmsg):
        # print('addUserInfo')
        try:
            user_info = REQmsg[3]
            r, result = self.dbUtil.addUserInfo(user_info)
            isSearch = REQmsg[3][12]
            if r == '1':
                _curPageIndex = REQmsg[3][11]
                if _curPageIndex <= 0:
                    _curPageIndex = 1
                _Pagerows = 12
                if isSearch:
                    key_word = REQmsg[3][13]
                    key_value = REQmsg[3][14]
                    result = self.dbUtil.getSearchUserInfoByPage(where_name=key_word, where_value=key_value,
                                                                 offset=(_curPageIndex - 1) * _Pagerows,
                                                                 psize=_Pagerows)
                    ui_size = self.dbUtil.getUserInfoLen(where_name=key_word, where_like=key_value)
                    ptotal = ceil(ui_size[0][0] / _Pagerows)
                else:
                    ui_size = self.dbUtil.getUserInfoLen()
                    ptotal = ceil(ui_size[0][0] / _Pagerows)
                    if _curPageIndex > ptotal:
                        _curPageIndex = ptotal
                    if _curPageIndex == 1:
                        result = self.dbUtil.getUserInfoByPage(offset=(_curPageIndex - 1) * _Pagerows,
                                                               psize=_Pagerows + 1)
                    else:
                        result = self.dbUtil.getUserInfoByPage(offset=((_curPageIndex - 1) * _Pagerows + 1),
                                                               psize=_Pagerows)
                msgtip = [REQmsg[1], f"添加用户信息成功", f'{REQmsg[2]}', '']
                ret = ['1', REQmsg[1], result, ptotal, isSearch]
                return msgtip, ret
            else:
                msgtip = [REQmsg[1], f"添加用户信息失败", f'{result}', '']
                ret = ['0', REQmsg[1], user_info]
                return msgtip, ret
        except Exception as e:
            print('addUserInfo', e)
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '数据库操作不成功', "", '']
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}数据库操作不成功"]
            return msgtip, ret

    # 根据传入参数删除用户信息
    def delUserInfo(self, macAddr, REQmsg):
        # print('delUserInfo')
        try:
            msgtip, ret = self.curUser.delUserInfo(REQmsg)
            return msgtip, ret
        except Exception as e:
            print('delUserInfo', e)
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '数据库操作不成功', "", '']
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}数据库操作不成功"]
            return msgtip, ret

    # 根据传入参数编辑用户信息
    def updateUserInfo(self, macAddr, REQmsg):
        # print('updateUserInfo')
        try:
            msgtip, ret = self.curUser.updateUserInfo(REQmsg)
            return msgtip, ret
        except Exception as e:
            print('updateUserInfo', e)
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '数据库操作不成功', "", '']
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}数据库操作不成功"]
            return msgtip, ret

    def userPaging(self, macAddr, REQmsg):
        try:
            isSearch = REQmsg[3][3]
            _curPageIndex = REQmsg[3][0]
            if _curPageIndex <= 0:
                _curPageIndex = 1
            _Pagerows = REQmsg[3][1]
            if _Pagerows <= 0:
                _Pagerows = 12
            if isSearch:
                key_word = REQmsg[3][4]
                key_value = REQmsg[3][5]
                result = self.dbUtil.getSearchUserInfoByPage(where_name=key_word, where_value=key_value,
                                                             offset=(_curPageIndex - 1) * _Pagerows, psize=_Pagerows)
            else:
                if _curPageIndex == 1:
                    result = self.dbUtil.getUserInfoByPage(offset=(_curPageIndex - 1) * _Pagerows, psize=_Pagerows + 1)
                else:
                    result = self.dbUtil.getUserInfoByPage(offset=((_curPageIndex - 1) * _Pagerows + 1),
                                                           psize=_Pagerows)
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '数据库操作成功', "", '']
            ret = ['1', REQmsg[1], result, isSearch]
            return msgtip, ret
        except Exception as e:
            print('userPaging', e)
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '数据库操作不成功', "", '']
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}数据库操作不成功"]
            return msgtip, ret

    def inquiryUserInfo(self, macAddr, REQmsg):
        try:
            key_word = REQmsg[3][0]
            key_value = REQmsg[3][1]
            _curPageIndex = REQmsg[3][2]
            if _curPageIndex <= 0:
                _curPageIndex = 1
            _Pagerows = REQmsg[3][3]
            if _Pagerows <= 0:
                _Pagerows = 12
            result = self.dbUtil.getSearchUserInfoByPage(where_name=key_word, where_value=key_value,
                                                         offset=(_curPageIndex - 1) * _Pagerows, psize=_Pagerows)
            ui_size = self.dbUtil.getUserInfoLen(where_name=key_word, where_like=key_value)
            ptotal = ceil(ui_size[0][0] / _Pagerows)
            msgtip = [REQmsg[2], f"应答{REQmsg[2]}", '数据库操作成功', "", '']
            ret = ['1', REQmsg[1], result, ptotal]
            return msgtip, ret
        except Exception as e:
            print('inquiryUserInfo', e)
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '数据库操作不成功', "", '']
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}数据库操作不成功"]
            return msgtip, ret

    # 导联配置模块
    # 根据传入参数获取导联配置信息
    def getMontage(self, macAddr, REQmsg):
        try:
            r, montageData = self.appUtil.getMontage()
            if r == '0':
                msgtip = [REQmsg[1], f"获取导联配置信息失败", f'{REQmsg[2]}', '']
                ret = ['0', REQmsg[1], montageData]
                return msgtip, ret
            elif r == '1':
                msgtip = [REQmsg[1], f"获取导联配置信息成功", f'{REQmsg[2]}', '']
                ret = ['1', REQmsg[1], montageData]
                return msgtip, ret
        except Exception as e:
            print('getMontage', e)
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '配置文件不成功', "", '']
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}配置文件不成功"]
            return msgtip, ret

    # 根据传入参数添加导联方案
    def addMontageScheme(self, macAddr, REQmsg):
        try:
            result = self.appUtil.addMontageScheme(REQmsg[3][0])
            if result[0] == '1':
                msgtip = [REQmsg[1], f"{result[1]}", f'{REQmsg[2]}', '']
                ret = ['1', REQmsg[1], REQmsg[3][0]]
                return msgtip, ret
            elif result[0] == '0':
                msgtip = [REQmsg[1], f"{result[1]}", f'{REQmsg[2]}', '']
                ret = ['0', REQmsg[1], REQmsg[3][0]]
                return msgtip, ret
        except Exception as e:
            print('addMontageScheme', e)
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '配置文件不成功', "", '']
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}配置文件不成功"]
            return msgtip, ret

    # 根据传入参数编辑导联方案
    def editMontageScheme(self, macAddr, REQmsg):
        try:
            result = self.appUtil.editMontageScheme(where_name=REQmsg[3][0], set_name=REQmsg[3][1])
            if result[0] == '1':
                msgtip = [REQmsg[1], f"{result[1]}", f'{REQmsg[2]}', '']
                ret = ['1', REQmsg[1], REQmsg[3]]
                return msgtip, ret
            elif result[0] == '0':
                msgtip = [REQmsg[1], f"{result[1]}", f'{REQmsg[2]}', '']
                ret = ['0', REQmsg[1], REQmsg[3]]
                return msgtip, ret
        except Exception as e:
            print('editMontageScheme', e)
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '配置文件不成功', "", '']
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}配置文件不成功"]
            return msgtip, ret

    # 根据传入参数删除导联方案
    def delMontageScheme(self, macAddr, REQmsg):
        try:
            result = self.appUtil.delMontageScheme(REQmsg[3][0])
            if result[0] == '1':
                msgtip = [REQmsg[1], f"{result[1]}", f'{REQmsg[2]}', '']
                ret = ['1', REQmsg[1], REQmsg[3]]
                return msgtip, ret
            elif result[0] == '0':
                msgtip = [REQmsg[1], f"{result[1]}", f'{REQmsg[2]}', '']
                ret = ['0', REQmsg[1], REQmsg[3]]
                return msgtip, ret
        except Exception as e:
            print('delMontageScheme', e)
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '配置文件不成功', "", '']
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}配置文件不成功"]
            return msgtip, ret

    # 根据传入参数保存导联方案通道
    def saveMontageChannel(self, macAddr, REQmsg):
        try:
            result = self.appUtil.saveMontageChannel(REQmsg[3][0], REQmsg[3][1])
            if result[0] == '1':
                msgtip = [REQmsg[1], f"{result[1]}", f'{REQmsg[2]}', '']
                ret = ['1', REQmsg[1], REQmsg[3]]
                return msgtip, ret
            elif result[0] == '0':
                msgtip = [REQmsg[1], f"{result[1]}", f'{REQmsg[2]}', '']
                ret = ['0', REQmsg[1], REQmsg[3]]
                return msgtip, ret
        except Exception as e:
            print('saveMontageChannel', e)
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '配置文件不成功', "", '']
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}配置文件不成功"]
            return msgtip, ret

    # 标注类型模块
    # 根据传入参数获取数据库标注类型
    def getTypeInfo(self, REQmsg):
        try:
            print('getTypeInfo')
            account = REQmsg[3][0]
            name = REQmsg[3][1]
            value = REQmsg[3][2]
            type_info = self.dbUtil.get_typeInfo(name, value)
            if type_info:
                msgtip = [account, f"查询标注类型信息成功", '', '']
                ret = ['1', REQmsg[1], f"查询标注类型信息成功", type_info]
                return msgtip, ret
            else:
                msgtip = [account, f"查询标注类型信息失败", '', '']
                ret = ['0', REQmsg[1], f"查询标注类型信息失败", type_info]
                return msgtip, ret
        except Exception as e:
            print('getTypeInfo', e)
            account = REQmsg[3][0]
            msgtip = [account, f"查询标注类型信息失败:{e}", '', '']
            ret = ['0', REQmsg[1], f"查询标注类型信息失败:{e}", '']
            return msgtip, ret

    # 根据传入参数增加数据库标注类型
    def addTypeInfo(self, REQmsg):
        try:
            account = REQmsg[3][0]
            type_info = REQmsg[3][1:]
            result = self.dbUtil.add_typeInfo(type_info)
            if result:
                msgtip = [account, f"添加标注类型信息成功", '', '']
                ret = ['1', REQmsg[1], f"添加标注类型信息成功", type_info]
                # REQmsg[3] = ret
                return msgtip, ret
            else:
                msgtip = [account, f"添加标注类型信息失败", '', '']
                ret = ['0', REQmsg[1], f"添加标注类型信息失败", type_info]
                return msgtip, ret
        except Exception as e:
            print('addTypeInfo', e)
            account = REQmsg[3][0]
            msgtip = [account, f"添加标注类型信息失败:{e}", '', '']
            ret = ['0', REQmsg[1], f"添加标注类型信息失败:{e}", '']
            return msgtip, ret

    # 根据传入参数删除数据库标注类型
    def delTypeInfo(self, REQmsg):
        try:
            account = REQmsg[3][0]
            type_info = REQmsg[3][1:]
            type_id = type_info[0]
            result = self.dbUtil.del_typeInfo('type_id', type_id)
            if result:
                msgtip = [account, f"删除标注类型信息成功", '', '']
                ret = ['1', REQmsg[1], f"删除标注类型信息成功", type_info]
                return msgtip, ret
            else:
                msgtip = [account, f"删除标注类型信息失败", '', '']
                ret = ['0', REQmsg[1], f"删除标注类型信息失败", type_info]
                return msgtip, ret
        except Exception as e:
            print('delTypeInfo', e)
            account = REQmsg[3][0]
            msgtip = [account, f"删除标注类型信息失败:{e}", '', '']
            ret = ['0', REQmsg[1], f"删除标注类型信息失败:{e}", '']
            return msgtip, ret

    # 根据传入参数更新数据库标注类型
    def updateTypeInfo(self, REQmsg):
        try:
            account = REQmsg[3][0]
            type_info = REQmsg[3][1:]
            value = REQmsg[3][1]
            type_id = REQmsg[3][2]
            result = self.dbUtil.update_typeInfo(value, 'type_id', type_id)
            if result:
                msgtip = [account, f"修改标注类型信息成功", '', '']
                ret = ['1', REQmsg[1], f"修改标注类型信息成功", type_info]
                return msgtip, ret
            else:
                msgtip = [account, f"修改标注类型信息失败", '', '']
                ret = ['0', REQmsg[1], f"修改标注类型信息失败", type_info]
                return msgtip, ret
        except Exception as e:
            print('updateTypeInfo', e)
            account = REQmsg[3][0]
            msgtip = [account, f"修改标注类型信息失败:{e}", '', '']
            ret = ['0', REQmsg[1], f"修改标注类型信息失败:{e}", '']
            return msgtip, ret







    def getConfigData(self, cmdID):
        configInfo = self.dbUtil.queryConfigData()
        msgtip = [cmdID, f"获取全部基本配置信息", '', '']
        print(configInfo)
        ret = ['1', cmdID, f"获取全部基本配置信息", configInfo]
        return msgtip, ret

    def addBasicConfig(self, cmdID, config):
        print(f'addBasicConfig: {config}')
        self.dbUtil.addBasicConfig(config)
        if config[5] == 1:
            for i, c in enumerate(self.curUser.config):
                print(f'c: {c}')
                if c[6] == 1:
                    self.dbUtil.updateBasicConfig('config_id', c[0], set_name='`default`', set_value=0)
        self.curUser.config = self.dbUtil.queryConfigData()
        msgtip = [cmdID, f"添加新的基本配置信息", '', '']
        ret = ['1', cmdID, f"添加新的基本配置信息", self.curUser.config[len(self.curUser.config) - 1]]
        return msgtip, ret

    def delBasicConfig(self, cmdID, config):
        print(f'delBasicConfig: {config}')
        if config[6] == 1:
            msgtip = [cmdID, f"admin正在删除默认配置，返回错误信息", '', '']
            ret = ['0', cmdID, f"admin正在删除默认配置，返回错误信息", '当前正在尝试删除默认配置，请先设置其他默认配置!']
            return msgtip, ret
        if not self.dbUtil.delBasicConfig('config_id', config[0]):
            msgtip = [cmdID, f"删除配置失败", '', '']
            ret = ['0', cmdID, f"删除配置失败", '删除配置失败，当前配置正在被用户使用']
            return msgtip, ret
        for i, c in enumerate(self.curUser.config):
            print(f'c: {c}')
            if c[0] == config[0]:
                self.curUser.config.remove(c)
        print(f'config: {self.curUser.config}')
        msgtip = [cmdID, f"删除新的基本配置信息", '', '']
        ret = ['1', cmdID, f"删除新的基本配置信息", config[0]]
        return msgtip, ret

    def updateBasicConfig(self, cmdID, config):
        print(f'updateBasicConfig: {config}')
        for i, c in enumerate(self.curUser.config):
            print(f'c: {c}')
            if c[0] == config[0]:
                if str(c[1]) != config[1] or str(c[2]) != config[2] or str(c[3]) != config[3] or str(c[4]) != config[
                    4] or str(c[5]) != config[5]:
                    if self.dbUtil.checkConfigisUsed(c[0]):
                        msgtip = [cmdID, f"修改配置失败", '', '']
                        ret = ['0', cmdID, f"修改配置失败", '修改配置失败，当前配置正在被用户使用']
                        return msgtip, ret
        if config[6] == 1:
            config_t = self.dbUtil.queryConfigData('default', 1)[0]
            if config_t != None or len(config_t) != 0:
                self.dbUtil.updateBasicConfig('config_id', config_t[0], set_name='`default`', set_value=0)
            else:
                msgtip = [cmdID, f"取消默认配置失败，请设置其他配置为默认配置", '', '']
                ret = ['0', cmdID, f"取消默认配置失败，请设置其他配置为默认配置",
                       '取消默认配置失败，请设置其他配置为默认配置']
                return msgtip, ret
        self.dbUtil.updateBasicConfig('config_id', config[0], config)
        self.curUser.config = self.dbUtil.queryConfigData()
        msgtip = [cmdID, f"修改新的基本配置信息", '', '']
        ret = ['1', cmdID, f"修改新的基本配置信息", self.curUser.config]
        return msgtip, ret




    ### dsj ==[===

    # 执行查看/提交主题(可用，不可用)
    def rgQ_theme_commit(self, clientAddr, REQmsg):
        if REQmsg[1] == 31:
            theme_id = REQmsg[3][0]
            stat = REQmsg[3][1]
            r0, d0 = self.dbUtil.task_get(theme_id=theme_id,
                                          other_sql="(state ='notStarted' or state= 'labelling' or state= 'labelled')")
            if r0 == '0':
                ret = [r0, REQmsg[1], f'统计当前主题的任务记录不成功:{d0}']
                msgtip = [REQmsg[2], f"应答:{REQmsg[0]}/统计当前主题的任务记录不成功:{d0}", '数据库操作', "不成功",""]
            elif len(d0)>0:
                ret = ['0', REQmsg[1], f'{REQmsg[0]}/主题不能设置{stat}，有任务{len(d0)}条未处理.']
                msgtip = [REQmsg[2], f"应答:{REQmsg[0]}/主题不能设置{stat}", '数据库操作', "有任务{len(d0)}条未处理.", ""]
            else:
                usql=f"update  theme set state='{stat}' where theme_id={theme_id}"
                r=self.dbUtil.myExecuteSql(usql)
                if r=="":
                    ret = ['1', REQmsg[1], f'{REQmsg[0]}/主题设置{stat}，操作成功。']
                    msgtip = [REQmsg[2], f"应答:{REQmsg[0]}/主题设置{stat}", '数据库操作', "成功", ""]
                else:
                    ret = ['0', REQmsg[1], f'{REQmsg[0]}/主题设置{stat}，数据库操作不成功{r}']
                    msgtip = [REQmsg[2], f"应答:{REQmsg[0]}/主题设置{stat}", '数据库操作', "不成功", ""]
        else:
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}未定义命令"]
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '未定义命令', '']
        return msgtip, ret


    #执行查看/查询、分页
    def rgQ_paging(self, clientAddr, REQmsg):
        if REQmsg[1] == 30:
            _uid = REQmsg[3][0]
            _curPageIndex = REQmsg[3][1]
            _Pagerows = REQmsg[3][2]
            if _Pagerows <= 0:
                _Pagerows = 12
            paging = REQmsg[3][3]

            theme_name = REQmsg[3][4]
            theme_state = REQmsg[3][5]
            task_state = REQmsg[3][6]
            sql_where = f" theme.uid={_uid}   and theme.state in ('evaluating','labelling')  " \
                        f"and  task.state in ('labelled','qualified','notqualified') "
            if theme_name is not None and theme_name != '':
                sql_where += f" and  theme.name like '%{theme_name}%' "
            if theme_state is not None and theme_state != '':
                sql_where += f" and  theme.state = '{theme_state}' "
            else:
                sql_where += f""
            if task_state is not None and task_state != '':
                sql_where += f" and  task.state = '{task_state}' "

            r, d = self.dbUtil.rg_get_labels(where_task=sql_where)

            if r == '0':
                ret = [r, d]
                msgtip = [REQmsg[2], f"应答:执行查看/[分页查询]提取标注信息", '数据库操作', "不成功", ""]
            else:
                rn = len(d)
                ptotal = ceil(rn / _Pagerows)
                if _curPageIndex > ptotal:
                    _curPageIndex = ptotal
                if _curPageIndex <= 0:
                    _curPageIndex = 1
                pids = ""
                uids = ""
                themeids = ""
                retData = []
                b = (_curPageIndex - 1) * _Pagerows
                for i in range(b, min(b + _Pagerows, rn)):
                    retData.append(d[i])
                    if pids == '':
                        pids += str(d[i][9])
                        uids += str(d[i][12])
                        themeids += str(d[i][0])
                    else:
                        pids += "," + str(d[i][9])
                        uids += "," + str(d[i][12])
                        themeids += "," + str(d[i][0])

                pr, pd = self.dbUtil.get_patientNameByPids(pids)
                if pr == '0':
                    pd = None
                ur, ud = self.dbUtil.get_userNameByUids(uids)
                if ur == '0':
                    ud = None
                sql = f" SELECT theme_id, count(*) FROM task where theme_id in  ({themeids}) and state in ('notStarted', 'labelling', 'labelled') " \
                      "group by theme_id"
                thr, thd = self.dbUtil.myQueryExt(sql)
                if thr == '0':
                    thd = None
                ret = [r, REQmsg[1], retData, pd, _curPageIndex, ptotal, rn, paging,ud,thd]
                msgtip = [REQmsg[2], f"应答:执行查看/[分页查询]标注信息", '数据库操作', "成功", ""]
        else:
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}未定义命令"]
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '未定义命令', '']
        return msgtip, ret

        # 执行查看/提交标注信息(合格，不合格)

    def rgQ_label_commit(self, clientAddr, REQmsg):
        if REQmsg[1] == 28:
            theme_id = REQmsg[3][0]
            check_id = REQmsg[3][1]
            file_id = REQmsg[3][2]
            uid = REQmsg[3][3]
            stat = REQmsg[3][4]
            # 'qualified', 'notqualified'
            sql1 = f" UPDATE theme SET state = 'evaluating' WHERE theme_id = {theme_id} "
            sql2 = f" UPDATE task SET state = '{stat}' WHERE theme_id = {theme_id} and check_id = {check_id} and " \
                   f"file_id ={file_id} and uid = {uid}"
            if stat == 'qualified':
                sqls = [sql2]
                r, d = self.dbUtil.myExecuteTranSql(sqls)
            elif stat == 'notqualified':
                # sql3 = f" delete from reslab where theme_id={theme_id} and check_id={check_id} and  file_id={file_id} and  uid={uid}"
                sqls = [sql2]
                r, d = self.dbUtil.myExecuteTranSql(sqls)
            else:
                r = '0'
                d = '状态只能是qualified或notqualified'
            if r == '1':
                ret = [r, REQmsg[1], f'{REQmsg[0]}/标注设置[{stat}],操作成功']
                msgtip = [REQmsg[2], f"应答:{REQmsg[0]}/标注设置[{stat}]", '数据库操作', "成功", ""]
            else:
                ret = [r, REQmsg[1], f'{REQmsg[0]}/标注设置[{stat}],操作不成功:{d}']
                msgtip = [REQmsg[2], f"应答:{REQmsg[0]}/标注设置[{stat}]", '数据库操作', f"不成功{d}", ""]
        else:
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}未定义命令"]
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '未定义命令', '']
        return msgtip, ret

    # 执行查看/提取未标注信息

    def rgQ_get_labels(self, clientAddr, REQmsg):
        if REQmsg[1] == 1:
            _uid = REQmsg[3][0]
            _curPageIndex = REQmsg[3][1]
            if _curPageIndex <= 0:
                _curPageIndex = 1
            _Pagerows = REQmsg[3][2]
            if _Pagerows <= 0:
                _Pagerows = 12
            # sql_where = f" task.uid={_uid} and (task.state='notStarted' or task.state='labelling') "
            #sql_where = f" theme.state in ('evaluating','notUsable','usable') and  theme.uid={_uid}  "
            sql_where = f" theme.state in ('evaluating','labelling') and  theme.uid={_uid} and " \
                        f" task.state in ('labelled','qualified','notqualified') "
            r, d = self.dbUtil.rg_get_labels(where_task=sql_where)
            if r == '0':
                ret = [r, d]
                msgtip = [REQmsg[2], "应答:执行查看/提取课堂内容信息", '数据库操作', "不成功", ""]
            else:
                rn = len(d)
                ptotal = ceil(rn / _Pagerows)
                if _curPageIndex > ptotal:
                    _curPageIndex = ptotal
                if _curPageIndex <= 0:
                    _curPageIndex = 1
                pids = ""
                uids = ""
                themeids = ""
                retData = []
                b = (_curPageIndex - 1) * _Pagerows
                for i in range(b, min(b + _Pagerows, rn)):
                    retData.append(d[i])
                    if pids == '':
                        pids += str(d[i][9])
                        uids += str(d[i][12])
                        themeids += str(d[i][0])
                    else:
                        pids += "," + str(d[i][9])
                        uids += "," + str(d[i][12])
                        themeids += "," + str(d[i][0])
                pr, pd = self.dbUtil.get_patientNameByPids(pids)
                if pr == '0':
                    pd = None
                ur, ud = self.dbUtil.get_userNameByUids(uids)
                if ur == '0':
                    ud = None
                sql=f" SELECT theme_id, count(*) FROM task where theme_id in  ({themeids}) and state in ('notStarted', 'labelling', 'labelled') " \
                     "group by theme_id"
                thr, thd = self.dbUtil.myQueryExt(sql)
                if thr == '0':
                    thd = None
                ret = [r, REQmsg[1], d, pd,ud,thd,_curPageIndex, ptotal, rn]
                msgtip = [REQmsg[2], "应答:执行查看/提取标注信息", '数据库操作', "成功",""]
        else:
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}未定义命令"]
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '未定义命令', '']
        return msgtip, ret

        # 诊断查询/提取诊断信息

    def mq_get_diags_Diagnosed(self, clientAddr, REQmsg):
        if REQmsg[1] == 1:
            _uid = REQmsg[3][0]
            _uid = ''
            _curPageIndex = REQmsg[3][1]
            if _curPageIndex <= 0:
                _curPageIndex = 1
            _Pagerows = REQmsg[3][2]
            if _Pagerows <= 0:
                _Pagerows = 12
            # r, rn = self.dbUtil.diag_getRecords(uid=_uid, diag_state='diagnosed')
            #r, d = self.dbUtil.diag_getRecords(diag_state='diagnosed')
            r, d = self.dbUtil.diag_getByPage(diag_state='diagnosed')
            if r == '0':
                ret = [r, f'统计记录数不成功{r}']
                msgtip = [REQmsg[2], f"应答:诊断查询/提取诊断信息", '统计记录数不成功', f"{r}", ""]
                return msgtip, ret
            rn = len(d)
            ptotal = ceil(rn / _Pagerows)
            if _curPageIndex > ptotal:
                _curPageIndex = ptotal
            if _curPageIndex <= 0:
                _curPageIndex = 1
            pids = ""
            uids = ""
            retData = []
            b = (_curPageIndex - 1) * _Pagerows
            for i in range(b, min(b + _Pagerows, rn)):
                retData.append(d[i])
                if pids == '':
                    pids += str(d[i][0])
                    uids += str(d[i][2])
                else:
                    pids += "," + str(d[i][0])
                    uids += "," + str(d[i][2])
            ur, ud = self.dbUtil.get_userNameByUids(uids)
            pr, pd = self.dbUtil.get_patientNameByPids(pids)
            if ur == '0':
                ud = None
            if pr == '0':
                pd = None
            ret = [r, REQmsg[1], retData, ud, pd, _curPageIndex, ptotal, rn]
            # rn = rn[0]
            # ptotal = ceil(rn / _Pagerows)
            # if _curPageIndex > ptotal:
            #     _curPageIndex = ptotal
            #
            # r, d = self.dbUtil.diag_getByPage(diag_state='diagnosed',
            #                                   offset=(_curPageIndex - 1) * _Pagerows,
            #                                   psize=_Pagerows)
            # if r == '0':
            #     ret = [r, d]
            #     msgtip = [REQmsg[2], f"应答:诊断查询/提取诊断信息", '数据库操作', "不成功", ""]
            # else:
            #     pids = ""
            #     uids = ""
            #     for dInfo in d:
            #         if pids == '':
            #             pids += str(dInfo[0])
            #             uids += str(dInfo[2])
            #         else:
            #             pids += "," + str(dInfo[0])
            #             uids += "," + str(dInfo[2])
            #     ur, ud = self.dbUtil.get_userNameByUids(uids)
            #     pr, pd = self.dbUtil.get_patientNameByPids(pids)
            #     if ur == '0':
            #         ud = None
            #     if pr == '0':
            #         pd = None
            #     ret = [r, REQmsg[1], d, ud, pd, _curPageIndex, ptotal, rn]
            msgtip = [REQmsg[2], f"应答:诊断查询/提取诊断信息", '数据库操作', "成功", ""]
        else:
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}未定义命令"]
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '未定义命令', '']
        return msgtip, ret

        # 标注诊断/拒绝诊断信息


    def diag_update(self, clientAddr, REQmsg):
        titleinfo = {'manual': '标注诊断', 'manualQuery': '诊断查询', 'consulting': '脑电会诊'}
        if REQmsg[1] == 27:
            r, d = self.dbUtil.diag_update(REQmsg[3])
            if r == '0':
                ret = [r, d]
                msgtip = [REQmsg[2], f"应答:ltip[REQmsg[0]]/修改诊断信息", '数据库操作', "不成功", ""]
            else:
                ret = [r, REQmsg[1], d]
                msgtip = [REQmsg[2], f"应答:ltip[REQmsg[0]]/修改诊断信息", '数据库操作', "成功", ""]
        else:
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}未定义命令"]
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '未定义命令', '']
        return msgtip, ret

        # 标注诊断/填写诊断信息


    # 标注诊断/提取诊断信息
    def diag_get(self, clientAddr, REQmsg):
        titleinfo = {'manual': '标注诊断', 'manualQuery': '诊断查询', 'consulting': '脑电会诊',
                     'diagTraining': '诊断学习'}
        if REQmsg[1] == 25 or REQmsg[0] == 'consulting' and REQmsg[1] == 3:
            r, d = self.dbUtil.diag_get(check_id=REQmsg[3][0], uid=REQmsg[3][1])
            if r == '0':
                ret = [r, d]
                msgtip = [REQmsg[2], f"应答:{titleinfo[REQmsg[0]]}/提取诊断信息", '数据库操作', "不成功", ""]
            else:
                ret = [r, REQmsg[1], d]
                msgtip = [REQmsg[2], f"应答:{titleinfo[REQmsg[0]]}/提取诊断信息", '数据库操作', "成功", ""]
        else:
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}未定义命令"]
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '未定义命令', '']
        return msgtip, ret

        # 诊断标注/提取未诊断信息
    def mq_paging(self, clientAddr, REQmsg):
        if REQmsg[1] == 30:
            _uid = REQmsg[3][0]
            _curPageIndex = REQmsg[3][1]

            _Pagerows = REQmsg[3][2]
            if _Pagerows <= 0:
                _Pagerows = 12
            paging = REQmsg[3][3]
            qname = REQmsg[3][4]
            qvalue = REQmsg[3][5]
            mdate1 = REQmsg[3][6]
            mdate2 = REQmsg[3][7]

            where_sql = ''
            pname = ''
            if qvalue is not None and qvalue != "":
                if qname == "检查单号":
                    where_sql = f" check_info.check_number like '%{qvalue}%' "
                elif qname == "病人姓名":
                    pname = qvalue
                elif qname == "测量日期":
                    where_sql = f" measure_date = '{qvalue}' "
                elif qname == "医生名称":
                    where_sql = f" diag.uid in (select uid FROM user_info where name like '%{qvalue}%') "
            if mdate1 is not None and mdate1 != "":
                if where_sql == '':
                    where_sql = f" sign_date >= '{mdate1} 00:00:00' "
                else:
                    where_sql += f" and sign_date >= '{mdate1} 00:00:00' "
            if mdate2 is not None and mdate2 != "":
                if where_sql == '':
                    where_sql = f" sign_date <= '{mdate2} 23:59.59' "
                else:
                    where_sql += f" and sign_date <= '{mdate2} 23:59.59' "
            r, d = self.dbUtil.diag_getByPage(pname=pname, diag_state='diagnosed', other_where=where_sql)
            if r == '0':
                ret = [r, d]
                msgtip = [REQmsg[2], f"应答:诊断查询/提取诊断信息", '数据库操作', "不成功", ""]
            else:
                rn = len(d)
                ptotal = ceil(rn / _Pagerows)
                if _curPageIndex > ptotal:
                    _curPageIndex = ptotal
                if _curPageIndex <= 0:
                    _curPageIndex = 1
                pids = ""
                uids = ""
                retData = []
                b = (_curPageIndex - 1) * _Pagerows
                for i in range(b, min(b + _Pagerows, rn)):
                    retData.append(d[i])
                    if pids == '':
                        pids += str(d[i][0])
                        uids += str(d[i][2])
                    else:
                        pids += "," + str(d[i][0])
                        uids += "," + str(d[i][2])
                ur, ud = self.dbUtil.get_userNameByUids(uids)
                pr, pd = self.dbUtil.get_patientNameByPids(pids)
                if ur == '0':
                    ud = None
                if pr == '0':
                    pd = None
                ret = [r, REQmsg[1], retData, ud, pd, _curPageIndex, ptotal, rn, paging]
                msgtip = [REQmsg[2], f"应答:诊断查询/分页查询诊断信息", '数据库操作', "成功", ""]
        else:
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}未定义命令"]
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '未定义命令', '']
        return msgtip, ret

    def diags_notDiag_get(self, clientAddr, REQmsg):
        titleinfo = {'manual': '标注诊断', 'manualQuery': '诊断查询', 'consulting': '脑电会诊'}
        refused_state=[]
        if REQmsg[1] == 24:
            if REQmsg[0] == 'manual':
                r, d = self.dbUtil.diag_get(check_id='', uid=REQmsg[3][0], diag_state='notDiagnosed',
                                            other_where="check_info.state='diagnosing'")
            else:
                r, d = self.dbUtil.diag_get_forConsulting(uid=REQmsg[3][0])
                tempt=[]
                #patientid,measure_date,diag.uid(诊断医生id),diag.state,diag.sign_date(诊断报告落款时间),[一系列报告内容],diag.check_id,check_info.puid,check_info.check_number,check_info.cUid
                for i in d:
                    tempt.append([i[15],i[2]])
                refused_state=self.dbUtil.diag_get_refused_state(tempt)
            if r == '0':
                ret = [r, d]
                msgtip = [REQmsg[2], f"应答:{titleinfo[REQmsg[0]]}/提取未诊断信息", '数据库操作', "不成功", ""]
            else:
                pids = ""
                uids = ""
                for dInfo in d:
                    if pids == '':
                        pids += str(dInfo[0])
                        uids += str(dInfo[2])
                    else:
                        pids += "," + str(dInfo[0])
                        uids += "," + str(dInfo[2])
                ur, ud = self.dbUtil.get_userNameByUids(uids)
                pr, pd = self.dbUtil.get_patientNameByPids(pids)
                if ur == '0':
                    ud = None
                if pr == '0':
                    pd = None
                ret = [r, REQmsg[1], d, ud, pd,refused_state]
                msgtip = [REQmsg[2], f"应答:{titleinfo[REQmsg[0]]}/提取未诊断信息", '数据库操作', "成功", ""]
        else:
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}未定义命令"]
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '未定义命令', '']
        return msgtip, ret

    # 标注诊断/删除样本状态信息



    # 标注诊断/提取样本信息？？？
    def init_SampleList(self, clientAddr, REQmsg):
        if REQmsg[1] == 16:
            check_id = REQmsg[3][0]
            file_id = REQmsg[3][1]
            channels = REQmsg[3][2]
            type_names = REQmsg[3][3]
            user_names = REQmsg[3][4]
            status_show = REQmsg[3][5]
            try:
                rn, retData = self.dbUtil.get_sampleListInfo(check_id, file_id, channels, type_names, user_names,
                                                             status_show)
                if rn == '0':
                    msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '数据库操作不成功', retData]
                    ret = ['0', REQmsg[1], f"应答{REQmsg[0]}数据库操作不成功:{retData}"]
                else:
                    msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '数据库操作', "成功", ""]
                    ret = ['1', retData]
            except Exception as e:
                msgtip = [REQmsg[2], f"应答{REQmsg[0]}", f'数据库操作不成功{e}', ""]
                ret = ['0', REQmsg[1], f"应答{REQmsg[0]}数据库操作不成功{e}"]
        else:
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}未定义命令"]
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '未定义命令', '']
        return msgtip, ret

        # 标注诊断/添加样本

        # 标注诊断/类型、用户信息
    def get_type_info(self, clientAddr, REQmsg):
        if REQmsg[1] == 4:
            type_info = self.dbUtil.get_typeInfo()
            user_manualinfo = self.dbUtil.getUserInfo()
            r, montage = self.appUtil.getMontage()
            if r == '0':
                montage = None
            ret = ['1', type_info, user_manualinfo, montage]
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}", '提取类型信息', '']
        else:
            ret = ['0', REQmsg[1], f"应答{REQmsg[0]}未定义命令"]
            msgtip = [REQmsg[2], f"应答{REQmsg[0]}提取类型信息", '未定义命令', '']
        return msgtip, ret




    def myTip(self, cmdId, tipMsg):
        row = self.tabV_model.rowCount()
        if row > 9:
            self.tabV_model.removeRow(0)
            row = 9

        now = datetime.datetime.now()
        item = QStandardItem(now.strftime("%Y-%m-%d %H:%M:%S"))
        self.tabV_model.setItem(row, 0, item)
        uInfo = self.curUser.users.get(tipMsg[0])
        if uInfo is None:
            item = QStandardItem(str(tipMsg[0]))
        else:
            item = QStandardItem(uInfo[1])
        self.tabV_model.setItem(row, 1, item)
        item = QStandardItem(tipMsg[1])
        self.tabV_model.setItem(row, 2, item)
        item = QStandardItem(tipMsg[2])
        self.tabV_model.setItem(row, 3, item)
        if len(tipMsg) > 3:
            item = QStandardItem(tipMsg[3])
            self.tabV_model.setItem(row, 4, item)
        else:
            tipMsg.append("")
        #self.dbUtil.sys_log(cmdId, tipMsg)

    def get_set_channel_info(self, set_description):
        return set_description.split('+')[3]
