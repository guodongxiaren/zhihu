#!/usr/bin/env python
# coding=utf-8
"""
python 3
"""
from bs4 import BeautifulSoup
from urllib import request
from urllib import parse
import datetime
import json
import sys
import time


def get_main_topic():
    url = 'https://www.zhihu.com/topics'
    origin_bytes = request.urlopen(url).read()
    origin_string = origin_bytes.decode('utf-8')
    soup = BeautifulSoup(origin_string, 'html.parser')

    # <li class="zm-topic-cat-item" data-id="1761"><a href="#生活方式">生活方式</a></li>
    main_topic_li = soup.find_all('li', class_='zm-topic-cat-item')
    main_topic = {}
    for li in main_topic_li:
        topic_id = li.get('data-id')
        topic_name = li.text
        main_topic[int(topic_id)] = topic_name

    return main_topic

def get_sub_topic(main_topic_id):
    size = 20
    url = 'https://www.zhihu.com/node/TopicsPlazzaListV2'
    offset = 0
    topic_list = {}
    while True:
        data = {
            'method': 'next',
            'params': '{"topic_id":%d,"offset":%d,"hash_id":""}' % (main_topic_id, offset),
        }
        # requests.post(url, data=data) wrong, I don't know why
        params = parse.urlencode(data).encode('utf-8')
        req = request.Request(url, params)
        resp = request.urlopen(req)
        resp_text = resp.read()
        resp_json = json.loads(resp_text)
        html_list = resp_json.get("msg", "")

        for origin_string in html_list: 
            soup = BeautifulSoup(origin_string, 'html.parser')
            a_list = soup.find_all('a')
            for a in a_list:
                href = a.get('href')
                if href == 'javascript:;':
                    continue
                name = a.text.strip()
                topic_id = href[len('/topic/'):]
                topic_list[topic_id] = name
        if len(html_list) < size:
            break;
        offset += size
    return topic_list

def get_all_topic_list(main_topic=None):
    if main_topic is None:
        main_topic = get_main_topic()
    all_topic_list = {}
    for main_topic_id, main_topic_name in main_topic.items():
        topic_list = get_sub_topic(main_topic_id)
        #all_topic_list[main_topic_id] = topic_list
        all_topic_list[main_topic_name] = topic_list
        #time.sleep(1)
        print('%s done:has %d sub topic' % (main_topic_name, len(topic_list)))
    return all_topic_list


if __name__ == '__main__':
    #topic_list = get_sub_topic(4217) # for test
    #print(topic_list)
    #exit("")
    main_topic = get_main_topic()
    all_topic = get_all_topic_list(main_topic)
    json.dump(all_topic, open('../data/topic.json', 'w'), ensure_ascii=False, indent=4)
