# http://search.jiayuan.com/v2/search_v2.php?key=&sex=f&stc=23:1&sn=default&sv=1&f=select
import requests
import urllib.parse
import urllib.request
import json
import re
from lxml import etree
import pymysql
import time
import random
# import queue
# import thread

def fetchUrl(url, headers):
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        res.encoding = 'unicode_escape'
        return res.text
    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error !")

def parserhtml(html, db):
    error = ''
    try:
        cursor = db.cursor()
        res = json.loads(html)
        for key in res['userInfo']:
            uid = key['realUid']
            income = salary(uid)
            age = key['age']
            work_location = key['work_location']
            error = work_location
            lng, lat = getLocation_json(work_location)
            height = key['height']
            education = key['education']
            edunum = edu(education)
            marriage1 = key['marriage']
            mnum = marrige(marriage1)
            matchCondition = key['matchCondition']
            sql = "insert into mfinfo(marrige, height, edu,income,lng,lat, age,matchC) values " \
                  "(%s, %s,%s,%s,%s,%s,%s,'%s')" % (mnum, height, edunum, income, lng, lat, age, matchCondition)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
    except:
        print('error')
        print(error)

def marrige(marrige):
    if(marrige == '未婚'):
        m = 1
        return m
    elif(marrige == '离异'):
        m = 0
        return m
    elif(marrige == '丧偶'):
        m = -1
        return m

def edu(education):
    if(education  == '高中中专及以下'):
        e = 1
        return e
    elif(education == '大专'):
        e = 2
        return e
    elif(education == '本科'):
        e = 3
        return e
    elif(education == '双学士'):
        e = 4
        return e
    elif(education == '硕士'):
        e = 5
        return e
    elif(education == '博士'):
        e = 6
        return e
    else:
        e = 0
        return e

def salary(uid):
    uidurl = 'http://www.jiayuan.com/%s?fxly=pmtq-ss-210&pv.mark=s_p_c|%s|205197176' % (uid, uid)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'Cookie':'accessID=20190422214243813520; ip_loc=21; save_jy_login_name=13516502945; stadate1=204197176; myloc=44%7C4406; myage=21; mysex=m; myuid=204197176; myincome=30; upt=ESWqVcKkGvmV0xxJXvgGVspRiT0JdSRo9bFGVLsnYbvkBx2Mr6tczPld38b7pZUoNFoAAHYYBpaixqbrZkU8Wc8.; user_attr=000000; skhistory_m=a%3A1%3A%7Bi%3A1556092333%3Bs%3A6%3A%22%E7%9C%89%E5%B1%B1%22%3B%7D; PHPSESSID=23cc8fc1d9f2bd5212c69f1b05a27530; SESSION_HASH=9c64eef5469e641d0e01caa7c7d66b0944e28554; jy_refer=sp0.baidu.com; FROM_BD_WD=%25E4%25B8%2596%25E7%25BA%25AA%25E4%25BD%25B3%25E7%25BC%2598; FROM_ST_ID=1764229; FROM_ST=.jiayuan.com; user_access=1; COMMON_HASH=1b86e07a17d23836a9aff7c4e2d76b8d; sl_jumper=%26cou%3D17%26omsg%3D0%26dia%3D0%26lst%3D2019-04-24; last_login_time=1556154167; PROFILE=205197176%3AaShenone%3Am%3Aimages1.jyimg.com%2Fw4%2Fglobal%2Fi%3A0%3A%3A1%3Azwzp_m.jpg%3A1%3A1%3A50%3A10%3A3.0; main_search:205197176=%7C%7C%7C00; pop_avatar=1; RAW_HASH=8aGHZG5cAyMCZYvcvqvE9L76RCENW1WxzTx66iX-Vo35475Zlmv3XGMumgVkDggmj4euT3h8M18qtkYNX5wZmfi-UY-Yl81lJKvziUcl91Fpn8g.; pop_time=1556155290740'
    }
    r = requests.get(uidurl, headers=header).text
    html = etree.HTML(r)
    income = html.xpath('//ul[@class="member_info_list fn-clear"]/li[4]/div[@class="fl pr"]/em/text()')
    res = re.findall(r"\d+\.?\d*", income[0])
    if(len(res) == 1):
        sum = int(res[0])
    else:
        sum1 = int(res[0])
        sum2 = int(res[1])
        sum = (sum1 + sum2) / 2
    return sum

