#自认为success，其实保存数据的功能还未实现。不知道该以何种形式对数据进行存储，就是存入的格式。。
#以后运行该程序时，记得更新一下cookie
#整成一个活的接口
import csv

import requests,re,time,random,sys
from jsonpath import jsonpath



class Spider():
    def __init__(self):
        self.first_url = 'https://weibo.com/ajax/statuses/buildComments'
        # self.second_url = 'https://weibo.com/ajax/statuses/buildComments'
        self.first_params = {
            'flow':None,
            'is_reload': '1',
            'id': '4907163765968907',
            'is_show_bulletin': '2',
            'is_mix': '0',
            'max_id':None,
            'count': '10',
            'uid': '2172061270',
            'fetch_level': 0
                            }
        self.second_params = {
            'flow':0,
            'is_reload': 1,
            'id': 4907163882885333,
            'is_show_bulletin': 2,
            'is_mix': 1,
            'fetch_level': 1,
            'max_id': 0,
            'count': 20,
            'uid': 2172061270
        }
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
                        'Cookie':'SINAGLOBAL=6827779990380.782.1679556633123; XSRF-TOKEN=Ljlah3VE3aJ4-RTCJ2L9HCdG; SUB=_2A25JcRsNDeRhGeNJ6FQY-CnKzDqIHXVqBwvFrDV8PUNbmtAGLUTjkW9NS8EkwS1RjxmcG6a2HuwnBN1c1IYJojCQ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh478-llwceQUYybxsb2KKX5JpX5KzhUgL.Fo-Ne0q41hMcS0q2dJLoIEXLxK-LBKqL1hzLxKBLB.BL1K-LxKML12zL1hzLxKqL1heLBoeLxKqL1-zLBozt; ALF=1716952797; SSOLoginState=1685416797; _s_tentry=weibo.com; Apache=7125770374805.486.1685416894778; ULV=1685416894847:3:1:1:7125770374805.486.1685416894778:1679965409068; PC_TOKEN=f955505f22; WBPSESS=ihNrCUzIK5bMw3CG01-xjfkTsNN9mmeB3aFCZSzQJq6dchMit-7Jw3LsQ8nwT6pIUFsuk4dtAxD35hQWP0MkmX2r3crzrCHLeKvyghuBm0AQcAVDZgma75JHl7CaJW8T7gn0KFqwLwpE7KxNl4es-A==',
                        'Referer':'https://weibo.com/2172061270/N30msp2MH'
        }
    #爬取一级评论
    def get_first_comments(self,url):
        response = requests.get(url,headers=self.headers,params=self.first_params).json()
        # print(response)
        data = jsonpath(response,'$.data')[0]
        authors = jsonpath(response,'$..data..user.screen_name')#用户
        comments = jsonpath(response,'$..data[0:20].text')#评论 data[0:20]也可用 data.*来表示，*表示匹配所有元素节点
        next_max_id = jsonpath(response,'$.max_id')[0]#下一个数据包的max_id    #int类型
        next_ids = jsonpath(response,'$..data[0:20].id')
        # print(authors)
        # print(comments)
        # print(next_max_id)
        # print(type(next_max_id))
        # print(next_ids)
        if not data:
            if next_max_id == 0:
                print('一级评论爬取完毕')
                sys.exit(0)
            else:
                print('data为空')
                self.first_params['max_id'] = next_max_id
                time.sleep(random.randint(3,6))
                self.get_first_comments(url)
        else:
            # print(data)
            self.first_params['flow'] = 0
            for author,comment,iid in zip(authors,comments,next_ids):
                comment = re.sub('<.*?>','',comment)#除去表情的那些内容
                # 一级评论
                print('一级评论：')
                print('用户：',author,'------',comment)
                time.sleep(random.randint(3,6))
                self.second_params['max_id'] = 0
                self.get_second_comments(iid)
            if next_max_id == 0:
                print('一级评论爬取完毕')
                sys.exit(0)
            self.first_params['max_id'] = next_max_id
            time.sleep(random.randint(3,6))
            self.get_first_comments(url)


    #爬取二级评论
    def get_second_comments(self,id):
        self.second_params['id'] = id
        response = requests.get(self.first_url,headers=self.headers,params=self.second_params).json()
        # print(response)
        data = jsonpath(response, '$.data')[0]
        # print(data)
        authors = jsonpath(response, '$..data[0:20].user.screen_name')  # 用户
        comments = jsonpath(response, '$..data[0:20].text')  # 评论
        next_max_id = jsonpath(response, '$.max_id')[0]
        # print(authors)
        # print(comments)
        # print(next_max_id)
        if not data:
            print('二级评论以空')
            return 0
        else:
            for author,comment in zip(authors,comments):
                comment = re.sub('<.*?>','',comment)#除去表情的那些内容
                # 二级评论
                print('二级评论：')
                print('用户：',author,'------',comment)
                time.sleep(random.randint(0,2))
            if next_max_id == 0:
                return 0
            self.second_params['max_id'] = next_max_id
            self.get_second_comments(id)




    def save_data(self):
        # csv_w.writerow()
        pass

    def run(self):
        self.get_first_comments(self.first_url)
        # self.get_second_comments()


if __name__ == '__main__':
    # with open('微博评论.csv','w',newline='',encoding='utf-8')as f:
    #     csv_w = csv.writer(f)
    #     csv_w.writerow(['一级评论','二级评论'])
    s = Spider()
    #若是要整成一个活的接口的话，在run方法里添加两个或三个参数，url、headers、params，用户可以自己简单的调用，将某条微博的url传入即可。
    s.run()