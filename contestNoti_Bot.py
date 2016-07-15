#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import pickle

from ContestParser import *
from MyScheduler import * # import Scheduler
from SupportMysql import * # import SQL support class

from multiprocessing import Process

# Telegram interface
import telebot
from telebot import types, apihelper

API_TOKEN = '<INPUT_YOUR_API_KEY>'
bot = telebot.TeleBot(API_TOKEN)

administratorChatID = '<INPUT_YOUR_TELEGRAM_CHAT_ID>'

host = '<INPUT_YOUR_DATABASE_SERVER_HOST>'
db_id = '<INPUT_YOUR_DATABASE_ID>'
db_pw = '<INPUT_YOUR_DATABASE_PASSWORD>'
db_name = '<INPUT_YOUR_DATABASE_NAME>'
db = MySQLdb.connect( host, db_id, db_pw, db_name, charset='utf8') # Encoding utf-8

mydb = SupportMysql(db) # DB controller
scheduler = Scheduler(bot)
parser = ContestParser()

# /help 명령어를 사용하였을때 전송할 메시지
help_message =(
    "<INPUT_YOUR_HELP_MESSAGE>"
)

# /start 명령어를 사용하였을때 전송할 메시지
start_message_True=( # 데이터베이스에 성공적으로 사용자를 저장하였을 경우
    "<INPUT_YOUR_MESSAGE>"
)
start_message_False=( # 데이터베이스에 이미 저장되있는 사용자일 경우
    "<INPUT_YOUR_MESSAGE>"
)


def sendNotification(bot, mydb):
    ''' 웹 사이트를 파싱 후 새로 업데이트된 정보를 확인하고 사용자들에게 메시지를 전송 '''

    notiList = [] # [[site name, parsing list]...] 알림을 전송해야하는 리스트 저장

    ContestListFile = [] # 정보가 저장되어있는 파일 이름 목록 저장
    siteList = parser.siteList # 지원하는 사이트 이름을 가져옴(웹사이트 파싱때 사용)
    siteNameList = parser.siteNameList # 지원하는 사이트 이름을 한글로 가져옴(메시지 전송때 사용)

    parsingData = [] # 파싱된 데이터들이 저장됨

    for s in siteList:
        ContestListFile.append(s + "List.data") # 저장된 파일 이름 목록을 저장
        temp = parser.returnParsingData(s) # 각 웹사이트를 파싱해서 임시 변수에 저장
        parsingData.append(temp)

    for parData in parsingData: # 각각의 웹사이트별로 파싱된 정보를 이용

        before = [] # 이전에 파싱했던 정보를 가져옴 (이전 기록과 현재기록을 비교해 새롭게 업데이트된 리스트를 체크하기 위함)

        # 무식한 방법이지만 우선 이렇게 처리
        index = int(parsingData.index(parData))
        fileName = ContestListFile[index]
        siteName = siteNameList[index]

        try: # 저장된 파일이 존재할 경우
            # 이전에 저장한 기록을 로드
            f = open(fileName, 'rb')
            before = pickle.load(f)
            f.close()

            # 새로 파싱한 정보를 새롭게 저장
            f = open(fileName, 'wb')
            pickle.dump(parData, f)
            f.close()
        except: # 저장된 파일이 존재하지 않을 경우
            # 새로 파싱한 정보를 새롭게 저장
            f = open(fileName, 'wb')
            pickle.dump(parData, f)
            f.close()

            before = parData # 현재 파싱된 정보를 이전 정보로 사용함

            # (결과적으로 처음에는 알림이 전송되지 않음)

        if before != 'error': # 만약 파싱을 제대로 못하였을 경우(사이트 구조가 바꼈을 경우 등)

            for b in before: # 파싱한 공모전의 세부 리스트를 반복(한 사이트의 여러 공모전 목록)
                # 이전 기록의 가장 최근에 업데이트된 공모전부터
                # 새롭게 파싱한 목록에서 몇번째 인덱스인지 확인
                # 혹시 이전에 기록된 공모전 소개 페이지가 이후 삭제되었을 경우를 대비해
                # 새롭게 파싱한 목록에서 찾을 수 있을때까지 반복
                #test = parData
                #test[0]['title'] = "rrr"
                #tempIndex = parser.findListIndex(test, b)
                tempIndex = parser.findListIndex(parData, b)
                if tempIndex != -1: # 찾았을 경우 (못 찾을 경우 -1이 리턴됨)

                    saveList = [] # 새롭게 업데이트된 공모전들이 저장됨

                    for i in range(tempIndex): # 새롭게 업데이트된 공모전들 저장
                        saveList.append(parData[i])

                    notiList.append([siteName, saveList]) # 사이트 이름과 함께 저장(추후 사전으로 변경)
                    break

        elif before == 'error': # 사이트에서 제대로 파싱하지 못했을 경우 빠르게 대응하기 위해
            bot.send_message(administratorChatID, "{} 사이트 에러 확인 요망".format(siteName)) # 관리자에게 에러 메시지 전송
            pass
        else:
            pass

    messageList = [] # 전송할 메시지들이 저장됨 (새롭게 업데이트된 공모전 리스트)

    for n in notiList: # 전송할 메시지를 제작
        siteName = n[0]
        parserList = n[1]

        for p in parserList:
            text = (
                "[{siteName}] {title} | {period} | {sponsor}\n{url}"
            )
            msg = text.format(siteName=siteName, title=p['title'], period=p['period'], sponsor=p['sponsor'],
                              url=p['url'])
            messageList.append(msg)

    memberList = mydb.returnCommand("SELECT * FROM memberTbl") # DB에 저장된 사용자들을 가져옴
    if memberList == 'error': # DB에서 가져올때 에러값이 리턴되었을 경우
        bot.send_message(administratorChatID, "DB 에러 확인 요망") # 관리자에게 에러 메시지 전송
    else:
        for data in memberList: # 사용자들에게 메시지 전송 (전송 속도를 위해 멀티 프로세싱 사용)
            cid = data[0]
            p = Process(target=sendContest, args=(bot, mydb, cid, messageList))
            p.start()
            #for msg in messageList:
            #    bot.send_message(cid, msg)

    # SendNotification End

