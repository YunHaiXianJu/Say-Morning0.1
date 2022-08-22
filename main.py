from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

#日期
today = datetime.now()

start_date = '2022-01-01'

#城市
city = '云浮'

#生日
birthday = '07-27'

#测试号ID
app_id = 'wxc9bd43a2be1e0d7a'

#测试号secret
app_secret = 'e6d9ee543afb468a62ee44f67704dc71'

#用户ID
user_id = 'oqkP86rWeqGjZhms2WdX1TUx7uhk'

#模板ID
template_id = 'bZG2knv3-RVTXk6Z-_7nf9LtkzrKh7UpDPKsw0bBr2Q'

#获取天气
def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

#
def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

#获取生日
def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
