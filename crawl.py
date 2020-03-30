import requests
from bs4 import BeautifulSoup
import re

#txt파일로 저장
def save(out, goods):
    for name, price in goods:

        out.write(name)
        out.write('\t')
        out.write(price)
        out.write('\n')

url = "https://search.shopping.naver.com/search/all.nhn"

#GET 파라미터들
params = {"pagingIndex" : "1", "pagingSize" : "80", "viewType" : 'list', "sort" : "rel" , "frm" : "NVSHPAG", "query" : ""}

product_name = "KM-037"

params["query"] = product_name

out = open("output.txt", "w", -1, "utf-8")

page = 1
while True:
    res = requests.get(url, params=params)

    html = res.text

    soup = BeautifulSoup(html, 'html.parser')

    if soup("div[class-search_none]"):
        break

    #제품리스트 추출
    list = soup.select('ul[class=goods_list]')[0]

    #제목 추출
    goods = []
    for title in list.select('div[class=tit]>a'):
        goods.append([title.text.replace('\n', ''), ''])

    #가격 추출
    i = 0
    for price in list.select('span[class=price]>em'):

        for temp in re.findall("\d+", price.text):#숫자만 추출
            goods[i][1] += temp

        i+=1

    save(out, goods)

    page += 1
    params["pagingIndex"] = str(page)
    print(page)

out.close()
