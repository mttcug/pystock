import pymysql
import requests

def getIndustry():
    db = pymysql.connect(host="localhost", user="root", password="", database="stock")
    cur = db.cursor()
    cur.execute("use stock;")
    cur.execute("select * from stock_industry;")
    result = cur.fetchall()
    cur.close()
    db.close()
    return result


def getTop10(id, url):
    url = url.replace("detail", "detail/field/3475914/order/desc/page/1/ajax/1")
    print(url)
    content = requests.get(url)
    return content


if __name__ == "__main__":
    industrys = getIndustry()
    for industry in industrys:
        lists = getTop10(industry[0], industry[2])