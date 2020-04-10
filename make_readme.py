#!/usr/bin/env python
# coding=utf-8
import json
user = 'guodongxiaren'
if __name__ == '__main__':
    topic_dict = json.load(open('./topic.json', 'r'))
    id_list = []
    for main_topic, sub_topics in topic_dict.items():
        print('# %s\n' % main_topic)
        for id, name in sub_topics.items():
            url = 'https://www.zhihu.com/people/%s/creations/%s' % (user, id)
            print('[`%s`](%s)' % (name, url))
            #print('[`%s`][%s]' % (name, id))
            id_str = '[%s]: %s' % (id, url)
            id_list.append(id_str)

    """

    print('\n-----------')
    for id_str in id_list:
        print(id_str)
    """
