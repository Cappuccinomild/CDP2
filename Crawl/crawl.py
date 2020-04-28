import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re

def get_total_item_num(url, params):

    res = requests.get(url, params=params)

    html = res.text

    soup = BeautifulSoup(html, 'html.parser')

    #전체리스트 추출
    total = ''
    for p in re.findall("\d+", soup.select('a[class=_productSet_total]')[0].text):
        total += p

    return int(total)

if __name__ == "__main__":
    url = "https://search.shopping.naver.com/search/all.nhn"

    #GET 파라미터들
    params = {"pagingIndex" : "1", "pagingSize" : "80", "viewType" : 'list', "sort" : "rel" , "frm" : "NVSHPAG", "query" : ""}

    product_name = "KM-037"

    params["query"] = product_name

    page = 1
    TOTAL_ITEM_NUM = get_total_item_num(url, params)

    #pagesize 읽기
    import math
    PAGE_LEN = math.ceil(TOTAL_ITEM_NUM / int(params['pagingSize']))

    ID = []
    name = []
    price = []
    send_price = []
    category = []
    mall = []

    #페이지 끝까지 읽기
    while page <= PAGE_LEN:
        print(page)
        res = requests.get(url, params=params)

        html = res.text

        soup = BeautifulSoup(html, 'html.parser')

        #상품정보 저장
        for item in soup.select('li[class=_itemSection]'):

            #상품 ID
            ID.append(item.get('data-nv-mid'))

            #상품명
            name.append(item.select_one('div[class=tit]>a').text.replace(",", " "))

            #가격
            price.append(''.join(re.findall("\d+", item.select_one('span[class=price]>em').text)))

            #배송비
            send_price.append(''.join(re.findall("\d+", item.select_one('ul[class=mall_option]>li>em').text)))

            #카테고리
            category.append(item.select_one('span[class=depth]').text.replace(' ', '').replace('\n', ''))

            #매장
            mall.append(item.select_one('p[class=mall_txt]>a').get('href'))

        page += 1
        params["pagingIndex"] = str(page)

    #상품정보들을 DataFrmae으로
    search_result = {
        'ID' : ID,
        'name' : name,
        'price' : price,
        'send_price' : send_price,
        'category' : category,
        'mall' : mall
    }

    search_result = pd.DataFrame(search_result, columns=["ID", "name", "price", "send_price", "category", "mall"])

    search_result.to_csv("data.csv", index = False, encoding="utf-8-sig")

    print(TOTAL_ITEM_NUM, len(search_result))
