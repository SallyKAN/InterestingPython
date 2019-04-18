import json
import random
from random import choice


import itchat

# 加载配置信息
def load_config():
    f = open("reply.json", encoding='utf-8')
    return json.load(f)

def send(msg, userName):
    itchat.send_msg(msg, toUserName=userName)

# 关键词回复消息
@itchat.msg_register([itchat.content.TEXT, itchat.content.PICTURE])
def group_msg(msg):
    # mg.msg = msg.text
    if msg['FromUserName'] in userNames:
        if msg['Type'] == itchat.content.TEXT:
            for item in keys:
                if item in msg.text:
                    send(choice(reply),msg['FromUserName'])
                    break
            print(msg.text)
        elif msg['Type'] == itchat.content.PICTURE:
            msg.download("./img/" + msg.fileName)
            img = '@%s@%s' % ('img' if msg['Type'] == 'Picture' else 'fil', "./img/" + msg['FileName'])
            return img

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    roomslist = itchat.get_chatrooms()
    # for it in roomslist:
    #     print(it['NickName'])
    config = load_config()
    keys = config['keys']
    reply = config['replyQ']
    ask = config['ask']
    testUsers = config['testUsers']
    userNames = []
    for user in testUsers:
        user_info = itchat.search_friends(name=user)
        userName = user_info[0]["UserName"]
        # send("hello", userName)
        send(choice(ask),userName)
        userNames.append(userName)
    # 运行
    itchat.run(True)
