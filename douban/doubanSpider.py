from urllib import request
from bs4 import BeautifulSoup as bs
import warnings

warnings.filterwarnings("ignore")

import re
import jieba    #分词包
import pandas as pd
import numpy
import matplotlib
import matplotlib.pyplot as plt


matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)

from wordcloud import WordCloud#词云包


def getNowPlayingMovie_list():
    resp = request.urlopen('https://movie.douban.com/nowplaying/beijing/')
    html_data = resp.read().decode('utf-8')
    ##print(html_data)
    soup = bs(html_data, 'html.parser')    
    nowplaying_movie = soup.find_all('div', id='nowplaying')
    nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')
    ##print(nowplaying_movie)
    nowplaying_list = []
    for item in nowplaying_movie_list:
        nowplaying_dict = {}
        nowplaying_dict['id']= item['data-subject']
        nowplaying_dict['name']= item['data-title']
        nowplaying_list.append(nowplaying_dict)
    return nowplaying_list
#print(nowplaying_list)
    
#print(nowplaying_movie_list)

def getCommentsById(movieId, pageNum):
    start = (pageNum-1)*20
    requrl = 'https://movie.douban.com/subject/'+ movieId + '/comments' +'?' +'start' + str(start) + '&limit=20'
    resp = request.urlopen(requrl)
    html_comment_data = resp.read().decode('utf-8')
    comment_soup = bs(html_comment_data,'html.parser')
    comment_div_lists= comment_soup.find_all('div',class_='comment')
    eachCommentList = [];
    for item in comment_div_lists: 
        if item.find_all('p')[0].string is not None:     
            eachCommentList.append(item.find_all('p')[0].string)
    return eachCommentList

#print(eachCommentList)
def main():
    commentList = []
    NowPlayingMovie_list = getNowPlayingMovie_list()
    for i in range(50):    
        num = i + 1 
        commentList_temp = getCommentsById(NowPlayingMovie_list[0]['id'], num)
        commentList.append(commentList_temp)
        #print(commentList)
    comments = ''
    for k in range(len(commentList)):
        comments = comments + (str(commentList[k])).strip()
    #print(comments)
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filterdata = re.findall(pattern, comments)
    cleaned_comments = ''.join(filterdata)

    segment = jieba.lcut(cleaned_comments)
    words_df=pd.DataFrame({'segment':segment})
    #print(words_df.head())
    stopwords=pd.read_csv("stopwords.txt",index_col=False,quoting=3,sep="\t",names=['stopword'], encoding='utf-8')#quoting=3全不引用
    words_df=words_df[~words_df.segment.isin(stopwords.stopword)]
    #print(words_df)
    words_stat=words_df.groupby(by=['segment'])['segment'].agg({"计数":numpy.size})
    words_stat=words_stat.reset_index().sort_values(by=["计数"],ascending=False)
    #print(words_stat)

    word_frequence_list = []
    wordcloud=WordCloud(font_path="simhei.ttf",background_color="white",max_font_size=80)
    word_frequence = {x[0]:x[1] for x in words_stat.head(1000).values}
    #print(word_frequence)
    
    #print(word_frequence_list)
    wordcloud=wordcloud.generate_from_frequencies(word_frequence)
    
    plt.imshow(wordcloud,interpolation="bilinear")
    plt.axis("off")
    plt.show()

main()
