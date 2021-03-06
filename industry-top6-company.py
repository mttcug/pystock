import requests
from fake_useragent import UserAgent
import re
import json
import pymysql


def getLinks(url):
    resp = requests.get(url, headers={
        'User-Agent': UserAgent(verify_ssl=False).random
    })
    resp.encoding = resp.apparent_encoding
    content = resp.text

    # 匹配出想要的数据
    reg = r'jQuery112403557064424984069_1591522896063\((.*)\);'
    result = re.findall(reg, content)
    jsonData = json.loads(result[0])
    data = jsonData['data']['diff']
    # print('data----\n\n', data)

    # 根据接口数据拼接得到url
    lists = []
    for item in data:
        industry = item['f14']
        prepart = item['f13']
        sufpart = item['f12']
        link = 'quote.eastmoney.com/unify/r/{prepart}.{sufpart}'.format(prepart=prepart, sufpart=sufpart)
        linkData = (industry, link)
        lists.append(linkData)
    return lists


def saveToDB(data):
    items = list(data)
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'stock'
    }
    db = pymysql.connect(**config)
    cur = db.cursor()
    cur.execute('use stock;')
    create_sql = '''
                CREATE TABLE INDUSTRY(
                    id char(10),
                    行业名称 char(50),
                    页面链接 char(150)
                )
                '''
    try:
        cur.execute(create_sql)
        index = 0
        for industry, link in items:
            print('industry:', industry, 'link:', link)
            insert_sql = '''
                        INSERT INTO INDUSTRY (
                        id,
                        行业名称,
                        页面链接
                        )
                        VALUES (
                            %s,
                            %s,
                            %s
                        )
                        '''
            cur.execute(insert_sql, (index, industry, link))
            db.commit()
            index = index + 1
    except Exception as e:
        print('e:----', e)
        raise e
    finally:
        cur.close()
        db.close()


if __name__ == '__main__':
    url = 'http://75.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112403557064424984069_1591522896063&pn=1&pz=100&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:2+f:!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f222&_=1591522896064'
    links = getLinks(url)
    saveToDB(links)