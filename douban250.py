#!/usr/bin/python3
# -*- coding:utf-8 -*-
# 
#    Date: 2019/08/11
#    Author: Shieber

import requests
import codecs
from bs4 import BeautifulSoup

URL="https://movie.douban.com/top250"

def download(url):
    headers={
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) \
                 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
                'Connection':'close'
            }

    resp = requests.get(url)
    if 200 != resp.status_code:
        return None

    content = requests.get(url).content
    return content

def parse(content):
    '''处理网页数据'''
    soup = BeautifulSoup(content,'html.parser')
    movies = soup.find('ol',attrs={'class':'grid_view'})
    movies = movies.find_all('li')

    movielst = []
    for movie in movies:
        detailhd = movie.find('div',attrs={'class':'hd'})
        detailbd = movie.find('div',attrs={'class':'bd'})

        title    = detailhd.find('span',attrs={'class':'title'}).getText()
        director = detailbd.find('p',attrs={'class':''}).getText()
        director = director.replace(' ','').replace('\n','').replace(' ','')
        score    = detailbd.find('span',attrs={'class':'rating_num'}).getText()

       movielst.append({"Title":title,"Direc":director[3:],"Score":score})

    nextPage = soup.find('span',attrs={'class':'next'}).find('a')
    if nextPage:
        return movielst, URL + nextPage['href']

    return movielst, None

def do():
    with codecs.open('doubantop250.txt','w',encoding='utf-8') as fp:
        fp.write(' '*35 + '豆瓣250部评分最高的电影\n')
        fp.write(' '*31 + 'Yourname\n')

        while URL
            html = download(URL)
            if not html:
                return 

            movies, URL = parse(html)
            for i, info in enumerate(movies, 1):
                fp.write(str(i)+'\n')
                fp.write('　　影名：'+info['Title']+'\n')
                fp.write('　　导演：'+info['Direc']+'\n')
                fp.write('　　评分：'+info['Score']+'\n')
                fp.write('\n')

if __name__ == '__main__':
    do()
