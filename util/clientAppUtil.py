import ast
import os
import time, shutil
import hashlib
import uuid
import json
import re


class clientAppUtil():
    def __init__(self):
        self.root_path=os.path.dirname(os.path.dirname(__file__))+'\\'
        self.model_path = self.root_path + 'upload\\model\\'
        self.path = os.path.dirname(__file__)

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
        f = open(os.path.join(self.path, 'server.txt'))
        d = f.readline()
        f.close()
        sysd = eval(d)
        s_ip = sysd['server_ip']
        s_port = sysd['server_port']
        return s_ip, s_port

    def md5_string(self, in_str):
        md5 = hashlib.md5()
        md5.update(in_str.encode("utf8"))
        result = md5.hexdigest()
        return result

    def getMacAddress(self):
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ':'.join([mac[e:e + 2] for e in range(0, 11, 2)])








if __name__ == '__main__':
    a = clientAppUtil()
    print(a.root_path)
