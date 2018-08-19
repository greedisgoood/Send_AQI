
# coding: utf-8

# In[ ]:


###AQI###
import requests
from bs4 import BeautifulSoup
import re
from wxpy import *
import time


# 初始化机器人，扫码登陆
bot = Bot(cache_path=True, console_qr=False)

def getAQI():
    url = "https://air-quality.com/place/china/cangzhoushihuanbaoju/f5e8fd68?lang=zh-Hans&standard=aqi_us"
    r = requests.get(url)
    #print (r.text)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    #print (soup)

    city = "沧州市环保局"  # 城市名称
    aqi = soup.find('div', {'class', "indexValue"})  # AQI指数
    aqi = re.findall(r"\d+\.?\d*", aqi.string)
    quality = soup.find('div', {'class', "level"})  # 空气质量等级
    quality = re.findall(u"[\u4e00-\u9fa5]+", quality.string)
    result1 = soup.find("div", class_='value')  # 空气质量pm2.5描述
    result1 = re.findall(r"\d+\.?\d*", result1.string)
    result2 = soup.find_all(
        "div",
        class_='value',
    )  # 空气质量pm10描述
    result2 = re.findall(r"\d+\.?\d*", result2[1].string)
    result = time.strftime(
        "%Y-%m-%d %H:%M", time.localtime()
    ) + ' ' + city + '\n' + '空气质量等级为—' + quality[0] + '\n' + 'AQI指数—' + aqi[0] + '\n' + ' 空气质量pm2.5—' + result1[0] + '\n' + ' 空气质量pm10—' + result2[0]
    result = str(result)
    #return result
    print(result)
    
    # 机器人账号自身
    myself = bot.self
    
#     #向唐朝挂面发送result
#     friend = bot.friends().search('唐朝挂面')[0]
#     friend.send(result)
    
   
    # 向文件传输助手发送消息
    bot.file_helper.send(result)
    
    # 向测试群发送消息
    group = ensure_one(bot.groups().search('沧州北航项目'))
    group.send(result)

#getAQI()


#
# 开始后台监测
def sleeptime(hour, min, sec):
    return hour * 3600 + min * 60 + sec
second1 = sleeptime(2, 30, 20)
second2 = sleeptime(0, 20, 20)
while 1 == 1:
    time.sleep(second2)
    bot.file_helper.send(time.strftime("%Y-%m-%d %H:%M", time.localtime())+' '+'alive')
    while 1 == 1:
        time.sleep(second1)
        getAQI()

        print('do action')
    #这是隔20秒执行一次
sleeptime(0, 30, 10)
bot.join()

