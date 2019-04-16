import json
import itchat


class WxMessage:
    name = ''
    type = ''
    msg = ''

    def __init__(self, name, type, msg):
        self.name = name
        self.type = type
        self.msg = msg


class User:
    name = ''
    count = 0

    def __init__(self, name, count):
        self.name = name
        self.count = count

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_count(self):
        return self.count

    def set_count(self, count):
        self.count = count


# 加载配置信息
def load_config():
    f = open("keys.json", encoding='utf-8')
    return json.load(f)


# 注册普通消息
@itchat.msg_register(itchat.content.TEXT)
def friend_msg(msg):
    mg = WxMessage('', '', '')
    mg.name = msg.user.nickName
    mg.type = "朋友"
    mg.msg = msg.text
    # print(mg.name)
    print(msg['Text'])


# 注册群聊消息
@itchat.msg_register([itchat.content.TEXT, itchat.content.PICTURE], isGroupChat=True)
def group_msg(msg):
    mg = WxMessage('', '', '')
    mg.name = msg.actualNickName
    mg.type = msg.user.nickName
    mg.msg = msg.text
    if user.get_count() >= 5:
        user.set_name('')
        user.set_count(0)

    if msg['Type'] == itchat.content.TEXT:
        for item in keys:
            if item in mg.msg or user.count > 0:
                send_reminder(mg)
                user.set_name(mg.name)
                count = user.get_count()
                user.set_count(count + 1)
                break
        print_msg(mg)
    elif msg['Type'] == itchat.content.PICTURE:
        if user.get_name() == mg.name:
            msg.download("./img/" + msg.fileName)
            img = '@%s@%s' % ('img' if msg['Type'] == 'Picture' else 'fil', "./img/" + msg['FileName'])
            print(img)
            send(img, userName)
            count = user.get_count()
            user.set_count(count + 1)


def send(msg, userName):
    itchat.send(msg, toUserName=userName)


# @itchat.msg_register(itchat.content.PICTURE, isGroupChat=True)
# def download_files(msg):
#     msg.download(msg.fileName)
#     img = '@%s@%s' % ('img' if msg['Type'] == 'Picture' else 'fil', msg['FileName'])
#     # itchat.send(img, msg['FromUserName'])
#     send(img,userName)


def send_reminder(mg):
    message_info = "发送群名：" + mg.type + "\n" + "发送人：" + mg.name + "\n" + "内容：" + mg.msg + "\n"
    send(message_info, userName)


# 打印到的消息
def print_msg(mg):
    message_info = "发送群名：" + mg.type + "\n" + "发送人：" + mg.name + "\n" + "内容：" + mg.msg + "\n"
    print(message_info)

# @itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING,PICTURE,RECORDING,ATTACHMENT,VIDEO,FRIENDS,SYSTEM])
# def reply_mseeage(msg):
#     if msg['Type'] == TEXT:
#        replyContent="我收到了文本消息"
#     if msg['Type'] == MAP:
#        replyContent = "我收到了位置内容"
#     if msg['Type'] == CARD:
#        replyContent = "我收到了推荐人信息"
#     if msg['Type'] == NOTE:
#        replyContent = "我收到了通知文本"
#     if msg['Type'] == SHARING:
#        replyContent = "我收到了分享消息"
#     if msg['Type'] == PICTURE:
#        replyContent = "我收到了图片"
#        download_files(msg)
#     if msg['Type'] == RECORDING:
#        replyContent = "我收到了语音"
#        download_files(msg)
#     if msg['Type'] == ATTACHMENT:
#        replyContent = "我收到了文件"
#        download_files(msg)
#     if msg['Type'] == VIDEO:
#        replyContent = "我收到了视频"
#        download_files(msg)
#     if msg['Type'] == FRIENDS:
#         itchat.add_friend(**msg['Text'])
#         replyContent = "我收到了好友请求"
#     if msg['Type'] == SYSTEM:
#        replyContent = "我收到了一条系统消息"
#     return replyContent;


if __name__ == '__main__':
    itchat.auto_login(enableCmdQR=2)
    roomslist = itchat.get_chatrooms()
    # for it in roomslist:
    #     print(it['NickName'])
    config = load_config()
    keys = config['keys']
    user_info = itchat.search_friends(name='LinkedME')
    userName = user_info[0]["UserName"]
    user = User('', 0)
    # r = redis.Redis(host='192.168.254.102', port=33424, db=3)
    # 运行
    itchat.run(True)
