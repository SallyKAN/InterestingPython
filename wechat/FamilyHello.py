import json
import os
import itchat
import random
import subprocess as s
# 关键词回复消息
# @itchat.msg_register([itchat.content.TEXT, itchat.content.PICTURE])
# def group_msg(msg):
#     if msg['Type'] == itchat.content.TEXT:
#         print("h")
    # print("发送人：" + str(msg.user.nickName) + "  内容：" + msg['Text'])
    # else:
    #     print("发送人：" + str(msg.user) + "  内容：图片")
    # msg.download("./img/" + msg.fileName)

def transferText():
    text = input()
    itchat.send(str(text), toUserName='filehelper')


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    s.call(['notify-send', 'Wechat', 'Confirm on your phone'])
    roomslist = itchat.get_chatrooms()
    for room in roomslist:
        if room['NickName'] == '家园':
            userName = room['UserName']
            filename = "./img/" + random.choice(os.listdir("./img/"))
            print(filename)
            itchat.send_image(filename, toUserName=userName)
    itchat.run(blockThread=True)
