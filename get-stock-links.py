import requests
from fake_useragent import UserAgent
import re
import xlwt
import xlrd


def getHtml(url):
    r = requests.get(url, headers={
        'User-Agent': UserAgent(verify_ssl=False).random,
    })
    r.encoding = r.apparent_encoding
    return r.text


def getContent(html):
    regex = r'<a.*? href="(.*?)" .*?>([\u4e00-\u9fa5]+)<\/a>'
    targetContent = re.findall(regex, html)
    return targetContent


def saveToExcel(data):
    listD = list(data)
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('stock-link', cell_overwrite_ok=True)
    for rowIndex, rowData in enumerate(listD):
        sheet.write(rowIndex, 0, rowData[1])
        sheet.write(rowIndex, 1, rowData[0])
    workbook.save('stockLink.xls')


# def getExcelData():
#     data = xlrd.open_workbook('stockLink.xls')
#     sheet = data.sheet_by_name('stock-link')
#     for row in range(sheet.nrows):
#         if row[0] == '':
#             print('row[1]:', row[1])


stockurl = 'http://quote.eastmoney.com/stocklist.html'
if __name__ == '__main__':
    html = getHtml(stockurl)
    # print('html:', html)
    content = getContent(html)
    saveToExcel(content)
    print('content:', content)
