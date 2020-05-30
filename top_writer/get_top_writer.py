#!/usr/bin/env python
# coding=utf-8
import requests
import json
from bs4 import BeautifulSoup

def load_cookie(filename):
    f = open(filename, 'r')
    cookie = f.readlines()[0].strip()
    f.close()
    return cookie

def load_header(filename):
    f = open(filename, 'r')
    header = {}
    for line in f.readlines():
        pos = line.find(':')
        if pos == -1:
            continue
        data = [line[0:pos], line[pos+1:-1]]
        key, value = map(lambda x:x.strip(), data)
        header[key] = value
    f.close()

    cookie = load_cookie('../data/cookie.txt'),
    "why is tuple"
    if type(cookie) == tuple:
        cookie = cookie[0]
    header['Cookie'] = cookie
    return header

def get_top_writer(topic_id):
    header = load_header('h.txt')
    url = 'https://www.zhihu.com/topic/%d/top-writer' % (int(topic_id))
    
    offset = 0
    author_list = []
    while True:
        data = {
            'offset': offset
        }
        resp = requests.post(url, data=data, headers=header)
        text = resp.text
        data = json.loads(text)
        count, html = data['msg']
        soup = BeautifulSoup(html, 'html.parser')
        writer_list = soup.find_all('a', class_='zg-link')
        writer_list = writer_list[0:count]
        for writer in writer_list: 
            href = writer['href']
            id = href[len('/people/'):]
            name = writer.text
            author = {
               'id': id,
               'name': name
            }
            author_list.append(author)
        if count < 20:
            break
        offset += count
    return author_list

if __name__ == '__main__':
    res = get_top_writer(19550874)
    print(res)
