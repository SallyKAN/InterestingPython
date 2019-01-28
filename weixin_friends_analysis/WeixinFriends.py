from wxpy import *
from pyecharts import Bar
from pyecharts import Map
import re
import jieba
import numpy
import pandas as pd
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator



def login():
    # 初始化机器人，扫码登陆
    bot = Bot(cache_path=True)
    # 获取所有好友
    my_friends = bot.friends()
    # print(type(my_friends))
    return my_friends,bot

def show_sex_ratio(friends):
    # 使用一个字典统计好友男性和女性的数量
    sex_dict = {'male': 0, 'female': 0}
    for friend in friends:
        # 统计性别
        if friend.sex == 1:
            sex_dict['male'] += 1
        elif friend.sex == 2:
            sex_dict['female'] += 1
    bar = Bar("微信好友性别比", "没有副标题")
    bar.use_theme('dark')
    bar.add("性别", ["男", "女"], [sex_dict['male'], sex_dict['female']])
    bar.render()

def show_area_distribution(friends):
    # 使用一个字典统计各省好友数量
    province_dict = {'北京': 0, '上海': 0, '天津': 0, '重庆': 0,
        '河北': 0, '山西': 0, '吉林': 0, '辽宁': 0, '黑龙江': 0,
        '陕西': 0, '甘肃': 0, '青海': 0, '山东': 0, '福建': 0,
        '浙江': 0, '台湾': 0, '河南': 0, '湖北': 0, '湖南': 0,
        '江西': 0, '江苏': 0, '安徽': 0, '广东': 0, '海南': 0,
        '四川': 0, '贵州': 0, '云南': 0,
        '内蒙古': 0, '新疆': 0, '宁夏': 0, '广西': 0, '西藏': 0,
        '香港': 0, '澳门': 0}
    for friend in friends:
        if friend.province in province_dict.keys():
            province_dict[friend.province] += 1
    # return province_dict
    data = []
    for key, value in province_dict.items():
        data.append({'name': key, 'value': value})

    value = [x for x in province_dict.values()]
    attr = [x for x in province_dict.keys()]
    print(value)
    # print(attr)
    map = Map("全国地图示例", width=1200, height=600)
    map.add("", attr, value, maptype='china',is_visualmap=True,
            is_piecewise=True,visual_range_text=["", ""],
            pieces=[
                {"max": 60, "min": 20, "label": "高数值"},
                {"max": 19, "min": 0, "label": "低数值"}],
            visual_text_color='#000')
    map.render()
    # value = [155, 10, 66, 78]
    # attr = ["福建", "山东", "北京", "上海"]
    # map = Map("全国地图示例", width=1200, height=600)
    # map.add("", attr, value, maptype='china')
    # map.render()

def write_txt_file(path, txt):
    '''
    写入txt文本
    '''
    with open(path, 'a', encoding='gb18030', newline='') as f:
        f.write(txt)

def read_txt_file(path):
    '''
    读取txt文本
    '''
    with open(path, 'r', encoding='gb18030', newline='') as f:
        return f.read()

# 统计签名
def show_signature(friends):
    for friend in friends:
        # 对数据进行清洗，将标点符号等对词频统计造成影响的因素剔除
        pattern = re.compile(r'[一-龥]+')
        filterdata = re.findall(pattern, friend.signature)
        write_txt_file('signatures.txt', ''.join(filterdata))

    # 读取文件
    content = read_txt_file('signatures.txt')
    segment = jieba.lcut(content)
    words_df = pd.DataFrame({'segment': segment})

    # 读取stopwords
    stopwords = pd.read_csv("stopwords.txt", index_col=False, quoting=3, sep=" ", names=['stopword'], encoding='utf-8')
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
    # print(words_df)
    words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数": numpy.size})
    words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)
    # print(words_stat)
    # color_mask = imread('background.jfif')
    wordcloud = WordCloud(font_path="simhei.ttf",  # 设置字体可以显示中文
                          background_color="white",  # 背景颜色
                          max_words=100,  # 词云显示的最大词数
                          # mask=color_mask,  # 设置背景图片
                          max_font_size=100,  # 字体最大值
                          random_state=42,
                          width=1000, height=860, margin=2,
                          # 设置图片默认的大小,但是如果使用背景图片的话,                                                   # 那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
                          )
    word_frequence = {x[0]: x[1] for x in words_stat.head(100).values}
    print(word_frequence)
    word_frequence_dict = {}
    for key in word_frequence:
        word_frequence_dict[key] = word_frequence[key]
    wordcloud.generate_from_frequencies(word_frequence_dict)
    # word_frequence_list = []
    # for key in word_frequence:
    #     temp = (key, word_frequence[key])
    #     word_frequence_list.append(temp)
    # wordcloud = wordcloud.generate_from_frequencies(word_frequence)
    # wordcloud = wordcloud.fit_words(word_frequence_list)
    wordcloud.to_file('output.png')

    # plt.imshow(wordcloud, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()

friends,bot = login()
show_signature(friends)
# bot.file_helper.send_image('output.png')
# bot.file_helper.send('https://github.com/SallyKAN/InterestingPython/tree/master/weixin_friends_analysis')
# print(attr)