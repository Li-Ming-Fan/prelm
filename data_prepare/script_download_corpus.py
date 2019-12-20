#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 20:21:18 2019

@author: li-ming-fan
"""

import os
import re
from requests import request
from pyquery import PyQuery as pq

header = {  
  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
}


#
DIR_BASE = "../bert_corp_raw"
#
URL_BASE_ART = "https://baike.baidu.com/art/%E8%89%BA%E6%9C%AF%E8%AF%84%E8%AE%BA?pn=2"
SUBDIR_BASE_ART = "art"
#

#
def get_article_links(str_url):
    """
    """
    # import requests
    # response = requests.get(url,headers=headers)
    response = request('GET', str_url, headers=header) #定义头信息发送请求返回response对象
    response.encoding='UTF-8'
    
    # print(response.url) #返回请求的URL
    # print(response.status_code)  #返回状态码200
    # print(response.encoding)  #返回编码
    # print(response.text)  #返回响应的内容以unicode表示
    # print(response.headers) #返回头信息
    # print(response.cookies) #返回cookies CookieJar
    # print(response.json()) #返回json数据
    
    #
    pattern = re.compile('<div class="list-content">(.*?)</div>', re.S)
    text = re.search(pattern, response.text)
    #
    str_temp = text.groups()[0]
    # print(str_temp)
    #
    pattern = re.compile('<a href="(.*?)target="_blank"', re.S)
    list_links_trim = re.findall(pattern, str_temp)
    # print(list_links_trim)
    #
    list_links = []
    for i in list_links_trim:
        link = i.strip()[:-1]
        list_links.append(link)
        # print(link)
    #
    return list_links

def get_article_title_body(link_url):
    """
    """
    response = request('GET', link_url, headers=header) #定义头信息发送请求返回response对象
    response.encoding = 'UTF-8'
    # print(response.url) #返回请求的URL  
    # print(response.text) 
    #
    pattern = re.compile('<h1 class="title" title="(.*?)">', re.S)
    text = re.search(pattern, response.text)
    #
    if text is None:
        return None, None
    #
    title = text.groups()[0]
    # print(title)
    #
    pattern = re.compile('<div class="text-box">(.*?)</div>', re.S)
    text = re.search(pattern, response.text)
    #
    body_html = text.groups()[0]
    # print(body_html)
    #
    
    # parse html
    doc = pq(body_html)
    # print(doc)
    #
    list_paragraphs = []
    #
    items = doc("p").items()
    for item in items:
        # print(item)
        list_paragraphs.append(item.text())
        # print(item.text())
        # print()
    
    return title, list_paragraphs

def write_article_to_file(dir_data, link, title, body_paras):
    """
    """
    str_arr = link.split("article/")
    filename = str_arr[1].replace("htm", "txt")
    filepath = os.path.join(dir_data, filename)
    
    fp = open(filepath, "w", encoding="utf-8")
    fp.write(link + "\n")
    fp.write(title + "\n")
    for para in body_paras:
        fp.write(para + "\n")
    #
    fp.close()
    #
    
#
if __name__ == "__main__":
    """
    """
    if not os.path.exists(DIR_BASE): os.mkdir(DIR_BASE)
    #
    dir_base = os.path.join(DIR_BASE, SUBDIR_BASE_ART)
    if not os.path.exists(dir_base): os.mkdir(dir_base)
    #
    url_base = URL_BASE_ART[:-1]
    #
    page_start = 1
    page_end = 5
    #
    count = 0
    for page in range(page_start, page_end):
        #
        url = url_base + str(page)
        print(url)
        #
        list_links = get_article_links(url)
        # print(list_links)
        #
        for link in list_links:
            #
            count += 1
            print("%d | %s" % (count, link))
            #
            title, body_paras = get_article_title_body(link)            
            # print(title)
            # print(body_paras)
            #
            if title is None: continue
            #
            write_article_to_file(dir_base, link, title, body_paras)
            #
            
    
