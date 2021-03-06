import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pymysql


def getHtml(url):
    res = requests.get(url, headers={
        'User-Agent': UserAgent(verify_ssl=False).random
    })
    res.encoding = res.apparent_encoding
    return res.text


def getIndustryLink(content):
    soup = BeautifulSoup(content, 'html.parser')
    aTag = soup.find_all('div', 'cate_items')
    industry_list = []
    for item in aTag:
        links = item.find_all('a')
        for link in links:
            industry_list += [(link.contents[0], link.get('href'))]
    return industry_list


def saveData(data):
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
                CREATE TABLE STOCK_INDUSTRY(
                    id char(10) NOT NULL PRIMARY KEY ,
                    行业名称 char(50) NOT NULL DEFAULT '--',
                    页面链接 char(150) NOT NULL DEFAULT '--'
                )
                '''
    try:
        cur.execute(create_sql)
        index = 0
        for industry, link in data:
            insert_sql = '''
                        INSERT INTO STOCK_INDUSTRY (id,行业名称,页面链接)
                                    VALUES (%s,%s,%s)
                    '''
            cur.execute(insert_sql, (index, industry, link))
            index += 1
        db.commit()
    except Exception as e:
        raise e
    finally:
        cur.close()
        db.close()


if __name__ == '__main__':
    # 获取页面html
    url = 'http://q.10jqka.com.cn/thshy/'
    htmlContent = getHtml(url)
    # 获取页面里的连接
    linkList = getIndustryLink(htmlContent)
    # 连接数据库存储数据
    saveData(linkList)
    print('res.text', linkList)