def sendContest(bot, mydb, cid, messageList):
    ''' 공모전 알림을 사용자들에게 전송함 '''
    for msg in messageList:
        try: # 메시지 전송을 시도
            bot.send_message(cid, msg)
        except telebot.apihelper.ApiException as e:
            error_code = str(e.result) # 에러코드를 저장함
            if error_code.find("403") != -1: # 403에러(사용자가 봇을 삭제 및 정지하였을 경우 발생)가 발생했을 경우
                # 사용자를 DB에서 제거함
                msg = mydb.deleteMsg('memberTbl', "chatID = '{}'".format(cid))
                check = mydb.setCommand(msg)
                if check==False: # DB에서 정상적으로 명령어를 실행하지 못했을 경우
                    bot.send_message(administratorChatID, "DB 멤버삭제 에러") # 관리자에게 에러 메시지 전송
                break



if __name__ == '__main__':
    scheduler.scheduler('cron', "1", sendNotification, bot, mydb) # 7~20시 사이에 10분 간격으로 동작
    pass

# When receive '/start' command
@bot.message_handler(commands=['start'])
def send_start(m):
    ''' Register user chatID in the database  '''
    cid = m.chat.id # Get chat ID
    check = mydb.initMember(cid) # Verify that the user has already been registered and register user chatId in a database.
    name = m.chat.last_name + m.chat.first_name # Get user name
    markup = types.ReplyKeyboardHide() # Keyboard markup

    if check: # Send success message
        msg = start_message_True.format(name, name, cid) + '\n' + help_message
        try:
            bot.send_message(cid, msg, reply_markup=markup)
        except telebot.apihelper.ApiException as e:
            pass

    else: # Send fail message
        msg = start_message_False.format(name)
        try:
            bot.send_message(cid, msg, reply_markup=markup)
        except telebot.apihelper.ApiException as e:
            pass

# When receive '/help' command
@bot.message_handler(commands=['help'])
def send_help(m):
    ''' Send help message '''
    cid = m.chat.id
    markup = types.ReplyKeyboardHide()
    try:
        bot.send_message(cid, help_message, reply_markup=markup)
    except telebot.apihelper.ApiException as e:
        pass

# When receive '/bot_restart' command
@bot.message_handler(commands=['bot_restart'])
def bot_restart(m):
    ''' Register user chatID in a database  '''
    cid = m.chat.id # Get chat ID
    if cid == administratorChatID:
        bot.send_message(cid, "봇을 재시작합니다.")
        os.system("<INPUT_YOUR_RESTART_COMMAND>")
    else:
        try:
            bot.send_message(cid, "권한이 없습니다.")
        except telebot.apihelper.ApiException as e:
            return

# Receive all message
@bot.message_handler(func=lambda message : True)
def echo_all(m):
    if m.text == '/cancel':
        pass
    elif m.text[0] == '/':
        try:
            bot.send_message(m.chat.id, '{} 명령어가 존재하지 않습니다.\n이 봇의 명령어는 /help 명령어를 통해 확인할 수 있습니다.'.format(m.text))
        except telebot.apihelper.ApiException as e:
            pass
    else:
        pass

bot.polling(none_stop=True)
