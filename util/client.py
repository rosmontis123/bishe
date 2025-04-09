# -*- coding: utf-8 -*-
import threading

from PyQt5.QtCore import Qt, pyqtSignal, QObject

from threading import Thread
from util.socketClient import socketClient


class client(QObject, socketClient):
    ## dsj [ ===



    # ---标注查询manualQuery ---
    mq_pagingResSig = pyqtSignal(list)
    mq_get_diags_DiagnosedResSig = pyqtSignal(list)
    mq_get_type_infoResSig = pyqtSignal(list)
    mq_get_fileNameByIdDateResSig = pyqtSignal(list)
    mq_openEEGFileResSig = pyqtSignal(list)
    mq_load_dataDynamicalResSig = pyqtSignal(list)
    mq_init_SampleListResSig = pyqtSignal(list)
    mq_get_diagResSig = pyqtSignal(list)


    ## dsj ] ===
    # 服务器异常信号
    serverExceptSig = pyqtSignal()

    # 登录
    loginResSig = pyqtSignal(int, str)
    logoutResSig = pyqtSignal(list)

    # 退出
    quitResSig = pyqtSignal()

    # 密码修改
    changePwdResSig = pyqtSignal(list)

    # 用户管理
    # 回调获取用户信息的信号
    getUserInfoResSig = pyqtSignal(list)
    # 回调添加用户信息的信号
    addUserInfoResSig = pyqtSignal(list)
    # 回调编辑用户信息的信号
    updateUserInfoResSig = pyqtSignal(list)
    # 回调删除用户信息的信号
    delUserInfoResSig = pyqtSignal(list)
    userPagingResSig = pyqtSignal(list)
    inquiryUserInfoResSig = pyqtSignal(list)

    # 主界面模块
    # 基本配置
    getConfigDataResSig = pyqtSignal(list)
    # 添加基本配置信号
    addBasicConfigResSig = pyqtSignal(tuple)
    # 更新基本配置信号
    updBasicConfigResSig = pyqtSignal(list)
    # 删除基本配置信号
    delBasicConfigResSig = pyqtSignal(list)

    # 配置选择
    getCurConfigDataResSig = pyqtSignal(tuple)
    getAllConfigDataResSig = pyqtSignal(list)
    chgCurUserConfigResSig = pyqtSignal(list)

    # 标注类型
    # 回调获取标注类型信息的信号
    getTypeInfoResSig = pyqtSignal(list)
    # 回调添加标注类型的信号
    addTypeInfoResSig = pyqtSignal(list)
    # 回调删除标注类型的信号
    delTypeInfoResSig = pyqtSignal(list)
    # 回调编辑标注类型的信号
    updateTypeInfoResSig = pyqtSignal(list)

    # 导联配置
    # 回调获取导联配置的信号
    getMontageResSig = pyqtSignal(list)
    # 回调添加导联方案的信号
    addMontageSchemeResSig = pyqtSignal(list)
    # 回调添加导联方案的信号
    editMontageSchemeResSig = pyqtSignal(list)
    # 回调删除导联方案的信号
    delMontageSchemeResSig = pyqtSignal(list)
    # 回调添加导联方案通道的信号
    saveMontageChannelResSig = pyqtSignal(list)





    def __init__(self, s_ip=None, s_port=None, cAppUtil=None):
        super().__init__()
        # tUser存放的信息顺序为
        # [uid, account, name, phone, email, administrator, labeler, student, teacher,
        # doctor, researcher, macAddr, defaultConfigID, now, curAuthority]
        self.tUser = None
        self.s_ip = s_ip
        self.s_port = s_port
        self.cAppUtil = cAppUtil
        self.macAddr = self.cAppUtil.getMacAddress()

    # 诊断标注/提取诊断信息
    def mq_paging(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manualQuery", 30, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调 诊断查询/提取诊断信息信号
    def mq_pagingRes(self, REPmsg):
        self.mq_pagingResSig.emit(list(REPmsg[3]))

    # 诊断查询/提取诊断信息
    def mq_get_diag(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manualQuery", 25, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调 诊断查询/提取诊断信息信号
    def mq_get_diagRes(self, REPmsg):
        self.mq_get_diagResSig.emit(list(REPmsg[3]))

    # 诊断查询/提取样本信息
    def mq_init_SampleList(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manualQuery", 16, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的诊断查询/提取样本信息 结果
    def mq_init_SampleListRes(self, REPmsg):
        self.mq_init_SampleListResSig.emit(list(REPmsg[3]))

    # 诊断查询/读取脑电文件数据块，拼接读取
    def mq_load_dataDynamical10(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manualQuery", 10, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的 诊断查询/读取脑电文件数据块，拼接读取 结果
    def mq_load_dataDynamical10Res(self, REPmsg):
        self.mq_load_dataDynamicalResSig.emit(list(REPmsg[3]))

    # 诊断查询/读取脑电文件数据块，首次读取
    def mq_load_dataDynamical(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manualQuery", 9, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的 诊断查询/读取脑电文件数据块，首次读取结果
    def mq_load_dataDynamicalRes(self, REPmsg):
        self.mq_load_dataDynamicalResSig.emit(list(REPmsg[3]))


    # 诊断查询/打开脑电文件
    def mq_openEEGFile(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manualQuery", 8, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的诊断查询/打开脑电文件结果
    def mq_openEEGFileRes(self, REPmsg):
        self.mq_openEEGFileResSig.emit(list(REPmsg[3]))

    # 诊断查询/脑电文件
    def mq_get_fileNameByIdDate(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manualQuery", 7, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的诊断查询/脑电文件结果
    def mq_get_fileNameByIdDateRes(self, REPmsg):
        self.mq_get_fileNameByIdDateResSig.emit(list(REPmsg[3]))


    # 诊断查询/类型、用户信息
    def mq_get_type_info(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manualQuery", 4, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调，处理服务端回传的诊断查询/类型、用户信息结果
    def mq_get_type_infoRes(self, REPmsg):
        self.mq_get_type_infoResSig.emit(list(REPmsg[3]))

    # 诊断查询/提取诊断信息
    def mq_get_diags_Diagnosed(self, REQdata):
        REQdata.insert(0, self.macAddr)
        msg = ["manualQuery", 1, self.tUser[0], REQdata]
        self.sendRequest(msg)

    # 回调 诊断查询/提取诊断信息
    def mq_get_diags_DiagnosedRes(self, REPmsg):
        self.mq_get_diags_DiagnosedResSig.emit(list(REPmsg[3]))







    ## dsj ] ===
    # 登录功能
    # 向服务端发送用户登录请求
    def login(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["login", 1, 0, REQmsg]
        self.isConnected = True
        self.sockOpenConn(self.s_ip, self.s_port)
        threading.Thread(target=self.receive_service_data).start()
        self.sendRequest(msg)

    # 回调，处理服务端回传的登录结果
    def loginRes(self, REPmsg):
        self.tUser = REPmsg[3][2]
        case = REPmsg[3][0]
        msg = REPmsg[3][1]
        print(f"loginRes REPData[3]: {self.tUser}")
        self.loginResSig.emit(case, msg)

    # 切换用户功能
    # 向服务端发送用户退出请求
    def logout(self, cmid):
        account = self.tUser[1]
        REQmsg = [account]
        REQmsg.insert(0, self.macAddr)
        msg = [cmid, 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调，处理服务端回传的登出处理结果
    def logoutRes(self, REPData):
        data = REPData[3]
        self.logoutResSig.emit(list(data))
        self.sockClose()

    # 回调，处理服务端回传的退出处理结果
    def quitRes(self, revData):
        self.quitResSig.emit()
        self.sockClose()

    # 修改密码功能
    # 向服务器发送修改密码请求
    def changePwd(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["pwd", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调，处理服务端回传的修改密码处理结果
    def pwdRes(self, REPData):
        self.changePwdResSig.emit(list(REPData[3]))

    # 用户管理功能
    # 向服务器发送获取用户信息请求
    def getUserInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["userManager", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调，处理服务器获取用户信息结果
    def getUserInfoRes(self, REPData):
        self.getUserInfoResSig.emit(list(REPData[3]))

    # 向服务器发送新增用户信息请求
    def addUserInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["userManager", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调，处理服务器新增用户信息结果
    def addUserInfoRes(self, REPData):
        self.addUserInfoResSig.emit(list(REPData[3]))

    # 向服务器发送删除用户信息请求
    def delUserInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["userManager", 3, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调，处理服务器删除用户信息结果
    def delUserInfoRes(self, REPData):
        self.delUserInfoResSig.emit(list(REPData[3]))

    # 向服务器发送编辑用户信息请求
    def updateUserInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["userManager", 4, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调，处理服务器编辑用户信息结果
    def updateUserInfoRes(self, REPData):
        self.updateUserInfoResSig.emit(list(REPData[3]))

    def userPaging(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["userManager", 5, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调，处理服务器获取用户信息结果
    def userPagingRes(self, REPData):
        self.userPagingResSig.emit(list(REPData[3]))

    def inquiryUserInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["userManager", 6, self.tUser[0], REQmsg]
        self.sendRequest(msg)

        # 回调，处理服务器获取用户信息结果

    def inquiryUserInfoRes(self, REPData):
        self.inquiryUserInfoResSig.emit(list(REPData[3]))

    def getConfigData(self):
        msg = ["basicConfig", 1, self.tUser[0], [self.macAddr]]
        self.sendRequest(msg)

        # 回调，处理服务器回传的基本配置信息

    def getConfigRes(self, REPData):
        self.getConfigDataResSig.emit(list(REPData[3][3]))

        # 向服务器发送添加基本配置的请求

    def addBasicConfig(self, REQmsg):
        msg = ["basicConfig", 2, self.tUser[0], [self.macAddr] + REQmsg]
        self.sendRequest(msg)

        # 回调，处理服务器回传的基本配置信息

    def addBasicConfigRes(self, REPData):
        print(f'addBasicConfigRes: {REPData}')
        self.addBasicConfigResSig.emit(REPData[3][3])

        # 向服务器发送修改基本配置的逻辑

    def updateBasicConfig(self, REQmsg):
        msg = ["basicConfig", 4, self.tUser[0], [self.macAddr] + REQmsg]
        self.sendRequest(msg)

        # 回调，处理服务器传回来的更新基本配置结果

    def updateBasicConfigRes(self, REPData):
        self.updBasicConfigResSig.emit([REPData[3][0], REPData[3][3]])

        # 向服务器发送删除基本配置的请求

    def delBasicConfig(self, REQmsg):
        msg = ["basicConfig", 3, self.tUser[0], [self.macAddr] + REQmsg]
        self.sendRequest(msg)

        # 回调，处理服务器传回来的基本配置结果

    def delBasicConfigRes(self, REPData):
        self.delBasicConfigResSig.emit([REPData[3][0], REPData[3][3]])

        # 获取默认的基本配置

    def getCurConfigData(self):
        msg = ["configOptions", 1, self.tUser[0], [self.macAddr, self.tUser[12]]]
        print(f'getCurConfigData MSG: {msg}')
        self.sendRequest(msg)

    def getCurConfigDataRes(self, REPData):
        print(f'getCurConfigDataRes ...')
        self.getCurConfigDataResSig.emit(REPData[3][3])


    def getAllConfigData(self):
        msg = ["configOptions", 2, self.tUser[0], [self.macAddr]]
        self.sendRequest(msg)

    def getAllConfigDataRes(self, REPData):
        self.getAllConfigDataResSig.emit(list(REPData[3][3]))


    def chgCurUserConfig(self, REQmsg):
        msg = ["configOptions", 3, self.tUser[0], [self.macAddr] + REQmsg]
        self.sendRequest(msg)

    def chgCurUserConfigRes(self, REPData):
        self.chgCurUserConfigResSig.emit(list(REPData[3][0]))


    # 导联配置功能
    # 向服务器发送获取导联配置信息的请求
    def getMontage(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["montage", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器获取导联配置信息的结果
    def getMontageRes(self, REPData):
        self.getMontageResSig.emit(list(REPData[3]))

    # 向服务器发送添加导联配置方案的请求
    def addMontageScheme(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["montage", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器添加导联方案的结果
    def addMontageSchemeRes(self, REPData):
        self.addMontageSchemeResSig.emit(list(REPData[3]))

    # 向服务器发送编辑导联配置方案的请求
    def editMontageScheme(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["montage", 3, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器编辑导联方案的结果
    def editMontageSchemeRes(self, REPData):
        self.editMontageSchemeResSig.emit(list(REPData[3]))

    # 向服务器发送删除导联配置方案的请求
    def delMontageScheme(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["montage", 4, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器删除导联方案的结果
    def delMontageSchemeRes(self, REPData):
        self.delMontageSchemeResSig.emit(list(REPData[3]))

    # 向服务器发送添加导联配置方案的请求
    def saveMontageChannel(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["montage", 5, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 回调,处理服务器添加导联方案的结果
    def saveMontageChannelRes(self, REPData):
        self.saveMontageChannelResSig.emit(list(REPData[3]))




    # 标注类型模块
    # 查询标注类型模块方法
    def getTypeInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["labelType", 1, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的查询标注类型的结果
    def getTypeInfoRes(self,REPData):
        print(REPData[3])
        self.getTypeInfoResSig.emit(list(REPData[3]))

    # 添加标注类型信息
    def addTypeInfo(self,REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["labelType", 2, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的添加标注类型信息
    def addTypeInfoRes(self, REPData):
        self.addTypeInfoResSig.emit(REPData[3])

    # 删除标注类型信息
    def delTypeInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["labelType", 3, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的删除标注类型信息
    def delTypeInfoRes(self, REPData):
        self.delTypeInfoResSig.emit(REPData[3])

    # 修改标注类型信息
    def updateTypeInfo(self, REQmsg):
        REQmsg.insert(0, self.macAddr)
        msg = ["labelType", 4, self.tUser[0], REQmsg]
        self.sendRequest(msg)

    # 处理客户端返回的修改标注类型信息
    def updateTypeInfoRes(self, REPData):
        print(REPData[3])
        self.updateTypeInfoResSig.emit(list(REPData[3]))
        # self.updateTypeInfoResSig.emit(list(REPData[3]))



    def sendRequest(self, msg):
        # r = self.sockOpenConn(self.s_ip, self.s_port)
        # if r is None:
        #     msg[3] = ['0','','网络忙.']
        #     self.appMain('', msg)
        #     return
        ret = self.send_client_data(msg)
        if ret:
            return True
        else:
            self.sockClose()
            self.serverExceptSig.emit()
            return False


    def appMain(self, serverAddr, REQmsg):
        # 退出
        if REQmsg[0] == 'quit' and REQmsg[1] == 1:
            self.quitRes(REQmsg)
        # 登出
        elif REQmsg[0] == 'logout' and REQmsg[1] == 1:
            self.logoutRes(REQmsg)
        # 登录
        elif REQmsg[0] == 'login' and REQmsg[1] == 1:
            self.loginRes(REQmsg)

        # 密码修改
        elif REQmsg[0] == 'pwd' and REQmsg[1] == 1:
            self.pwdRes(REQmsg)

        # 获取用户信息
        elif REQmsg[0] == 'userManager' and REQmsg[1] == 1:
            self.getUserInfoRes(REQmsg)

        # 新增用户信息
        elif REQmsg[0] == 'userManager' and REQmsg[1] == 2:
            self.addUserInfoRes(REQmsg)

        # 删除用户信息
        elif REQmsg[0] == 'userManager' and REQmsg[1] == 3:
            self.delUserInfoRes(REQmsg)

        # 编辑用户信息
        elif REQmsg[0] == 'userManager' and REQmsg[1] == 4:
            self.updateUserInfoRes(REQmsg)

        # 编辑用户信息
        elif REQmsg[0] == 'userManager' and REQmsg[1] == 5:
            self.userPagingRes(REQmsg)

        elif REQmsg[0] == 'userManager' and REQmsg[1] == 6:
            self.inquiryUserInfoRes(REQmsg)


        # 获取导联配置信息
        elif REQmsg[0] == 'montage' and REQmsg[1] == 1:
            self.getMontageRes(REQmsg)

        # 添加导联方案
        elif REQmsg[0] == 'montage' and REQmsg[1] == 2:
            self.addMontageSchemeRes(REQmsg)

        # 编辑导联方案
        elif REQmsg[0] == 'montage' and REQmsg[1] == 3:
            self.editMontageSchemeRes(REQmsg)

        # 删除导联方案
        elif REQmsg[0] == 'montage' and REQmsg[1] == 4:
            self.delMontageSchemeRes(REQmsg)

        # 保存导联方案通道
        elif REQmsg[0] == 'montage' and REQmsg[1] == 5:
            self.saveMontageChannelRes(REQmsg)


        # 标注类型模块
        # 回调获取标注类型信息
        elif REQmsg[0] == 'labelType' and REQmsg[1] == 1:
            self.getTypeInfoRes(REQmsg)

        # 回调增加标注类型信息
        elif REQmsg[0] == 'labelType' and REQmsg[1] == 2:
            self.addTypeInfoRes(REQmsg)

        # 回调删除标注类型信息
        elif REQmsg[0] == 'labelType' and REQmsg[1] == 3:
            self.delTypeInfoRes(REQmsg)

        # 回调修改标注类型信息
        elif REQmsg[0] == 'labelType' and REQmsg[1] == 4:
            self.updateTypeInfoRes(REQmsg)

        # 基本设置

        elif REQmsg[0] == 'basicConfig' and REQmsg[1] == 1:
            self.getConfigRes(REQmsg)

        elif REQmsg[0] == 'basicConfig' and REQmsg[1] == 2:
            self.addBasicConfigRes(REQmsg)

        elif REQmsg[0] == 'basicConfig' and REQmsg[1] == 3:
            self.delBasicConfigRes(REQmsg)

        elif REQmsg[0] == 'basicConfig' and REQmsg[1] == 4:
            self.updateBasicConfigRes(REQmsg)


        # 配置选择
        elif REQmsg[0] == 'configOptions' and REQmsg[1] == 1:
            self.getCurConfigDataRes(REQmsg)
        elif REQmsg[0] == 'configOptions' and REQmsg[1] == 2:
            self.getAllConfigDataRes(REQmsg)
        elif REQmsg[0] == 'configOptions' and REQmsg[1] == 3:
            self.chgCurUserConfigRes(REQmsg)

        # 诊断查询/查询、分页
        elif REQmsg[0] == 'manualQuery' and REQmsg[1] == 30:
            self.mq_pagingRes(REQmsg)

        # 诊断查询/提取诊断信息
        elif REQmsg[0] == 'manualQuery' and REQmsg[1] == 25:
            self.mq_get_diagRes(REQmsg)
        # 标注诊断/(绘图设置)提取样本信息(绘图设置)
        elif REQmsg[0] == 'manualQuery' and REQmsg[1] == 16:
            self.mq_init_SampleListRes(REQmsg)

        # 诊断查询/读取脑电文件数据块
        elif REQmsg[0] == 'manualQuery' and REQmsg[1] == 10:
            self.mq_load_dataDynamical10Res(REQmsg)

        elif REQmsg[0] == 'manualQuery' and REQmsg[1] == 9:
            self.mq_load_dataDynamicalRes(REQmsg)

        # 诊断查询/打开脑电文件
        elif REQmsg[0] == 'manualQuery' and REQmsg[1] == 8:
            self.mq_openEEGFileRes(REQmsg)

        # 诊断查询/脑电文件
        elif REQmsg[0] == 'manualQuery' and REQmsg[1] == 7:
            self.mq_get_fileNameByIdDateRes(REQmsg)
        # 诊断查询/类型、用户信息
        elif REQmsg[0] == 'manualQuery' and REQmsg[1] == 4:
            self.mq_get_type_infoRes(REQmsg)

        # 诊断查询/提取诊断信息
        elif REQmsg[0] == 'manualQuery' and REQmsg[1] == 1:
            self.mq_get_diags_DiagnosedRes(REQmsg)






        else:
            print(f"{REQmsg[0]}.{REQmsg[1]}未定义")
