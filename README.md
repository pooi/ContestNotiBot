<h1 align=center>ContestNotiBot</h1>
<p align=center>공모전 알림 봇은 공모전 정보를 제공해주는 사이트에 새로운 공모전이<br>업데이트 되었을 경우 텔레그램을 통해 이를 알려줍니다.</p>
<br>


공모전 알림 봇 활성화 <a href="https://telegram.me/ContestNotiBot">telegram.me/ContestNotiBot</a><br>
Bot available at <a href="https://telegram.me/ContestNotiBot">telegram.me/ContestNotiBot</a>

License : MIT License<br>
Contact & Help : ldayou@me.com<br>


## 개발에 참고한 문서
><a href="https://github.com/eternnoir/pyTelegramBotAPI">https://github.com/eternnoir/pyTelegramBotAPI</a><br>
><a href="http://www.hardcopyworld.com/gnuboard5/bbs/board.php?bo_table=lecture_rpi&wr_id=38">http://www.hardcopyworld.com/gnuboard5/bbs/board.php?bo_table=lecture_rpi&wr_id=38</a><br>
><a href="http://www.clien.net/cs2/bbs/board.php?bo_table=lecture&wr_id=324116&page=2">http://www.clien.net/cs2/bbs/board.php?bo_table=lecture&wr_id=324116&page=2</a>

<br>

## 공모전 사이트
>각각의 공모전 사이트에게 감사합니다.

<ul type=square>
  <li>대티즌 <a href="http://www.detizen.com/">detizen.com</a><br>
  <li>캠퍼스몬 <a href="http://campusmon.jobkorea.co.kr/">campusmon.jobkorea.co.kr</a><br>
  <li>allcontests <a href="http://all-con.co.kr/">all-con.co.kr</a><br>
  <li>위비티 <a href="http://www.wevity.com/">wevity.com</a><br>
</ul>

<br>

## Notice
>공모전 알림 봇은 <a href="https://core.telegram.org/bots/api">Telegram cli</a>, <a href="https://github.com/eternnoir/pyTelegramBotAPI">pyTelegramBotAPI</a>, MySQL, BeautifulSoup, apscheduler, 파이썬 2.7을 사용합니다.<br>

* pyTelegramBotAPI<br>
<a href="http://www.hardcopyworld.com/gnuboard5/bbs/board.php?bo_table=lecture_rpi&wr_id=8&page=1">http://www.hardcopyworld.com/gnuboard5/bbs/board.php?bo_table=lecture_rpi&wr_id=8&page=1</a>
```python
import telebot
from telebot import types
```

* MySQLdb<br>
<a href="http://www.hardcopyworld.com/gnuboard5/bbs/board.php?bo_table=lecture_rpi&wr_id=37">http://www.hardcopyworld.com/gnuboard5/bbs/board.php?bo_table=lecture_rpi&wr_id=37</a>
```python
import MySQLdb
```

* BeautifulSoup<br>
```
$ sudo pip install beautifulsoup4
```
```python
from bs4 import BeautifulSoup
```

* apscheduler<br>
<a href="http://www.clien.net/cs2/bbs/board.php?bo_table=lecture&wr_id=324116&page=2">http://www.clien.net/cs2/bbs/board.php?bo_table=lecture&wr_id=324116&page=2</a>
```
$ sudo pip install apscheduler
```
```python
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
```


<br>

## Usage
>기본적인 설정은 위의 링크대로 진행해주세요.<br>

이 프로젝트를 사용하기 위해서는 <a href="https://telegram.me/botfather">@BotFather</a>(<a href="https://core.telegram.org/bots#3-how-do-i-create-a-bot">안내</a>)를 통해 api key를 획득한 후 사용해주세요.

획득한 api key를 <a href="https://github.com/pooi/ContestNotiBot/blob/master/contestNoti_Bot.py">`contestNoti_Bot.py`</a>에 입력해주세요.
```python
API_TOKEN = '<INPUT_YOUR_API_KEY>'
bot = telebot.TeleBot(API_TOKEN)
```

MySQL과 연동을 위해 <a href="https://github.com/pooi/ContestNotiBot/blob/master/contestNoti_Bot.py">`contestNoti_Bot.py`</a>에 Host, ID, Password, DB Name을 입력해주세요.
```python
# Connect database
host = '<INPUT_YOUR_DATABASE_SERVER_HOST>'
db_id = '<INPUT_YOUR_DATABASE_ID>'
db_pw = '<INPUT_YOUR_DATABASE_PASSWORD>'
db_name = '<INPUT_YOUR_DATABASE_NAME>'
db = MySQLdb.connect( host, db_id, db_pw, db_name, charset='utf8') # Encoding utf-8
```

혹시 자신에게 메시지를 전송하고 싶다면 편의를 위해 자신의 Chat ID를 기록해두세요.
```python
administratorChatID = '<INPUT_YOUT_TELEGRAM_CHAT_ID>'
```

<br>

## Bot Commands
공모전 알림 봇은 4개의 명령어를 사용합니다.
```
/start        최초 시작시 사용되는 명령어입니다.
/subscribe    공모전 알림을 설정합니다.(/start와 동일)
/unsubscribe  공모전 알림을 해제합니다.
/help         도움말을 보여줍니다.
```

<br>

## How it works
공모전 알림 봇은 07시 ~ 20시까지 10분 간격으로 사이트들을 확인하여 새로운 공모전이 업데이트 되었을 경우 이를 사용자에게 전송합니다.

<br>

## Screenshot
<img src="https://github.com/pooi/ContestNotiBot/blob/master/Screenshot/IMG_1446.PNG" width=45%>
<img src="https://github.com/pooi/ContestNotiBot/blob/master/Screenshot/IMG_1448.PNG" width=45%><br>
