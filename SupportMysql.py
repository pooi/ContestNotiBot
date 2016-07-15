#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import MySQLdb

class SupportMysql:

    def __init__(self, db):
        self.db = db

    def initMember(self, chatID):
        ''' 초기 사용자를 등록하는 함수 (Register initial user) '''
        # 한 테이블만 예시로 사용자가 있는지 확인함
        msg1 = "SELECT chatID FROM memberTbl WHERE chatID={};".format(chatID)
        people = self.returnCommand(msg1)
        if len(people) == 0: # 사용자가 없다면 새로운 사용자를 등록
            msg = "INSERT INTO memberTbl VALUES('{}', (SELECT CURDATE()));".format(chatID)
            self.setCommand(msg)
            return True
        else: # 사용자가 존재한다면 예외 처리
            return False

    def returnCommand(self, msg):
        '''
        sql 명령문으로 부터 결과 값을 반환(sql 명령문을 인자로 받음)
        Return the result from sql command
        '''
        try:
            self.db.commit() # Database synchronization
            cur = self.db.cursor()
            cur.execute(msg)
            results = cur.fetchall() # sql 결과값 임시 저장
            data = [] # 빈배열 선언
            for result in results:
                data.append(result) # 배열을 결과값으로 채움
            cur.close()
            return data
        except MySQLdb.Error as e:
            return 'error'

    def setCommand(self, msg):
        ''' 설정할때 사용하는 sql명령문(sql 명령문을 인자로 받음[insert,update,delete]) '''
        try:
            self.db.commit()
            cur = self.db.cursor()
            cur.execute(msg)
            self.db.commit()
            cur.close()
            return True
        except MySQLdb.Error as e:
            return False


    def deleteMsg(self, table, condition):
        ''' 사용자를 삭제하는 명령문을 만듬(인자 ; 테이블명, chatID) '''
        msg = "DELETE FROM {} WHERE ({});".format(table, condition)
        return msg