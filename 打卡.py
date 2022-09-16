import base64
import hashlib
import hmac
import json
import pyautogui
import random
import requests
import time
import urllib.parse
import os
from chinese_calendar import is_holiday
from datetime import datetime


def send(msg):
    headers = {'Content-Type': 'application/json', "Charset": "UTF-8"}
    # 这里替换为复制的完整 webhook 地址
    prefix = 'https://oapi.dingtalk.com/robot/send?access_token' \
             '=872281511d7738d801eaf916782c1b3509375c2c31c7b6e1821418e42e475bdd '
    timestamp = str(round(time.time() * 1000))
    # 这里替换为自己复制过来的加签秘钥
    secret = 'SEC9b10d0106744fb02b5b9bd20eb0bd46842b8d1024fb22aa96876bc395d56209e'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    url = f'{prefix}&timestamp={timestamp}&sign={sign}'

    # 钉钉消息格式，其中 msg 就是我们要发送的具体内容
    data = {
        "at": {
            "isAtAll": False
        },
        "text": {
            "content": msg
        },
        "msgtype": "text"
    }

    return requests.post(url=url, data=json.dumps(data), headers=headers).text


def sign():
    time.sleep(2)
    location_kq = pyautogui.locateOnScreen('kq.png')  # 寻找刚才保存考勤图片
    center_kq = pyautogui.center(location_kq)  # 寻找图片的中心
    pyautogui.click(center_kq)

    time.sleep(10)
    location_dk = pyautogui.locateOnScreen('dk.png')  # 寻找刚才保存打卡图片
    center_dk = pyautogui.center(location_dk)  # 寻找图片的中心
    pyautogui.click(center_dk)


def wait(t):
    random_value = random.randint(1, t)
    minute = random_value % 3600 / 60
    second = random_value % 3600 % 60
    print(f"将于{int(minute)}分{int(second)}秒后开始打卡")


localtime = time.localtime(time.time())
if is_holiday(datetime(localtime.tm_year, localtime.tm_mon, localtime.tm_mday)):
    send("今天放假")
elif pyautogui.locateOnScreen('kq.png'):
    wait(9)
    Path = r'D:\Program Files\MuMu\emulator\nemu\EmulatorShell\NemuPlayer.exe'
    os.startfile(Path)
    sign()  # 调用打卡函数
    if pyautogui.locateOnScreen('success.png'):
        send("打卡成功")
    else:
        send("打开失败")
else:
    send("打卡失败")
