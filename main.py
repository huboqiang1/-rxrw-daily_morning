from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import re
import json

today = datetime.now()
start_date = os.environ['START_DATE']
together_date = os.environ['TOGETHER_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
birthday_man = os.environ['BIRTHDAY_MAN']
betrothal = os.environ['BETROTHAL']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_id2 = os.environ["USER_ID2"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://api.yytianqi.com/observe?city=CH190101&key=9lvtgv9cv3kpd46p"
  res = requests.get(url).json
  res.replace('/'','/"')
  print(type(res))
  print(res)
  print(res['data'])
  print(res['data']['tq'])
  print(res['data']['qw'])
  weather = res['data']['tq']
  return weather['weather'], math.floow(int(res['data']['qw']))

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_together():
  delta = today - datetime.strptime(together_date, "%Y-%m-%d")
  return delta.days

def get_weekday():
  week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
  return week_list[today.weekday()]

def get_birthday():
#   next = datetime.strptime(str(date.today().year) + "-" + birthday_man, "%Y-%m-%d")
#   if next < datetime.now():
#     next = next.replace(year=next.year + 1)
#   return (next - today).days
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  next = str(next.year) + "-" + birthday
  
  splits = re.split(r'[-.s+/]', next)  
  splits = [s for s in splits if s]
  if len(splits) < 3:
    raise ValueError('输入格式不正确， 至少包括年月日')
     
  splits = splits[:3]  # 只截取年月日
  birthday1 = datetime.strptime('-'.join(splits), '%Y-%m-%d')
  tod = date.today()
  delta = birthday1.date() - tod
  return delta.days

def get_betrothal():
  next = datetime.strptime(str(date.today().year) + "-" + betrothal, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  next = str(next.year) + "-" + betrothal
  
  splits = re.split(r'[-.s+/]', next)  
  splits = [s for s in splits if s]
  if len(splits) < 3:
    raise ValueError('输入格式不正确， 至少包括年月日')
     
  splits = splits[:3]  # 只截取年月日
  betrothal1 = datetime.strptime('-'.join(splits), '%Y-%m-%d')
  tod = date.today()
  delta = betrothal1.date() - tod
  return delta.days

def get_birthday_man():
  next = datetime.strptime(str(date.today().year) + "-" + birthday_man, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
#   return (next.day - today.day).days
  next = str(next.year) + "-" + birthday_man
  
  splits = re.split(r'[-.s+/]', next)  
  splits = [s for s in splits if s]
  if len(splits) < 3:
    raise ValueError('输入格式不正确， 至少包括年月日')
     
  splits = splits[:3]  # 只截取年月日
  birthday1 = datetime.strptime('-'.join(splits), '%Y-%m-%d')
  tod = date.today()
  delta = birthday1.date() - tod
  return delta.days

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
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"together_days":{"value":get_together()},"birthday_left":{"value":get_birthday()},"birthday_right":{"value":get_birthday_man()},"words":{"value":get_words(), "color":get_random_color()}, "betrothal":{"value":get_betrothal()}, "isWeekDay":{"value":get_weekday()}}
res = wm.send_template(user_id, template_id, data)
wm.send_template(user_id2, template_id, data)
print(res)
