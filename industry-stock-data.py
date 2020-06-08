import requests
from fake_useragent import UserAgent
import json
import re
import pymysql


def getData():
    ajaxUrl = 'http://75.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112403557064424984069_1591522896063&pn=1&pz=100&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:2+f:!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f222&_=1591522896064'
    rep = requests.get(ajaxUrl, headers={
        'User-Agent': UserAgent(verify_ssl=False).random,
    })
    return rep.text


def saveToDB():
    # 连接数据库
    config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "stock"
    }
    db = pymysql.connect(**config)
    cur = db.cursor()
    # 创建表格
    createDBTable(db, cur)
    # 插入数据
    insertData(db, cur, data)

# 创建数据库
def createDBTable(db, cur):
    try:
        cur.execute('use stock;')
        createSql = "create table industry0608(id int, 板块名称 char(30), 涨跌幅 float, 最新价 float, 上涨家数 int, 下跌家数 int, 领涨股票 char(50), 领涨涨跌幅 float)"
        cur.execute(createSql)
    except Exception as e:
        raise e

# 插入数据
def insertData(db, cur, data):
    try:
        for item in data:
            industryName = item['f14']
            upRate = item['f3']
            downRate = item['f2']
            upNum = item['f104']
            downNum = item['f105']
            topStockName = item['f128']
            topRate = item['f136']
            print(industryName, type(industryName), upRate, type(upRate), downRate, type(downRate), upNum, type(upNum), downNum, type(downNum), topStockName, type(topStockName), topRate, type(topRate))
            # insertSql = 'insert into industry0607(id, 板块名称, 涨跌幅, 最新价, 上涨家数, 下跌家数, 领涨股票, 领涨涨跌幅) values(0,' + industryName + ',' + upRate + ',' + downRate + ',' + upNum + ',' + downNum + ',' + topStockName + ',' + topRate + ')'
            # 另一种替换变量的方式 "UPDATE %s set %s='%s',ID='%s' where ID='%s'"%(mtype,attribute,value,ID,ID)
            # 注：字符串类型需要加引号
            insertSql = "insert into industry0607(id, 板块名称, 涨跌幅, 最新价, 上涨家数, 下跌家数, 领涨股票, 领涨涨跌幅) values(0, '{industryName}', {upRate}, {downRate}, {upNum}, {downNum}, '{topStockName}', {topRate})".format(industryName=industryName, upRate=upRate, downRate=downRate, upNum=upNum, downNum=downNum, topStockName=topStockName, topRate=topRate)
            cur.execute(insertSql)
            db.commit()
    except Exception as e:
        raise e
    finally:
        cur.close()
        db.close()


if __name__ == '__main__':
    response = getData()
    reg = r'jQuery112403557064424984069_1591522896063\((.*)\);'
    result = re.findall(reg, response)
    jsonData = json.loads(result[0])
    data = jsonData['data']['diff']
    print('长度：', data, len(data))
    saveToDB()
    # print('data3-------------------------:\n', data)