def getLocation_json(addr):
    if(addr == '喀什'):
        addr = '新疆喀什'
    elif(addr == '西安'):
        addr ='山西西安'
    elif(addr == '香港'):
        addr='中国香港'
    elif(addr == '澳门'):
        addr = '中国澳门'
    elif(addr == '普陀'):
        addr = '上海'
    url1 = 'http://api.map.baidu.com/geocoder?address=%s&output=json&key=f247cdb592eb43ebac6ccd27f796e2d2' % addr
    html = requests.get(url1)
    hjson =json.loads(html.text) #转化为dict类型
    lng = hjson['result']['location']['lng'] # 经度
    lat = hjson['result']['location']['lat'] # 纬度
    return lng, lat

def main(url, header, db):
    html = fetchUrl(url, header)
    parserhtml(html, db)

if __name__ == '__main__':
    db = pymysql.connect("localhost", "root", "LZ6=0*9RuWKd", "graduateprojecttest")
    stc = [
        "2:18.24,23:1",
        "2:25.30,23:1",
        "2:31.36,23:1",
        "2:37.42,23:1",
        "2:43.48,23:1",
        "2:49.54,23:1",
        "2:55.60,23:1",
        "2:61,66,23:1",
        "2:67,70,23:1",
    ]
    us = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"]

    headers = {
        'User-Agent':random.choice(us),
        'Cookie':'guider_quick_search=on; is_searchv2=1; accessID=20190422214243813520; save_jy_login_name=13516502945; stadate1=204197176; myloc=44%7C4406; myage=21; mysex=m; myuid=204197176; myincome=30; upt=ESWqVcKkGvmV0xxJXvgGVspRiT0JdSRo9bFGVLsnYbvkBx2Mr6tczPld38b7pZUoNFoAAHYYBpaixqbrZkU8Wc8.; user_attr=000000; skhistory_m=a%3A1%3A%7Bi%3A1556092333%3Bs%3A6%3A%22%E7%9C%89%E5%B1%B1%22%3B%7D; SESSION_HASH=9c64eef5469e641d0e01caa7c7d66b0944e28554; jy_refer=sp0.baidu.com; FROM_BD_WD=%25E4%25B8%2596%25E7%25BA%25AA%25E4%25BD%25B3%25E7%25BC%2598; FROM_ST_ID=1764229; FROM_ST=.jiayuan.com; user_access=1; PHPSESSID=598890ed90bbbb0f326b5c703e8e9611; COMMON_HASH=1b86e07a17d23836a9aff7c4e2d76b8d; sl_jumper=%26cou%3D17%26omsg%3D0%26dia%3D0%26lst%3D2019-04-24; last_login_time=1556154167; PROFILE=205197176%3AaShenone%3Am%3Aimages1.jyimg.com%2Fw4%2Fglobal%2Fi%3A0%3A%3A1%3Azwzp_m.jpg%3A1%3A1%3A50%3A10%3A3.0; main_search:205197176=%7C%7C%7C00; pop_avatar=1; RAW_HASH=8aGHZG5cAyMCZYvcvqvE9L76RCENW1WxzTx66iX-Vo35475Zlmv3XGMumgVkDggmj4euT3h8M18qtkYNX5wZmfi-UY-Yl81lJKvziUcl91Fpn8g.'
    }
    for stcdata in stc:
        for page in range(1, 101):
            print('第%s次爬取' % page)
            url = 'http://search.jiayuan.com/v2/search_v2.php?key=&sex=m&stc=%s&sn=default&sv=1&p=%s&f=select' % (stcdata, page)
            main(url, headers, db)
            if page % 10 == 0:
                time.sleep(3)
    db.close()