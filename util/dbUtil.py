import re
from random import sample

import numpy as np

from util.mysqlService import MySqlService


class dbUtil(MySqlService):
    def __init__(self):
        mysqlInfo = self.GetMysqlInfo()
        super().__init__(mysqlInfo['dbUrl'], mysqlInfo['dbPort'], mysqlInfo['dbUser'], mysqlInfo['dbPwd'],
                         mysqlInfo['dbName'])

    def GetMysqlInfo(self):
        f = open('service/server.txt')
        d = f.readline()
        f.close()
        sysd = eval(d)
        return sysd

    def getUserInfo(self, where_name='', where_value='', where_like=''):
        if where_name == '':
            sql = "select * from user_info "
        elif where_like != '':
            sql = f"select * from user_info where {where_name} like '%{where_value}%'"
        else:
            sql = f"select * from user_info where {where_name}='{where_value}'"
        user_info = self.myQuery(sql)
        return user_info

    def getUserInfoLen(self, where_name='', where_like=''):
        if where_name == '':
            sql = "select count(*) from user_info where uid != 1"
        else:
            sql = f"select count(*) from user_info where {where_name} Like '%{where_like}%' and uid != 1"
        len = self.myQuery(sql)
        return len

    def getUserInfoByPage(self, offset='', psize=''):
        sql = f"select * from user_info limit {offset}, {psize}"
        user_info = self.myQuery(sql)
        return user_info

    def getSearchUserInfoByPage(self, where_name, where_value, offset='', psize=''):
        sql = f"select * from user_info where {where_name} like '%{where_value}%' AND account != 'admin' order by uid " \
              f" limit {offset}, {psize} "
        user_info = self.myQuery(sql)
        return user_info

    def updateUserInfo(self, where_name, where_value, userInfo=None, set_name='', set_value=''):
        try:
            if userInfo is None:
                sql = "update user_info set {} = '{}' where {}='{}'".format(set_name, set_value, where_name,
                                                                            where_value)
                self.myExecuteSql(sql)
                return True
            else:
                sql = "update user_info set name = '{}', phone = '{}', email = '{}', labeler = '{}', student = '{}', teacher = '{}', doctor = '{}',researcher = '{}' where {}='{}'".format(
                    userInfo[1], userInfo[2], userInfo[3], userInfo[4], userInfo[5], userInfo[6], userInfo[7],
                    userInfo[8],
                    where_name, where_value)
                tag = self.myExecuteSql(sql)
                if tag == '':
                    return '1', str(tag)
                else:
                    return '0', str(tag)
        except Exception as e:
            print(e)
            return '0', str(e)

    def delUserInfo(self, where_name, where_value):
        try:
            sql = "delete from user_info where {} = '{}'".format(where_name, where_value)
            tag = self.myExecuteSql(sql)
            if tag == '':
                return '1', str(tag)
            else:
                return '0', str(tag)
        except Exception as e:
            print(re)
            return '0', str(e)

    def addUserInfo(self, user_info):
        try:
            sql = f"insert into user_info(account,pwd,name,phone,email,administrator,labeler,student,teacher,doctor,researcher) values " \
                  "('{}','{}','{}','{}','{}',{},{},{},{},{},{})".format(
                user_info[0], user_info[1], user_info[2], user_info[3], user_info[4], user_info[5], user_info[6],
                user_info[7], user_info[8], user_info[9], user_info[10])
            tag = self.myExecuteSql(sql)
            if tag == "":
                return '1', str(tag)
            else:
                return '0', str(tag)
        except Exception as e:
            return '0', str(e)

    # 密码修改模块
    # 更新用户信息
    def update_userInfo(self, user_msg='', flag='1'):
        try:
            if flag == "1":
                uid = user_msg[0]
                pwd = user_msg[1]
                sql = f"update user_info set pwd = '{pwd}' where uid='{uid}'"
            self.myExecuteSql(sql)
        except Exception as e:
            print("update_userInfo", e)
            return False
        return True

    # 标注类型
    # 获取标注类型信息
    def get_typeInfo(self, where_name='', where_value=''):
        try:
            if where_name == '':
                sql = "select * from type_info"
            else:
                sql = f"select * from type_info where {where_name} like '%{where_value}%'"
            type_info = self.myQuery(sql)
        except Exception as e:
            print("get_typeInfo", e)
            return None
        return type_info

    # 添加标注类型信息
    def add_typeInfo(self, type_info):
        try:
            type_name = type_info[0]
            description = type_info[1]
            category = type_info[2]
            sql = f"insert into type_info(type_name, description, category) values ('{type_name}','{description}', '{category}')"
            flag = self.myExecuteSql(sql)
            if flag == "":
                return True
            else:
                return False
        except Exception as e:
            print('addtypeInfo', e)

    # 删除标注类型信息
    def del_typeInfo(self, where_name, where_value):
        try:
            sql = f"delete from type_info where {where_name} = '{where_value}'"
            self.myExecuteSql(sql)
        except Exception as e:
            print('delTypeInfo', e)
            return False
        return True

    # 修改标注类型信息
    def update_typeInfo(self, set_value, where_name, where_value):
        try:
            sql = f"update type_info set type_name = '{set_value[0]}',description = '{set_value[1]}',category = '{set_value[2]}'where {where_name}='{where_value}' "
            self.myExecuteSql(sql)
        except Exception as e:
            print('updateTypeInfo', e)
            return False
        return True























    def queryConfigData(self, where_name='', where_value=''):
        try:
            if where_name == '':
                sql = "select * from config"
            else:
                sql = f"select * from config where `{where_name}`='{where_value}'"
            print(f'queryConfigData SQL: {sql}')
            config = self.myQuery(sql)
            print(config)
            return config
        except Exception as e:
            print('del_detailInfo', e)
            return False

    def addBasicConfig(self, config):
        try:
            sql = f"insert into config(config_name,sampling_rate,notch,low_pass,high_pass,`default`) values " \
                  "('{}',{},{},{},{},{})".format(config[0], config[1], config[2], config[3], config[4], config[5])
            flag = self.myExecuteSql(sql)
            print(f'addBasicConfig: {sql}')
            if flag == "":
                return True
            else:
                return False
        except Exception as e:
            return False

    def delBasicConfig(self, where_name, where_value):
        try:
            sql = "delete from config where {} = '{}'".format(where_name, where_value)
            re = self.myExecuteSql(sql)
            print(f'delBasicConfig sql: {sql}, re: {re}')
            if re == "":
                return True
            else:
                return False
        except Exception as re:
            return False

    def updateBasicConfig(self, where_name, where_value, config=None, set_name='', set_value=''):
        try:
            if config is None:
                sql = "update config set {} = '{}' where {}='{}'".format(set_name, set_value, where_name, where_value)
            else:
                sql = "update config set config_name = '{}', sampling_rate = '{}', notch = '{}', low_pass = '{}', high_pass = '{}', `default` = '{}' where {}='{}'".format(
                    config[1], config[2], config[3], config[4], config[5], config[6], where_name, where_value)
            print(f'updateBasicConfig SQL: {sql}')
            self.myExecuteSql(sql)
            return True
        except Exception as e:
            print(e)
            return False

    def checkConfigisUsed(self, value):
        selectTable = ['class', 'classifier', 'file_info', 'set_info', 'theme']
        flag = False
        for table in selectTable:
            sql = f"SELECT COUNT(*) AS usage_count FROM {table} WHERE config_id = {value};"
            re = self.myQuery(sql)
            if re[0][0] != 0:
                print(f'{table}')
                flag = True
                break
        return flag

    def getDoctorInfo(self, column='*', where_name='', where_like=''):
        try:
            if where_name == '':
                sql = f"select {column} from user_info where doctor='1' or researcher='1'"
            else:
                sql = f"select {column} from user_info where (doctor='1' or researcher='1') and {where_name} like '%{where_like}%'"
            print(f'getDoctorInfo sql: {sql}')
            user_info = self.myQuery(sql)
            return user_info
        except Exception as e:
            print('getDoctorInfo', e)
            return False

    def getAllConsInfo(self, where_name='', where_like='', date1='', date2='', userID=''):
        try:
            sql1 = """
            SELECT c.check_number, p.name AS patient_name,c.measure_date, u1.name AS pUid_name, u2.name AS cUid_name, c.state, 'NONE' AS create_name,'NONE' AS sign_date, c.description, c.check_id
            FROM check_info c
            JOIN patient_info p ON c.patient_id = p.patient_id
            JOIN user_info u1 ON c.pUid = u1.uid
            JOIN user_info u2 ON c.cUid = u2.uid
            WHERE c.state = 'uploaded'
            """
            sql2 = """
            SELECT
                    ci.check_number,pi.name AS patient_name,ci.measure_date,
                    u1.name AS pUid_name, u2.name AS cUid_name, di.state, ui.name AS create_name, di.sign_date, ci.description, ci.check_id
            FROM check_info AS ci 
            JOIN diag AS di ON ci.check_id = di.check_id
            JOIN patient_info AS pi ON ci.patient_id = pi.patient_id
            JOIN user_info AS ui ON di.uid = ui.uid
            JOIN user_info u1 ON ci.pUid = u1.uid
            JOIN user_info u2 ON ci.cUid = u2.uid
            """

            if where_name == 'check_number':
                sql1 = sql1 + f" and c.{where_name} like '%{where_like}%'"
                sql2 = sql2 + f" where ci.{where_name} like '%{where_like}%'"
            elif where_name == 'name':
                sql1 = sql1 + f" and p.{where_name} like '%{where_like}%'"
                sql2 = sql2 + f" where pi.{where_name} like '%{where_like}%'"

            if userID != '':
                sql1 = sql1 + f" and u2.uid = {userID}"
                sql2 = sql2 + f" and u2.uid = {userID}"

            if date1 != '' and date2 != '':
                sql1 = sql1 + f" and c.measure_date BETWEEN '{date1}' AND '{date2}'"
                sql2 = sql2 + f" and ci.measure_date BETWEEN '{date1}' AND '{date2}'"

            sql1 = sql1 + " ORDER BY c.measure_date DESC"
            sql2 = sql2 + " ORDER BY ci.measure_date DESC"

            print(f'getAllConsInfo SQL1: {sql1}')
            print(f'getAllConsInfo SQL2: {sql2}')
            check_info1 = self.myQuery(sql1)
            check_info2 = self.myQuery(sql2)
            return check_info1 + check_info2
        except Exception as e:
            print('getAllConsInfo', e)












    ### dsj ==[===

    def get_userNameByUids(self, uids=''):
        try:
            if uids == '':
                sql = "select uid,name from user_info"
            else:
                sql = f"select uid,name from user_info where uid in ({uids})"
            user_info = self.myQuery(sql)
        except Exception as re:
            return '0', str(re)
        return '1', user_info

    def get_patientNameByPids(self, pids=''):
        try:
            if pids == '':
                sql = "select patient_id,name from patient_info"
            else:
                sql = f"select patient_id,name from patient_info where patient_id in ({pids})"
            patientInfo = self.myQuery(sql)
        except Exception as re:
            return '0', str(re)
        return '1', patientInfo




    # zh 获取样本列表
    def get_sampleListInfo(self, check_id, file_id, channels, type_names, user_names, status_show):
        try:
            if status_show == True:
                sql = "select channel,begin,end,sample_info.uid,sample_info.type_id,type_name from sample_info," \
                      "type_info,user_info where check_id={} and file_id={} and " \
                      " (channel in {} or channel='all') and sample_info.type_id=type_info.type_id and type_info.type_name in " \
                      " {} and sample_info.uid=user_info.uid and user_info.name in {} order by begin".format(
                    check_id, file_id, channels, type_names, user_names)
            else:
                sql = "select channel,begin,end,sample_info.uid,sample_info.type_id,type_name from sample_info," \
                      "type_info,user_info  where check_id={} and  file_id={} and channel " \
                      "in {} and sample_info.type_id=type_info.type_id and type_info.type_name in {}  and sample_info.uid=" \
                      "user_info.uid and user_info.name in {} order by begin".format(
                    check_id, file_id, channels, type_names, user_names)
            sample_info = self.myQuery(sql)
        except Exception as re:
            return '0', str(re)
        return '1', sample_info








    def diag_getByPage(self, check_id='', pname='', uid='', diag_state='', other_where='', offset=0, psize=0):
        sql = " where diag.check_id = check_info.check_id "
        if check_id != '':
            sql += " and diag.check_id= " + str(check_id)
        if uid != '':
            sql += " and diag.uid= " + str(uid)
        if diag_state != '':
            sql += " and diag.state = '" + diag_state + "'"
        if other_where != '':
            sql += " and  " + str(other_where)
        if pname != '':
            sql += f" and  patient_id in (select patient_id FROM patient_info where name like '%{pname}%') "
        if offset >= 0 and psize > 0:
            sql += f" limit  {offset}, {psize}"
        sql = "select patient_id,measure_date, diag.uid, diag.state,diag.sign_date, alpha,slow,fast,amplitude,eyes," \
              "hyperventilation,sleep,abnormal_wave,attack_stage,summary,diag.check_id,check_info.pUid, " \
              "check_info.check_number,check_info.cUid " \
              " from diag,check_info " + sql
        try:
            dataSet = self.myQuery(sql)
        except Exception as re:
            return '0', str(re)
        return '1', dataSet

    # author:dsj  state enum('notDiagnosed','diagnosed','refused')
    # 通过patient_id,measure_date,uid,提取diag信息
    def diag_get(self, check_id='', uid='', diag_state='', other_where=''):
        sql = " where diag.check_id = check_info.check_id "
        if check_id != '':
            sql += " and diag.check_id = " + str(check_id)
        if uid != '':
            sql += " and diag.uid = " + str(uid)
        if diag_state != '':
            sql += " and diag.state = '" + diag_state + "'"
        if other_where != '':
            sql += " and  " + str(other_where)
        sql = "select patient_id,measure_date, diag.uid, diag.state,diag.sign_date, alpha,slow,fast,amplitude,eyes," \
              "hyperventilation,sleep,abnormal_wave,attack_stage,summary,diag.check_id,check_info.pUid, " \
              "check_info.check_number,check_info.cUid " \
              " from diag,check_info " + sql
        try:
            dataSet = self.myQuery(sql)
        except Exception as re:
            return '0', str(re)
        return '1', dataSet

    # author:dsj  state enum('notDiagnosed','diagnosed','refused')
    # 通过patient_id,measure_date,uid,提取diag信息
    def diag_get_forConsulting(self, uid=''):
        sql = " where diag.check_id = check_info.check_id and check_info.state in ('diagnosing','consulting') "
        if uid != '':
            sql += " and diag.check_id in (select check_id from  diag where state='notDiagnosed' and uid = " + str(
                uid) + ")"
        sql = "select patient_id,measure_date, diag.uid, diag.state,diag.sign_date, alpha,slow,fast,amplitude,eyes," \
              "hyperventilation,sleep,abnormal_wave,attack_stage,summary,diag.check_id,check_info.pUid, " \
              "check_info.check_number,check_info.cUid " \
              " from diag,check_info " + sql + " order by diag.check_id "
        try:
            dataSet = self.myQuery(sql)
        except Exception as re:
            return '0', str(re)
        return '1', dataSet
    def diag_get_refused_state(self,tempt):
        if not tempt:
            return []

            # 构建 SQL 查询
        queries = []
        for check_id, uid in tempt:
            queries.append(
                f"SELECT {check_id} AS check_id, {uid} AS uid, EXISTS (SELECT 1 FROM sample_info WHERE check_id = {check_id} AND uid = {uid}) AS `exists`")

        sql = " UNION ALL ".join(queries)
        results =self.myQuery(sql)
        # results = data.fetchall()
        exist_results = [row[2] for row in results]
        return exist_results

    def getAllSampleByFile(self, check_id, file_id, Puid):
        sql = f'select channel, begin, end, type_id from sample_info where check_id = {check_id} and file_id = {file_id} and uid = {Puid}'
        samples = self.myQuery(sql)
        return samples


if __name__ == '__main__':
    dbUtil = dbUtil()
    dbUtil.ramdom_add()
