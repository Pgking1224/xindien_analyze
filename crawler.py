import pandas as pd
import numpy as np
import time
from bs4 import BeautifulSoup
import requests

start_page = input('請輸入開始頁數:')
end_page = input('請輸入結束頁數:')
city = input('請輸入縣市:\n(ex:NewTaipei-city, Yunlin-county)')
district = input('請輸入郵遞區號:')
use = input('請輸入房屋用途:\n(ex:house-use)')
age = input('請輸入屋齡:\n(ex:0-5)')
scratch_range = range(int(start_page), int(end_page) + 1)

def crawler(scratch_range,city,district,use,age):
    title = []
    price = []
    detail = []
    for i in scratch_range:  
        s1 = []
        s2 = []
        s3 = []
        url = 'http://buy.sinyi.com.tw/list/{}/{}-zip/{}/{}-year/{}.html'.format(city,district,use,age,i)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, headers)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text ,'html.parser')
        a = soup.findAll('span','item_title')
        for i in a:
            title.append(i.get_text())
        b = soup.findAll('div','price_new')    
        for i in b:    
            price.append(i.get_text().replace(' ','').replace('\n',''))
        detail_line1 = soup.findAll('div','detail_line1')
        for i in detail_line1:    
            s3.append(i.get_text())
        detail_line2 = soup.findAll('div','detail_line2')
        for i in range(0,len(detail_line2),2):
            s1.append(detail_line2[i].get_text())
        for i in range(1,len(detail_line2),2):
            s2.append(detail_line2[i].get_text())        
        for i in range(len(s1)):
            ss = []
            for item in s3[i].split('\n'):
                if item != '':       
                    ss.append(item)
            for item in s1[i].split('\n'):
                if item != '':
                    ss.append(item)
            for item in s2[i].split('\n'):
                if item != '':       
                    ss.append(item)
            detail.append(ss)
    j = []
    for item in detail:
        jj = []
        for item2 in item:
            if ' ' not in item2:
                jj.append(item2.replace(' ',''))
        j.append(jj)
    
    add = []
    for item in j:
        add.append(item[0])
        item.remove(item[0])
    df = pd.DataFrame({'House':title,'address':add,'price':price,'info':j}) 
    df.to_csv('{}_{}.csv'.format(city, district),index=False)
    print(len(df))


if __name__ == '__main__': 
    crawler(scratch_range,city,district,use,age)