#!/usr/bin/env python
# coding=utf-8
import base64
import datetime
import getpass
import os
import signal
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from urllib import parse
from PIL import Image, ImageEnhance
import pytesseract
import numpy as np
import json
sys.path.append('/Users/jelly/github/zheye')
from zheye import zheye

from selenium.webdriver import Chrome, ChromeOptions
options = ChromeOptions()

options.add_experimental_option('excludeSwitches', ['enable-automation'])


#browser = webdriver.PhantomJS()
#browser = webdriver.Firefox()
#browser = webdriver.Chrome()
browser = webdriver.Chrome(options=options)

def ocr(img_path):
    #login = Image.open(img_path).convert('RGB')
    loginImg = Image.open(img_path).convert('RGB')
    loginImg.show()
    print('----')
    print(pytesseract.image_to_string(loginImg))
    print('----')
    """
    截取下来验证码图片，并且进行灰度转化，二值化处理
    """
    #loginImg = login.crop(rangle)  # 截取验证码图片
    #loginImg.show()
    loginImg = loginImg.convert("L")#convert()方法传入参数L，将图片转化为灰度图像
    #loginImg.show()
    print("xx")
    loginImg = np.asarray(loginImg)
    loginImg = (loginImg > 100) * 255
    print("xxx")
    loginImg = Image.fromarray(loginImg).convert('RGB')
    print("xxx1")
    sharpness = ImageEnhance.Contrast(loginImg)
    print("xxxx")
    loginImg = sharpness.enhance(3.0)
    loginImg = loginImg.resize((300, 100))
    loginImg.show()
    """
    将图片转化为文本字符串，切割之后，转化为数字进行计算
    """
    text = pytesseract.image_to_string(loginImg, lang='ytbx').strip().replace(' ', '')
    print(text)


def login():
    """登录，需要输入用户名和密码
    """
    login_url = 'https://www.zhihu.com/signin'
    print('xxxxxxxx')
    browser.get(login_url)
    print('xxxxxxxx')
    time.sleep(1)
    print('open:' + login_url)

    #username, password = '', ''
    username, password = '13315728454', 'shenzhenmao18'
    # 输入用户名和密码
    """
    while username.strip() == '':
        username = raw_input('username:')
    while password.strip() == '':
        password = getpass.getpass('passord:')
    """
    browser.find_elements_by_class_name('SignFlow-tab')[1].click()
    #time.sleep(3)

    browser.find_element_by_name('username').send_keys(username)
    print('username')
    #time.sleep(3)
    browser.find_element_by_name('password').send_keys(password)
    print('password')
    #time.sleep(3)
    browser.find_element_by_class_name('SignFlow-submitButton').click()
    time.sleep(3)
    img = None
    is_ch, is_en = False, False
    try:
        img = browser.find_element_by_class_name('Captcha-chineseImg')
        is_ch = True
    except Exception as e:
        try:
            img = browser.find_element_by_class_name('Captcha-englishImg')
            is_en = True
        except Exception as e:
            print('img not found')
    if img is None:
        print('img not found')
        exit("xxx")
    print("size:")
    print(img.size)

    print('get img src')
    imgsrc = img.get_attribute('src')
    print(imgsrc)
    
    src_prefix, base64_img = imgsrc.split(',')
    
    #imgdata = base64.b64decode(imgsrc[len('data:image/jpg;base64,'):])
    missing_padding = len(base64_img) % 4
    if missing_padding != 0:
        base64_img += '='* (4 - missing_padding)
    
    base64_img = parse.unquote(base64_img)
    imgdata = base64.b64decode(base64_img)
    if is_ch:
        pic_name = 'catcha_ch.jpg'
    elif is_en:
        pic_name = 'catcha_en.gif'
    file = open(pic_name, 'wb')
    file.write(imgdata)
    file.close()
    if is_ch:
        z = zheye()
        positions = z.Recognize(pic_name)
        print(positions)
        mouse_action = ActionChains(browser)
        for pos in positions:
            x, y = pos
            print(x,y)
            x, y = x/2, y/2
            print(x,y)
            mouse_action.move_to_element_with_offset(img, y, x).click().perform()
            time.sleep(2)

        mouse_action.click().perform()
    if is_en:
        ocr(pic_name)

    print('click1')
    browser.find_element_by_class_name('SignFlow-submitButton').click()
    time.sleep(1)
    print('click2')
    browser.find_element_by_class_name('SignFlow-submitButton').click()
    print('click3')
    browser.find_element_by_class_name('SignFlow-submitButton').send_keys(Keys.ENTER)

def get_cookie():
    """从浏览器获取cookie
    """
    browser.refresh()
    cookie_list = browser.get_cookies()
    cookies = ''
    for cookie in cookie_list:
        name = cookie['name']
        value = cookie['value']
        cookies += "%s=%s; " % (name, value)

    return cookies


def save_cookie(cookie_path, cookie):
    """存储cookie
    cookie_path: cookie文件路径
    cookie: Cookie字符串
    """
    cookie_file = open(cookie_path, 'w')
    cookie_file.write(cookie)
    cookie_file.close()


def fresh_cookie(url, cookie_path):
    """刷新cookie
    """
    open_website(url)
    cookie = get_cookie()
    # print log
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sys.stderr.write(now + '\n')
    sys.stderr.write(cookie + '\n')

    if not os.path.exists(cookie_path):
        save_cookie(cookie_path, cookie)
    else:
        cookie_file = open(cookie_path, 'r+')
        origin_cookie = cookie_file.readline()
        cookie_file.close()

        if origin_cookie != cookie:
            save_cookie(cookie_path, cookie)


if __name__ == '__main__':
    login()
    try:
        # 创建子进程，结束主进程
        pid = os.fork()
        if pid > 0:
            sys.exit(0)

        os.setsid()
        #os.umask(022)
        os.umask(0)

        sys.stdout.flush()
        sys.stderr.flush()
        # 忽略一些信号
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGHUP, signal.SIG_IGN)

        si = open(os.devnull, 'r')
        so = open('run.log', 'w')
        se = open('run.log', 'w')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        fresh_cookie(url, cookie_path)

            # sleep 5 min
        #time.sleep(300)

    except Exception as error:
        sys.stderr.write(error.message)

    # browser.close()
