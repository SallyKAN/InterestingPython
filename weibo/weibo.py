import time
from logging import exception

import re
from selenium import webdriver


driver = webdriver.Edge("C:\\Users\K\seleniumDriver\MicrosoftWebDriver.exe")
def loginWeibo(username, password):
    driver.get('https://passport.weibo.cn/signin/login')
    time.sleep(3)

    driver.find_element_by_id("loginName").send_keys(username)
    driver.find_element_by_id("loginPassword").send_keys(password)
    driver.find_element_by_id("loginAction").click()


def visitUserInfo(userId):
    driver.get('http://weibo.cn/' + userId)

    print('********************')
    print('用户资料')

    # 1.用户id
    print('用户id:' + userId)

    # 2.用户昵称
    strName = driver.find_element_by_xpath("//div[@class='ut']")
    strlist = strName.text.split(' ')
    nickname = strlist[0]
    print('昵称:' + nickname)

    # 3.微博数、粉丝数、关注数
    strCnt = driver.find_element_by_xpath("//div[@class='tip2']")
    pattern = r"\d+\.?\d*"  # 匹配数字，包含整数和小数
    cntArr = re.findall(pattern, strCnt.text)
    print(strCnt.text)
    print("微博数：" + str(cntArr[0]))
    print("关注数：" + str(cntArr[1]))
    print("粉丝数：" + str(cntArr[2]))

    print('\n********************')
    # 4.将用户信息写到文件里
    with open("userinfo.txt", "w", encoding="gb18030") as file:
        file.write("用户ID：" + userId + '\r\n')
        file.write("昵称：" + nickname + '\r\n')
        file.write("微博数：" + str(cntArr[0]) + '\r\n')
        file.write("关注数：" + str(cntArr[1]) + '\r\n')
        file.write("粉丝数：" + str(cntArr[2]) + '\r\n')


def visitWeiboContent(userId):
    pageList = driver.find_element_by_xpath("//div[@class='pa']")
    print(pageList.text)
    pattern = r"\d+\d*"  # 匹配数字，只包含整数
    pageArr = re.findall(pattern, pageList.text)
    totalPages = pageArr[1]  # 总共有多少页微博
    print(totalPages)

    pageNum = 1  # 第几页
    numInCurPage = 1  # 当前页的第几条微博内容
    curNum = 0  # 全部微博中的第几条微博
    contentPath = "//div[@class='c'][{0}]"
    # while(pageNum <= 3):
    while (pageNum <= int(totalPages)):
        try:
            contentUrl = "http://weibo.cn/" + userId + "?page=" + str(pageNum)
            driver.get(contentUrl)
            content = driver.find_element_by_xpath(contentPath.format(numInCurPage)).text
            # print("\n" + content)                  # 微博内容，包含原创和转发
            if "设置:皮肤.图片.条数.隐私" not in content:
                numInCurPage += 1
                curNum += 1
                with open("weibocontent.txt", "a", encoding="gb18030") as file:
                    file.write(str(curNum) + '\r\n' + content + '\r\n\r\n')
            else:
                pageNum += 1  # 抓取新一页的内容
                numInCurPage = 1  # 每一页都是从第1条开始抓
                time.sleep(20)  # 要隔20秒，否则会被封
        except exception as e:
            print("curNum:" + curNum)
            print(e)
        finally:
            pass
    print("Load weibo content finished!")


if __name__ == '__main__':
    username = '491251735@qq.com'  # 输入微博账号
    password = 'kangjiayuan1119'  # 输入密码
    loginWeibo(username, password)  # 要先登录，否则抓取不了微博内容

    time.sleep(3)
    uid = '2177457674'  # “寻医问药”的个性域名
    visitUserInfo(uid)  # 获取用户基本信息
    visitWeiboContent(uid)  # 获取微博内容