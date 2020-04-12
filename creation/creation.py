#!/usr/bin/env python
# coding=utf-8
import json
user = 'guodongxiaren'
if __name__ == '__main__':
    print('%s 在各个话题下面的创作:' % user)
    topic_dict = json.load(open('../data/topic.json', 'r'))
    id_list = []
    for main_topic, sub_topics in topic_dict.items():
        print('# %s\n' % main_topic)
        for id, name in sub_topics.items():
            url = 'https://www.zhihu.com/people/%s/creations/%s' % (user, id)
            #print('[%s](%s)' % (name, url))
            print('[`%s`][%s]' % (name, id))
            id_str = '[%s]: %s' % (id, url)
            id_list.append(id_str)

