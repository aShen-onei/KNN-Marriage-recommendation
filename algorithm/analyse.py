import KNN as kNN
import numpy as np
import sys
import pymysql
import re
import requests
import json
import random
import LR_SORT as lr
sys.path.append('../traindata/')
import manreplite as getlocal
"""
filename = '../testdata/dataSet.txt'
filename2 = '../testdata/dataSetTest.txt'
sql = 'select * from finfo where ()'
"""
def select_data(sql):
    print(sql)
    result = []
    try:
        pysql = pymysql.connect("localhost", "root", "LZ6=0*9RuWKd", "graduateprojecttest")
        cursor = pysql.cursor()
        cursor.execute(sql)
        alldata = cursor.fetchall()
        for res in alldata:
            result.append(res)
    except Exception as e:
        print('error message:%s' % e)
    finally:
        cursor.close()
        pysql.close()
    return result

def sql_slectAll():
    sql = 'select distinct * from finfo order by rand() limit 500'
    res = select_data(sql)
    return res
def sql_select(arrayLable):
    for lable in arrayLable:
        sql = 'select distinct * from finfo where '
        whereage = ''
        whereheight = ''
        whereimage = ''
        whereedu = ''
        wheremarrige = ''
        wherenation = ''
        wherelocation = ''
        lable_group = lable.split(',')
        for item in lable_group:
            if '岁' in item:
                res = re.findall(r"\d+\.?\d*", item)
                if '不限' in item:
                    if res[0].isdigit():
                        whereage += 'age>%s' % res[0]
                    else:
                        whereage += 'age>18 and age<%s' % res[1]
                else:
                    whereage += 'age>%s and age<%s' % (res[0], res[1])
                sql += whereage
            elif 'cm' in item:
                res = re.findall(r"\d+\.?\d*", item)
                if '不限' in item:
                    if res[0].isdigit():
                        whereheight += 'height>%s' % res[0]
                    else:
                        whereheight += 'height>140 and height<%s' % res[1]
                else:
                    whereheight += 'height>%s and height<%s' % (res[0], res[1])
                if whereage:
                    sql += ' and '+whereheight
                else:
                    sql += whereheight
            elif '有照片' == item:
                whereimage = 'haveimage=1'
                if whereage or whereheight:
                    sql += ' and '+whereimage
                else:
                    sql+=whereimage
            elif '高中中专及以下' in item or '大专' in item or '本科' in item or '双学士'in item or '硕士' in item or '博士' in item:
                whereedu = 'edu = \'%s\'' % item
                if (whereage or whereheight) or whereimage:
                    sql+=' and '+whereedu
                else:
                    sql+=whereedu
            elif '未婚' in item or '离异' in item or '丧偶' in item:
                wheremarrige = 'marrige = \'%s\'' % item
                if ((whereage or whereheight) or whereimage) or whereedu:
                    sql+=' and '+wheremarrige
                else:
                    sql+=wheremarrige
            elif item == '':
                continue
            elif '族' in item:
                wherenation = 'nationality=\'%s\'' % item
                if (((whereage or whereheight) or whereimage) or whereedu)or wheremarrige:
                    sql+=' and '+wherenation
                else:
                    sql+=wherenation

            else:
                wherelocation = 'location = \'%s\'' % item
        if (((whereage or whereheight) or whereimage) or whereedu) or wheremarrige:
            if wherelocation:
                sql+=' and '+wherelocation
        else:
            sql+=wherenation
        results = select_data(sql)
        if results:
            return results
            break
        else:
            print('Empty')

# 分化区间[-1,1]测试
'''
区间分化[-1,1]精确度不高

def main():
    dataSet, lable = kNN.dataSetAnalyse('../testdata/dataSet.txt')
    stdDataSet, averageVals, ranges = kNN.standardization(dataSet)
    lng, lat = getlocal.getLocation_json('安徽')
    nyarry = np.array([0, 160.0, 1.0, 10000.0, lng, lat, 27])
    testArray = (nyarry - averageVals) / ranges
    arrayLable = kNN.kNN(testArray, stdDataSet, lable, 3)
    print(arrayLable)
    sql_select(arrayLable)
'''
def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = 'qGp3Vuokj7oBIbLK3rCd9vZWkx1CHjMT'
    uri = url + '?' + 'address=' + address  + '&output=' + output + '&ak=' + ak
    try:
        res = requests.get(uri)
        res.raise_for_status()
        res.encoding = 'unicode_escape'
        temp = json.loads(res.text)
        lng = temp['result']['location']['lng']
        lat = temp['result']['location']['lat']
        return lng, lat
    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error !")

