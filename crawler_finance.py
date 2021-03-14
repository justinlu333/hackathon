import re
import requests

from bs4 import BeautifulSoup
from lxml import etree
 

headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

url = "http://quotes.money.163.com/f10/zycwzb_601318.html"
 

response = requests.get(url, headers=headers, verify=False)

html = etree.HTML(response.content.decode('utf-8'))

# 解析table 表头
table = html.xpath('//table[@class="table_bg001 border_box limit_sale"]//tr')
for i in table:
    p = ''.join(i.xpath(".//td//text()")) 
    print(p)


# 解析table 数据
table = html.xpath('//table[@class="table_bg001 border_box limit_sale scr_table"]//tr')
for i in table:
    tdlist = i.xpath(".//td//text()")
    for str in tdlist:
        print(str)
