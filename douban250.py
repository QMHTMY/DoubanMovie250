#!/usr/bin/python3
# -*- coding:utf-8 -*-
# 
#    Date: 2019/08/11
#    Author: Shieber
#
#                             APACHE LICENSE
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
#                            Function Description
#    Download Top 250 movies information into a txt file and 
#    You can transefer it into PDF file. 
#
#    Copyright 2019 
#    All Rights Reserved!

import requests
import codecs
from bs4 import BeautifulSoup

Src_URL="https://movie.douban.com/top250"

def download_page(url):
    headers={
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) \
                 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
                'Connection':'close'
            }
    content = requests.get(url).content
    return content

def parse_html(content):
    '''处理网页数据'''
    soup = BeautifulSoup(content,'html.parser')
    movie_list_soup = soup.find('ol',attrs={'class':'grid_view'})
    movie_list_li   = movie_list_soup.find_all('li')
    movie_info_list = []

    for movie_li in movie_list_li:
        detailhd   = movie_li.find('div',attrs={'class':'hd'})
        detailbd   = movie_li.find('div',attrs={'class':'bd'})

        movie_name = detailhd.find('span',attrs={'class':'title'}).getText()
        director   = detailbd.find('p',attrs={'class':''}).getText()
        director   = director.replace(' ','').replace('\n','').replace(' ','')
        score      = detailbd.find('span',attrs={'class':'rating_num'}).getText()

        infodic    = {
                        "Title":movie_name,
                        "Direc":director[3:],
                        "Score":score
                     }
        movie_info_list.append(infodic)

    next_page = soup.find('span',attrs={'class':'next'}).find('a')
    if next_page:
        return movie_info_list, Src_URL + next_page['href']

    return movie_info_list, None

def main():
    url = Src_URL
    with codecs.open('doubantop250.txt','w',encoding='utf-8') as fp:
        fp.write(' '*35 + '豆瓣250部评分最高的电影\n')
        fp.write(' '*31 + 'Yourname\n')
        i = 0
        while url:
            html_data   = download_page(url)
            movies, url = parse_html(html_data)
            for info in movies:
                i += 1
                fp.write(str(i)+'\n')
                fp.write('　　影名：'+info['Title']+'\n')
                fp.write('　　导演：'+info['Direc']+'\n')
                fp.write('　　评分：'+info['Score']+'\n')
                fp.write('\n')

if __name__ == '__main__':
    main()