def analyse(result, array):
    # array = [1, 169.0, 1.0, 3500.0, lng, lat, 23]
    age = array[6]
    height = array[1]
    education = array[2]
    marriage = array[0]
    lng = array[4]
    lat = array[5]
    std_age = 1
    std_height = 1
    std_edu = 1
    std_marriage = 1
    std_area = 1
    res = result.split(',')
    for item in res:
        if '岁' in item:
            res = re.findall(r"\d+\.?\d*", item)
            if '不限' in item:
                if res[0].isdigit():
                    if array[6] > int(res[0]):
                        age = array[6]
                        std_age = 1
                    else:
                        age = int(res[0])
                        std_age = 0
                else:
                    if array[6] < int(res[0]):
                        age = array[6]
                        std_age = 1
                    else:
                        age = int(res[0])
                        std_age = 0
            else:
                if array[6] > int(res[0]) and array[6] < int(res[1]):
                    age = array[6]
                    std_age = 1
                else:
                    age = (int(res[0]) + int(res[1])) / 2
                    std_age = 0
        elif 'cm' in item:
            res = re.findall(r"\d+\.?\d*", item)
            if '不限' in item:
                if res[0].isdigit():
                    if array[1] > int(res[0]):
                        height = array[1]
                        std_height = 1
                    else:
                        height = int(res[0])
                        std_height = 0
                else:
                    if array[1] < int(res[0]):
                        height = array[1]
                        std_height = 1
                    else:
                        height = int(res[0])
                        std_height = 0
            else:
                if array[1] > int(res[0]) and array[1] < int(res[0]):
                    height = array[1]
                    std_height = 1
                else:
                    height = (int(res[0]) + int(res[1])) / 2
                    std_height = 0
        elif '有照片' == item:
            continue
        elif '高中中专及以下' in item or '大专' in item or '本科' in item or '双学士' in item or '硕士' in item or '博士' in item:
            edu = getlocal.edu(item)
            if array[2] > edu:
                education = array[2]
                std_edu = 1
            else:
                education = edu
                std_edu = 0
        elif '未婚' in item or '离异' in item or '丧偶' in item:
            ma = getlocal.marrige(item)
            if array[0] == ma:
                marriage = array[0]
                std_marriage = 1
            else:
                if ma == None:
                    marriage = array[0]
                else:
                    marriage = ma
                std_marriage = 0
        elif item == '':
            continue
        elif '族' in item:
            continue
        else:
            try:
                print(item)
                lng, lat = getlnglat(item)
                if abs(lng - array[4]) < 14 and abs(lat - array[5]) < 10:
                    std_area = 1
                else:
                    std_area = 0
            except Exception as e:
                lng = lat =0
                print(e)

    std_point = (std_area+std_marriage+std_edu+std_height+std_age)/5
    if std_point>0.5:
        return [age, height, education, marriage, lng, lat, 1]
    else:
        return [age, height, education, marriage, lng, lat, 0]
def wrTrainText(result, array):
    fr = open('../train/logisticTrain.txt', 'w', encoding='utf-8')
    for res in result:
        data = analyse(res[9], array)
        fr.write(str(data[0])+'\t'+str(data[1])+'\t'+str(data[2])+'\t'+str(data[3])+'\t'+str(data[4])+'\t'+str(data[5])+'\t'+str(data[6])+'\n')
        # fr.write(str(res[0]) + '\t' + str(res[1]) + '\t' + str(res[2]) + '\t' + str(res[3]) + '\t' + str(res[4]) + '\t' + str(res[5]) + '\t' + str(res[6]) + '\t' + str(res[7]) + '\n')
    # return result
def wrTestText(result, array):
    fr = open('../testdata/logisticTest.txt', 'w', encoding='utf-8')
    for res in result:
        data = analyse(res[9], array)
        fr.write(str(data[0])+'\t'+str(data[1])+'\t'+str(data[2])+'\t'+str(data[3])+'\t'+str(data[4])+'\t'+str(data[5])+'\t'+str(data[6])+'\n')
def analyse_result(res):
    age = 0
    height = 0
    edu = 0
    for item in res:
        if item.isdigit():

def rightpercent(result, std)
    fr = open('recommend.txt', 'w', encoding='utf-8')
    sum = len(result)
    for res in result:
        fr.write(res)
        array = analyse_result(res)
if __name__ == "__main__":
    # main()
    dataSet, lable = kNN.dataSetAnalyse('../testdata/dataSetTest.txt')
    std_dataset, min_values, range_values = kNN.autNorm_mat(dataSet)
    lng, lat = getlocal.getLocation_json('贵阳')
    array = [1, 170.0, 3.0, 3500.0, lng, lat, 23]
    std_girl = ['18-22岁,155-170cm,贵阳']
    nyarry = np.array(array)
    testArray = (nyarry - min_values) / range_values
    arrayLable = kNN.kNN(testArray, std_dataset, lable, 3)
    print(arrayLable)
    result = sql_select(arrayLable)
    print(result)
    all_result = sql_slectAll()
    wrTrainText(all_result, array)
    wrTestText(result, array)
    index = lr.main()
    new_order = []
    for i in range(0, index.__len__())[::-1]:
        new_order.append(result[index[i]])

