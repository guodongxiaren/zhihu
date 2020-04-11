#!/usr/bin/env python
# coding=utf-8
import json
from bs4 import BeautifulSoup
import requests
import sys
def load_cookie(filename):
    with open(filename, 'r') as f:
        cookie = f.read().strip()
    return cookie

def get_top_author(topic_id):
    url = 'https://www.zhihu.com/topic/%d/top-writer' % (int(topic_id))
    header = {
        'Cookie': load_cookie('../data/cookie.txt'),
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0',
    }
    resp = requests.get(url, headers=header)
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    writer_list = soup.find_all('a', class_='zg-link')
    author_list = []
    for writer in writer_list:
       href = writer['href']
       id = href[len('/people/'):]
       name = writer.text
       author = {
           'id': id,
           'name': name
       }
       author_list.append(author)
    return author_list

def get_all_top_author():
    topic_dict = json.load(open('../data/topic.json', 'r'))
    top_author_dict = {}
    for main_topic, sub_topics in topic_dict.items():
        print('# %s\n' % main_topic)
        for topic_id, topic_name in sub_topics.items():
            author_list = get_top_author(topic_id)
            if len(author_list) == 0:
                continue
            top_author_dict[topic_name] = author_list
            print('## %s \n拥有 %d 位优秀回答者:' % (topic_name, len(author_list)))
            for author in author_list:
                print('[%s](https://www.zhihu.com/people/%s)' % (author['name'], author['id']))
            sys.stdout.flush()
    return top_author_dict


if __name__ == '__main__':
    #author_list = get_top_author(19584970)
    #print(author_list)
    top_author_dict = get_all_top_author()
    top_author_count = 0
    for topic_name, author_list in top_author_dict.items():
        #print('%s has %d author: %s' % (topic_name, len(author_list), ','.join(author_list)))
        top_author_count += len(author_list)

    print('zhihu has %d top writer' % (top_author_count))

