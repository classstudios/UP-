"""
 * @author        教室工作室 馆长
 * @date          2020/4/12
 * @version       1.0
"""
# requests.get示例
import requests
import re, random
import json, time
from bs4 import BeautifulSoup
"""
from wordcloud import WordCloud
import matplotlib.pyplot as plt  # 绘制图像的模块
import jieba  # jieba分词
"""

def get评论html(评论, UP主名, 评论html):
    count = 1
    fi = open(UP主名 + "评论.txt", "w", encoding="utf-8")
    while (True):
        评论html = 评论html + str(count)
        评论url = requests.get(评论html)
        if 评论url.status_code == 200:
            cont = json.loads(评论url.text)
        else:
            break
        if cont["data"]["replies"] != None:
            lengthRpy = len(cont["data"]["replies"])
        else:
            lengthRpy = 0
        if count == 1:
            try:
                lengthHot = len(cont["data"]["hots"])
                for i in range(lengthHot):
                    # 热门评论内容
                    hotMsg = cont["data"]["hots"][i]["content"]["message"]
                    fi.write(hotMsg + "\n")
                    评论 = hotMsg + 评论
                    leng = len(cont["data"]["hots"][i]["replies"])
                    for j in range(leng):
                        # 热门评论回复内容
                        hotMsgRp = cont["data"]["hots"][i]["replies"][j]["content"]["message"]
                        fi.write(hotMsgRp + "\n")
                        评论 = hotMsgRp + 评论
            except:
                pass
        if lengthRpy != 0:
            for i in range(lengthRpy):
                comMsg = cont["data"]["replies"][i]["content"]["message"]
                fi.write(comMsg + "\n")
                评论 = comMsg + 评论
                print("评论:", cont["data"]["replies"][i]["content"]["message"])
                # print(cont["data"]["replies"][i]["replies"])
                if cont["data"]["replies"][i]["replies"] != None:
                    leng = len(cont["data"]["replies"][i]["replies"])
                    for j in range(leng):
                        comMsgRp = cont["data"]["replies"][i]["replies"][j]["content"]["message"]
                        fi.write(comMsgRp + "\n")
                        评论 = comMsgRp + 评论


        else:
            break
        print("第%d页写入成功！" % count)
        count += 1
    fi.close()
    print(count - 1, "页评论写入成功！")


if __name__ == "__main__":
    my_headers = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "]
    # 随机选择一个Header伪装成浏览器
    head = {}
    head['User-Agent'] = random.choice(my_headers)
    评论 = ""
    UP主名 = input("请输入UP主名")
    html1 = requests.get('https://search.bilibili.com/upuser?keyword=' + UP主名 + "&page=1&order=0&order_sort=0",
                         headers=head)

    soup = BeautifulSoup(html1.text)
    print(soup)
    uid = soup.find(name='a', attrs={"class": "title"})
    分析数量 = soup.find(name='div', attrs={"class": "up-info clearfix"})
    # <div class="up-info clearfix"><span>稿件：27</span><span>粉丝：1046</span></div>
    分析数量 = str(分析数量)
    分析数量 = re.findall("<div.*?稿件：(.+)</span><span>粉丝.*", 分析数量)

    uid = str(uid)
    uid = re.findall('<a.*?href="//space.bilibili.com/(.+)f.*', uid)

    uid = uid[0][:-1]
    print("找到ID啦:", uid)

    分析数量 = int(分析数量[0])
    if 分析数量 > 100:
        分析数量 = 100
    else:
        分析数量 = 分析数量
    urlb = "https://api.bilibili.com/x/space/arc/search?mid=" + str(uid) + "&ps=" + str(
        分析数量) + "&pn=1&keyword=&order=click&jsonp=jsonp"
    print(urlb)
    html2 = requests.get(urlb, headers=head)
    print(str(html2.text))
    aid = []
    for i in range(0, 分析数量):
        aid.append(json.loads(str(html2.text))["data"]['list']['vlist'][i]['aid'])
        print(aid)
        评论html = "https://api.bilibili.com/x/v2/reply?type=1&oid=" + str(aid[i]) + "&pn="
        get评论html(评论, UP主名, 评论html)

    print(评论)

    # path_txt=UP主名+'评论.txt'
    # f = open(path_txt,'r',encoding='UTF-8').read()

    # 结巴分词，生成字符串，wordcloud无法直接生成正确的中文词云
    """
    cut_text = " ".join(jieba.cut(评论))
    # 1写出不想显示的词组
    exclude = {'UP', '回复', '这部', '为了', '视频', '还是', '我们', '你们', '他们', '它们', '因为', '因而', '所以', '如果', '那么', \
               '如此', '只是', '但是', '就是', '这是', '那是', '而是', '而且', '虽然', \
               '这些', '有些', '然后', '已经', '于是', '一种', '一个', '一样', '时候', \
               '没有', '什么', '这样', '这种', '这里', '不会', '一些', '这个', '仍然', '不是', \
               '自己', '知道', '可以', '看到', '那儿', '问题', '一会儿', '一点', '现在', '两个', \
               '三个', \
               }
    wordcloud = WordCloud(
        # 设置字体，不然会出现口字乱码，文字的路径是电脑的字体一般路径，可以换成别的
        font_path="C:/Windows/Fonts/simfang.ttf",
        # 设置了背景，宽高
        background_color="white", width=1000, height=880, stopwords=exclude).generate(cut_text)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
"""
