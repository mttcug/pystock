import pymysql
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

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
    resp = requests.get(url, headers={
        'User-Agent': UserAgent(verify_ssl=False).random,
    })
    resp.encoding = "utf-8"
    content = resp.text
    print("################:", url, resp.text)
    # soup = BeautifulSoup(content, "html.parser")
    # code = soup.find_all("tr")
    # print("_______________code:", code)
    return content


if __name__ == "__main__":
    industrys = getIndustry()
    for industry in industrys:
        lists = getTop10(industry[0], industry[2])