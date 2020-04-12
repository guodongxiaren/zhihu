#!/usr/bin/env python
# coding=utf-8
import urllib.request as request
import json
url = 'https://api.github.com/repos/guodongxiaren/blog/issues/32'
origin_bytes = request.urlopen(url).read()
origin_string = origin_bytes.decode('utf-8')
json_obj = json.loads(origin_string)
f = open('./README.md', 'w')
if 'body' in json_obj:
    f.write(json_obj['body'])
f.close()
