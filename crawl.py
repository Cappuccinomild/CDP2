import requests
from bs4 import BeautifulSoup
import re

#txt파일로 저장
def save(out, goods):
    for key, value in goods.items():
        out.write(key + '\t')
        out.write('\t'.join(value))
        out.write('\n')

def get_total_item_num(url, params):

    res = requests.get(url, params=params)

    html = res.text

    soup = BeautifulSoup(html, 'html.parser')

    #전체리스트 추출
    total = ''
    for p in re.findall("\d+", soup.select('a[class=_productSet_total]')[0].text):
        total += p

    return int(total)

#한 페이지를 읽어서 데이터를 정리
def get_page_data(url, params):

    res = requests.get(url, params=params)

    html = res.text

    soup = BeautifulSoup(html, 'html.parser')

    search_result = {}
    for item in soup.select('li[class=_itemSection]'):

        goods = []
        #상품명
        goods.append(item.select_one('div[class=tit]>a').text)

        #가격
        goods.append(''.join(re.findall("\d+", item.select_one('span[class=price]>em').text)))

        #카테고리
        goods.append(item.select_one('span[class=depth]').text.replace(' ', '').replace('\n', ''))

        #매장
        goods.append(item.select_one('p[class=mall_txt]>a').get('href'))

        search_result [item.get('data-nv-mid')] = goods

    return search_result

def dict_merge(a, b):

    for key, value in b.items():
        print(key, value)
        flag = False

        try:

            print(a[key])

        except:

            a[key] = value
            flag = True

        if flag == False:
            print("중복")


url = "https://search.shopping.naver.com/search/all.nhn"

#GET 파라미터들
params = {"pagingIndex" : "1", "pagingSize" : "80", "viewType" : 'list', "sort" : "rel" , "frm" : "NVSHPAG", "query" : ""}

product_name = "KM-037"

params["query"] = product_name

out = open("output.txt", "w", -1, "utf-8")

page = 1
TOTAL_ITEM_NUM = get_total_item_num(url, params)


import math
PAGE_LEN = math.ceil(TOTAL_ITEM_NUM / int(params['pagingSize']))

search_result={}

while page <= PAGE_LEN:

    prev = len(search_result)

    search_result.update(get_page_data(url, params))

    print(len(search_result) - prev, page)

    page += 1
    params["pagingIndex"] = str(page)



save(out, search_result)

print(TOTAL_ITEM_NUM, len(search_result))

out.close()
