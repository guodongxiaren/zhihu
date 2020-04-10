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
            print('[`%s`][%s]' % (name, id))
            id_str = '[%s]: https://www.zhihu.com/people/%s/creations/%s' % (id, user, id)
            id_list.append(id_str)

    print('\n-----------')
    for id_str in id_list:
        print(id_str)

