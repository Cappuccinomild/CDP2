from multiprocessing import Process
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re
import os
import time
import random

def get_total_item_num(url, params):

    res = requests.get(url, params=params)

    html = res.text

    soup = BeautifulSoup(html, 'html.parser')

    #전체리스트 추출
    total = ''
    for p in re.findall("\d+", soup.select('a[class=_productSet_total]')[0].text):
        total += p

    return int(total)

def crawl(index, url, page, PAGE_LEN, params):

    ID = []
    name = []
    price = []
    send_price = []
    category = []
    mall = []

    params['pagingIndex'] = page

    #페이지 끝까지 읽기
    while page <= PAGE_LEN:
        #print(page)
        res = requests.get(url, params=params)
        html = res.text

        soup = BeautifulSoup(html, 'html.parser')
        data = soup.select('li[class=_itemSection]')

        #데이터를 받아오지 못한 경우
        if len(data) == 0:
            print("Data Receive Failed")
            for i in range(random.randint(20, 40)):
                print(str(index) + " : wait..." + str(i))
                time.sleep(1)
            continue

        #상품정보 저장
        for item in data:

            #상품 ID
            ID.append(item.get('data-nv-mid'))

            #상품명
            name.append(item.select_one('div[class=tit] > a').text.replace(",", " "))

            #가격
            price.append(''.join(re.findall("\d+", item.select_one('span[class=price] > em').text)))

            #배송비
            send_price.append(''.join(re.findall("\d+", item.select_one('ul[class=mall_option] > li > em').text)))

            #카테고리
            category.append(item.select_one('span[class=depth]').text.replace(' ', '').replace('\n', ''))

            #매장
            mall.append(item.select_one('p[class=mall_txt] > a').get('href'))


        print(page, len(ID))
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
    search_result.to_csv("data_"+str(index)+".csv", index = False, encoding="utf-8-sig")

def merge(process_num):

    df = pd.read_csv('data_0.csv')
    os.remove('data_0.csv')

    for i in range(1, process_num):
        fname = "data_" + str(i) + ".csv"

        temp_df = pd.read_csv(fname)
        df = pd.concat([df, temp_df])
        os.remove(fname)

    print("merge end")
    df.to_csv("data.csv", index = False, encoding="utf-8-sig")

if __name__ == "__main__":

    url = "https://search.shopping.naver.com/search/all.nhn"

    #GET 파라미터들
    params = {"pagingIndex" : "1", "pagingSize" : "80", "viewType" : 'list', "sort" : "rel" , "frm" : "NVSHPAG", "query" : ""}

    product_name = "니퍼"

    params["query"] = product_name

    page = 1
    TOTAL_ITEM_NUM = get_total_item_num(url, params)

    #pagesize 읽기
    import math
    PAGE_LEN = math.ceil(TOTAL_ITEM_NUM / int(params['pagingSize']))

    #멀티프로세싱
    procs = []
    process_num = 3
    part = math.ceil(PAGE_LEN / process_num)

    for i in range(process_num):

        start = i*part + 1
        end = (i+1) * part
        if end > PAGE_LEN:
            end = PAGE_LEN

        proc = Process(target = crawl, args =( i, url, start, end, params ))
        print(start, end)
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    #merge(process_num)
