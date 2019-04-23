# http://search.jiayuan.com/v2/search_v2.php?key=&sex=f&stc=23:1&sn=default&sv=1&f=select
import requests
import urllib.parse
import urllib.request
import json
import re
import pymysql
import time
import random
# import queue
# import thread

def fetchUrl(url, headers, formdata):
    try:
        data = urllib.parse.urlencode(formdata).encode('utf-8')
        request = urllib.request.Request(url, data=data, headers=headers)
        response = urllib.request.urlopen(request)
        js = response.read().decode('unicode_escape')
        js = js.replace("##jiayser##", "").replace("//", "").replace("\/", "/")
        return js
    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error !")

def parserhtml(html, db):
    try:
        cursor = db.cursor()
        res = json.loads(html)
        pat = re.compile('>(.*?)<')
        ranTagNationality = ''
        ranTaglistNationality = ''
        Nationality = ''
        for key in res['userInfo']:
            reslist = []
            uid = key['uid']
            nickname = key['nickname']
            sex = key['sex']
            age = key['age']
            work_location = key['work_location']
            height = key['height']
            education = key['education']
            marriage = key['marriage']
            income = key['income']
            count = key['count']
            ranTag = pat.findall(key['randTag'])
            for temp in ranTag:
                if '族' in str(temp):
                    ranTagNationality = temp
            ranTaglist = pat.findall(key['randListTag'])
            for temp2 in ranTaglist:
                if '族' in str(temp2):
                    ranTaglistNationality = temp2
            if ranTagNationality == '' and ranTaglistNationality == '':
                Nationality = '汉族'
            elif ranTaglistNationality == '':
                Nationality = ranTagNationality
            elif ranTagNationality == '':
                Nationality = ranTaglistNationality
            else:
                Nationality = ranTaglistNationality
            image = key['image']
            if image:
                haveimage = 1
            else:
                haveimage = 0
            shortnote = key['shortnote']
            matchCondition = key['matchCondition']
            sql = "insert into finfo(uid, nickname, sex, age, edu, height, location, marrige, nationality, matchCondition, haveimage, image, shortnote) values " \
                  "(%s, '%s', '%s', %s,'%s', %s, '%s','%s', '%s', '%s', %s, '%s', '%s')" % (
                  uid, nickname, sex, age, education, height, work_location, marriage, Nationality, matchCondition,
                  haveimage, image, shortnote)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
    except:
        print(html)
def main(url, header, formdata, db):
    html = fetchUrl(url, header, formdata)
    parserhtml(html, db)