#!/bin/bash
source ~/.bash_profile
python readme.py

fileday=`date -r README.md +'%Y%m%d'`
today=`date +'%Y%m%d'`
if [[ $today == $fileday ]];then
    git add README.md
    git commit -m"`date +'%Y-%m-%d'`"
    git pull --rebase
    git push
fi
