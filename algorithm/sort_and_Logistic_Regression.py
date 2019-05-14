import KNN as kNN
import numpy as np
import sys
sys.path.append('../traindata/')
import manreplite as getlocal
import pymysql
import re
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

def sql_select(arrayLable):
    for lable in arrayLable:
        sql = 'select * from finfo where '
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
                        whereheight += 'height>18 and height<%s' % res[1]
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
            print(results[0])
        else:
            print('Empty')

def main():
    dataSet, lable = kNN.dataSetAnalyse('../testdata/dataSet.txt')
    stdDataSet, averageVals, ranges = kNN.standardization(dataSet)
    lng, lat = getlocal.getLocation_json('广东')
    nyarry = np.array([0, 160.0, 1.0, 10000.0, lng, lat, 27])
    testArray = (nyarry - averageVals) / ranges
    arrayLable = kNN.kNN(testArray, stdDataSet, lable, 3)
    print(arrayLable)
    sql_select(arrayLable)

if __name__ == "__main__":
    main()
    # dataSet, lable = kNN.dataSetAnalyse('../testdata/dataSetTest.txt')
    # std_dataset, min_values, range_values = kNN.autNorm_mat(dataSet)
    # lng, lat = getlocal.getLocation_json('新疆')
    # nyarry = np.array([1, 169.0, 1.0, 3500.0, lng, lat, 23])
    # testArray = (nyarry - min_values) / range_values
    # arrayLable = kNN.kNN(testArray, std_dataset, lable, 3)
    # print(arrayLable)