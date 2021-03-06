#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
from bs4 import BeautifulSoup



from datetime import datetime, timedelta


class ContestParser:
    ''' 웹 사이트를 파싱함. siteList 혹은 siteNameList 변수를 통해 지원하는 사이트를 확인할 수 있음 '''

    # 지원하는 사이트 목록
    siteList = ['detizen', 'campusmon', 'allcon', 'wevity']
    #siteNameList = ['대티즌', '캠퍼스몬', '올콘', '위비티']
    siteNameList = {
            'detizen' : '대티즌',
            'campusmon' : '캠퍼스몬',
            'allcon' : '올콘',
            'wevity' : '위비티'
        }

    def returnParsingData(self, siteName):

        if siteName == 'detizen':
            return self.detizenParsing()
        elif siteName == 'campusmon':
            return self.campusmonParsing()
        elif siteName == 'allcon':
            return self.allconParsing()
        elif siteName == 'wevity':
            return self.wevityParsing()
        else:
            return 'error'

    def returnSiteName(self, site):
        try:
            return self.siteNameList[site]
        except:
            return 'error'


    def detizenParsing(self):
        try:
            mainURL = 'http://www.detizen.com/contest/'.encode("UTF-8")
            html = urllib.urlopen(mainURL)
            soup = BeautifulSoup(html, "html.parser")

            find = soup.find_all("ul", attrs={'class': "basic-list page-list"})

            parsingData = []

            for data in find:
                dataTemp = data.find_all('li', {'class':''})
                for d in dataTemp:
                    temp = {}
                    sponsor = d.find('span', {'class' : 'text-sponsor'}).text
                    title = d.find('a').text
                    period = d.find('p', {'class': 'text-period'}).text
                    period = period.split('\n')
                    period = str(period[2].replace("	", "")).replace('\r', "")
                    url =  mainURL + str(d.find('a')['href'])
                    temp['sponsor'] = sponsor
                    temp['title'] = title
                    temp['period'] = period
                    temp['url'] = url
                    parsingData.append(temp)

            if len(parsingData) == 0:
                return 'error'
            else:
                return parsingData
        except:
            return 'error'

    def thinkGoodParsing(self):
        try:
            mainURL = 'http://www.thinkcontest.com/bbs/board.php?bo_table=sub4&category=all'.encode("UTF-8")
            html = urllib.urlopen(mainURL)
            soup = BeautifulSoup(html, "html.parser")

            find = soup.find_all("div", attrs={'class': "contest_bn"})

            parsingData = []
            for data in find:
                # dataTemp = data.find_all('div', {'class': 'bn_tit'})

                temp = {}
                sponsor = data.find('li', {'class': 'host'}).text
                if sponsor == " ":
                    break
                title = data.find('div', {'class': 'bn_tit'}).text
                period = data.find('li', {'class': 'day'}).text
                url = "http://www.thinkcontest.com/" + str(data.find('a')['href'])
                temp['sponsor'] = sponsor
                temp['title'] = title
                temp['period'] = period
                temp['url'] = url
                parsingData.append(temp)

            if len(parsingData) == 0:
                return 'error'
            else:
                return parsingData
        except:
            return 'error'

    def allconParsing(self):
        try:
            mainURL = 'http://www.all-con.co.kr/uni_contest'.encode("UTF-8")
            html = urllib.urlopen(mainURL)
            soup = BeautifulSoup(html, "html.parser")

            find = soup.find_all("table", attrs={'class': "board_table"})

            parsingData = []
            for data in find:
                dataTemp = data.find_all('tr', {'class': 'list document '})
                for d in dataTemp:
                    temp = {}
                    sponsor = d.find('td', {'class': 'extravars white'}).text
                    sponsor = sponsor.replace('\n', "").replace("	", "")
                    title = d.find('a').text
                    title = title.replace('\n', "").replace("	", "")
                    period = d.find('p').text
                    period = period.replace('\n', "").replace("	", "").split(" ")[2][:17]
                    url = d.find('a')['href']
                    temp['sponsor'] = sponsor
                    temp['title'] = title
                    temp['period'] = period
                    temp['url'] = url
                    parsingData.append(temp)

            if len(parsingData) == 0:
                return 'error'
            else:
                return parsingData
        except:
            return 'error'

    def campusmonParsing(self):
        try:
            mainURL = 'http://campusmon.jobkorea.co.kr/Contest/List/'.encode("UTF-8")
            html = urllib.urlopen(mainURL)
            soup = BeautifulSoup(html, "html.parser")

            find = soup.find_all("table", attrs={'class': "cTb rank"})

            parsingData = []
            for data in find:
                dataTemp = data.find_all('tbody')
                for d in dataTemp:
                    dataTemp2 = d.find_all('tr')
                    for d2 in dataTemp2:
                        temp = {}
                        sponsor = d2.find('p', {'class': 'tx'}).text
                        bar = sponsor.find('|') - 1
                        sponsor = sponsor[:bar]
                        title = d2.find('a').text
                        period = d2.find('td', {'class': 'day'}).find('span')['title']
                        url = "http://campusmon.jobkorea.co.kr" + d2.find('a')['href']
                        temp['sponsor'] = sponsor
                        temp['title'] = title
                        temp['period'] = period
                        temp['url'] = url
                        parsingData.append(temp)

            if len(parsingData) == 0:
                return 'error'
            else:
                return parsingData
        except:
            return 'error'

    def wevityParsing(self):
        try:
            mainURL = 'http://www.wevity.com/?c=find&s=1&gub=1&gp=1'.encode("UTF-8")
            html = urllib.urlopen(mainURL)
            soup = BeautifulSoup(html, "html.parser")

            temp = []
            find = soup.find_all("ul", {'class': 'list'})
            for data in find:
                dataTemp = data.find_all('li')
                for d in dataTemp:
                    temp.append(d)

            del temp[0]

            parsingData = []

            for d in temp:
                temp = {}
                sponsor = d.find('div', {'class': 'organ'}).text

                title = d.find('a').text
                space = title.find('  ')
                title = title[:space]

                period = d.find('div', {'class': 'day'}).text
                stateMsg = d.find('div', {'class': 'day'}).find('span').text
                stateMsg = stateMsg.replace("	", "")
                period = period.replace("	", "").replace("\n", "")
                index = period.find(stateMsg)
                period = str(period[:index])
                slash = period.find('-')+1
                Dday = int(period[slash:])
                now = datetime.now()
                timegap = timedelta(days=Dday)
                after = (now + timegap).strftime("%Y-%m-%d")
                period = "~" + str(after)

                url = "http://www.wevity.com" + d.find('a')['href']

                temp['sponsor'] = sponsor
                temp['title'] = title
                temp['period'] = period
                temp['url'] = url
                parsingData.append(temp)

            if len(parsingData) == 0:
                return 'error'
            else:
                return parsingData
        except:
            return 'error'

    def findListIndex(self, findList, item):
        try:
            index = findList.index(item)
            return int(index)
        except:
            return -1

    def printList(self, parsingData):
        for p in parsingData:
            text = (
                "주최 : {}\n"
                "제목 : {}\n"
                "기간 : {}\n"
                "url : {}\n"
            )
            print(text.format(p['sponsor'], p['title'], p['period'], p['url']))