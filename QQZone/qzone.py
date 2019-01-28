import os

import re

import pymysql
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time


# 登录QQ空间
def login():
    driver = webdriver.Edge("C:\\Users\K\seleniumDriver\MicrosoftWebDriver.exe")
    # 使用get()方法打开待抓取的URL
    driver.get('http://user.qzone.qq.com/')
    time.sleep(5)
    # 等待5秒后，判断页面是否需要登录，通过查找页面是否有相应的DIV的id来判断
    try:
        driver.find_element_by_id('login_div')
        a = True
    except:
        a = False
    if a == True:
        # 如果页面存在登录的DIV，则模拟登录
        # 打开QQ网页
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').clear()  # 选择用户名框
        driver.find_element_by_id('u').send_keys('你的qq号')
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys('你的qq密码')
        driver.find_element_by_id('login_button').click()
        time.sleep(3)
        driver.switch_to.default_content()
    # driver.implicitly_wait(3)
    return driver


# 获取cookies,返回带cookies的requests
def back_session(driver):
    mysession = requests.session()
    cookies = driver.get_cookies()
    cookie = {}
    # 将cookies转换成字典格式
    for elem in cookies:
        cookie[elem['name']] = elem['value']

    headers = {'host': 'h5.qzone.qq.com',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'zh-CN,zh;q=0.8',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
               'connection': 'keep-alive'
               }
    c = requests.utils.cookiejar_from_dict(cookie, cookiejar=None, overwrite=True)
    mysession.headers = headers
    mysession.cookies.update(c)
    return mysession

#存储在mysql数据库中
def in_mysql(time,content,qq,conn):
    time=str(time.strip())
    time ='"'+time+'"'
    qq = '"'+qq+'"'
    # print(time)
    content=str(content.strip())
    sql="insert into `qq_friend` (`time`,`content`,`qq_number`) VALUES("+time+","+content+","+qq+")"
    # print(sql)
    conn.query(sql)
    conn.commit()

# g_tk算法
def get_g_tk(cookie):
    hashes = 5381
    for letter in cookie['p_skey']:
        hashes += (hashes << 5) + ord(letter)  # ord()是用来返回字符的ascii码
    return hashes & 0x7fffffff

def get_allQQ(mysession,g_tk,qzonetoken):
	#获取好友QQ的网址
	url_friend='https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin=491251735&do=1&fupdate=1&clean=1&g_tk='+str(g_tk)+'&qzonetoken='+qzonetoken
	friendpat='"uin":(.*?),'
	resp=mysession.get(url_friend)
	friendlist=re.compile(friendpat).findall(resp.text)
	time.sleep(3)
	return friendlist

def get_spider(mysession,qq,g_tk,qzonetoken):
    # 这个url是存储的是好友说说的内容和时间
    url = 'https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin=' + str(
        qq) + '&inCharset=utf-8&outCharset=utf-8&hostUin=' + str(
        qq) + '&notice=0&sort=0&pos=0&num=20&cgi_host=http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6&code_version=1&format=jsonp&need_private_comment=1&g_tk=' + str(
        g_tk) + '&qzonetoken=' + str(qzonetoken)

    # 内容
    cpat = '"certified".*?"conlist":(.*?),'
    # 时间
    tpat = '"certified".*?"createTime":"(.*?)"'

    # 获取总说说数,由于每个网页都会有,只爬取一次就好
    shuoshuo_number_pat = '"total":(.*?),'
    resp = mysession.get(url)
    resp.encoding = 'GBK'
    shuoshuo_number = re.compile(shuoshuo_number_pat).findall(resp.text)[0]
    content_list = re.compile(cpat, re.S).findall(resp.text)
    if len(content_list) == 0:
        print("该好友说说为0,或你被禁止查看此好友的空间")
        return False
    # 算出页数
    if int(shuoshuo_number) % 20 == 0:
        page = int(shuoshuo_number) / 20
    else:
        page = int(shuoshuo_number) / 20 + 1
    print("一共有" + str(shuoshuo_number) + "条说说")
    # 爬取接下几页的说说
    for i in range(0, int(page)):
        # 和上面的网址一样,只不过改页数需要变动pos这个参数
        pos = i * 20
        try:
            url = 'https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin=' + str(
                qq) + '&inCharset=utf-8&outCharset=utf-8&hostUin=' + str(qq) + '&notice=0&sort=0&pos=' + str(
                pos) + '&num=20&cgi_host=http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6&code_version=1&format=jsonp&need_private_comment=1&g_tk=' + str(
                g_tk) + '&qzonetoken=' + qzonetoken
            resp = mysession.get(url)
            content_list = re.compile(cpat, re.S).findall(resp.text)
            time_list = re.compile(tpat, re.S).findall(resp.text)
            print("正在爬取第" + str(i + 1) + "页信息----------")
            for c, t in zip(content_list, time_list):
                try:
                    c = c.replace('[{"con":', '').replace('[{"nick":','')
                    # print(c)
                    in_mysql(t, c,qq, conn)
                except Exception as e:
                    print(e)
                    print("有一条说说数据无法写入")

        except Exception as e:
            print("第" + str(i + 1) + "页信息爬取失败")

def start():
	#构造g_tk参数,这在构造网址上会有用
    # time = "2018年2月"
    # content= "你好"
    # sql = "insert into qq_friend (time,content) VALUES('"+time+"','"+content+"')"
    # print(sql)
    driver=login()
	#获取qzondetoken参数
    html=driver.page_source
    xpat=r'window\.g_qzonetoken = \(function\(\)\{ try\{return (.*?);\} catch\(e\)'
    qzonetoken=re.compile(xpat).findall(html)[0]
    cookies=driver.get_cookies()
    cookie = {}
    for elem in cookies:
        cookie[elem['name']] = elem['value']
    g_tk=get_g_tk(cookie)
    mysession=back_session(driver)
    driver.close()
    # 接下来就可以爬取好友的信息
    friend_list = get_allQQ(mysession, g_tk, qzonetoken)
    for i in range(0, len(friend_list)):
        print("现在爬取的是" + str(friend_list[i]) + "的信息")
        try:
            get_spider(mysession, friend_list[i], g_tk, qzonetoken)
            print(str(friend_list[i]) + "的信息已经爬取完毕***********")
            print("\n\n")
            time.sleep(5)
        except Exception as e:
            print("该好友爬取出现问题,跳过.爬取下一位好友")
            print("\n\n")
        time.sleep(3)

if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', user='root', password='password',
                           database='qq_spider', charset="utf8")
    start()
    conn.close()