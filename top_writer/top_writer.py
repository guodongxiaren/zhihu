#!/usr/bin/env python
# coding=utf-8
import datetime
import json
from bs4 import BeautifulSoup
import random
import requests
import sys
import time
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
        has_print_main_topic = False
        topic_id_list = list(sub_topics.keys())
        random.shuffle(topic_id_list)

        #for topic_id, topic_name in sub_topics.items():
        for topic_id in topic_id_list:
            topic_name = sub_topics[topic_id]
            #time.sleep(random.randint(1, 10))
            sys.stderr.write('@begin %s \n' % topic_name)
            sys.stderr.flush()
            time.sleep(2)
            author_list = get_top_author(topic_id)
            if len(author_list) == 0:
                continue
            if not has_print_main_topic:
                print('# %s(主话题)\n' % main_topic)
                has_print_main_topic = True
            top_author_dict[topic_name] = author_list
            print('## %s \n拥有 %d 位优秀回答者:\n' % (topic_name, len(author_list)))
            for author in author_list:
                print('[`%s`](https://www.zhihu.com/people/%s)' % (author['name'], author['id']))
            sys.stdout.flush()
    return top_author_dict


if __name__ == '__main__':
    #author_list = get_top_author(19584970)
    #print(author_list)
    top_author_dict = get_all_top_author()
    author_set = set()
    for topic_name, author_list in top_author_dict.items():
        author_set.update([author['id'] for author in author_list])

    today = datetime.datetime.now().strftime('%Y-%m-%d')
    with open('.header.md', 'w') as f:
        f.write('--------\n')
        f.write('截止 %s，知乎共有 %d 位优秀回答者\n' % (today, len(author_set)))

