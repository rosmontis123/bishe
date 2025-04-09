import ast
import datetime

import json

import os
import time, shutil
import re
import mne
import pyedflib
import pypinyin
import numpy as np
import urllib
import urllib.request
import smtplib
from email.mime.text import MIMEText

class appUtil():
    def __init__(self, dbUtil):
        self.root_path=os.path.dirname(os.path.dirname(__file__))+'\\'
        self.algorithm_path = self.root_path + 'client_root\\classifier\\'
        self.dbUtil = dbUtil
        self.model_path = os.path.join(self.root_path,'classifier\\models\\')

    def get_now_datetime(self):
        """
        @Description: 返回当前时间，格式为：年月日时分秒
        """
        return time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))

    def get_now_time(self):
        """
        @Description: 返回当前时间，格式为：时分秒
        """
        return time.strftime('%H-%M-%S', time.localtime(time.time()))

    def get_now_date(self):
        """
        @Description: 返回当前时间，格式为：年月日
        """
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))








    def GetSocketIpFile(self):
        f = open('service/server.txt')
        d = f.readline()
        f.close()
        sysd = eval(d)
        s_ip = sysd['server_ip']
        s_port = sysd['server_port']
        return s_ip, s_port

    def GetMysqlInfo(self):
        f = open('service/server.txt')
        d = f.readline()
        f.close()
        sysd = eval(d)
        return sysd





    def getMontage(self):
        try:
            with open('data/config.json', "r", encoding='utf8') as fp:
                data = json.load(fp)
                montageData = data.get('montages')
                fp.close()
                return '1',montageData
        except (IOError, OSError) as err:
            #print('getMontage', err)
            return '0', '打开导联文件文件无效'


    def addMontageScheme(self, scheme_name, channels=[]):
        try:
            with open('data/config.json', "r", encoding='utf8') as fp:
                data = json.load(fp)
                fp.close()
            with open('data/config.json', "w", encoding='utf8') as fp:
                new_montage_scheme = {'name': scheme_name, 'channels': channels}
                data['montages'].append(new_montage_scheme)
                json.dump(data, fp, ensure_ascii=False)
                fp.close()
                ret = ['1', '添加导联方案成功']
                return ret
        except (IOError, OSError) as err:
            print('addMontageScheme', err)
            ret = ['0', '打开导联文件文件无效']
            return ret

    def editMontageScheme(self, where_name, set_name):
        try:
            with open('data/config.json', "r", encoding='utf8') as fp:
                data = json.load(fp)
                fp.close()
            with open('data/config.json', "w", encoding='utf8') as fp:
                for i in range(len(data['montages'])):
                    if data['montages'][i]['name'] == where_name:
                        # print(data['montages'][i]['name'])
                        data['montages'][i]['name'] = set_name
                        break
                json.dump(data, fp, ensure_ascii=False)
                fp.close()
                ret = ['1', '编辑导联方案成功']
                return ret
        except (IOError, OSError) as err:
            print('editMontageScheme', err)
            ret = ['0', '打开导联文件文件无效']
            return ret

    def delMontageScheme(self, where_name):
        try:
            with open('data/config.json', "r", encoding='utf8') as fp:
                data = json.load(fp)
                fp.close()
            with open('data/config.json', "w", encoding='utf8') as fp:
                for i in range(len(data['montages'])):
                    if data['montages'][i]['name'] == where_name:
                        del_index = i
                        break
                del data['montages'][del_index]
                json.dump(data, fp, ensure_ascii=False)
                fp.close()
                ret = ['1', '删除导联方案成功']
                return ret
        except (IOError, OSError) as err:
            print('delMontageScheme', err)
            ret = ['0', '打开导联文件文件无效']
            return ret

    def saveMontageChannel(self, where_name, channels):
        try:
            with open('data/config.json', "r", encoding='utf8') as fp:
                data = json.load(fp)
                fp.close()
            with open('data/config.json', "w", encoding='utf8') as fp:
                for i in range(len(data['montages'])):
                    if data['montages'][i]['name'] == where_name:
                        data['montages'][i]['channels'] = channels
                        break
                json.dump(data, fp, ensure_ascii=False)
                fp.close()
                ret = ['1', '保存导联方案通道成功']
                return ret
        except (IOError, OSError) as err:
            print('saveMontageChannel', err)
            ret = ['0', '打开导联文件文件无效']
            return ret










# if __name__ == '__main__':
#     a = appUtil()
#     print(a.root_path)







