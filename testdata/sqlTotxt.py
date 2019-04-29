import pymysql

def select_data(sql):
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

def get_result(sql, filename):
    print(sql)
    results = select_data(sql)
    fr = open('dataSet.txt', 'w', encoding='utf-8')
    for res in results:
        fr.write(str(res[0])+'\t'+str(res[1])+'\t'+str(res[2])+'\t'+str(res[3])+'\t'+str(res[4])+'\t'+str(res[5])+'\t'+str(res[6])+'\t'+str(res[7])+'\n')
    return results

if __name__ == '__main__':
    sql = "select * from mfinfo"
    res = get_result(sql, 'dataSet.txt')

