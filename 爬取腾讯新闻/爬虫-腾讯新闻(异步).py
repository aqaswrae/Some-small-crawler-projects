# success
# 所有的数据都在xhr文件中，list?..
# 不像网易新闻那样，刚开始的数据在document里，后边的数据在xhr文件里

import requests,sys
from jsonpath import jsonpath
from openpyxl import workbook


class Spider():
    def __init__(self):
        self.url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57',
            'referer': 'https: // news.qq.com /'
        }
        self.wb = workbook.Workbook()  # 创建Excel对象
        self.ws = self.wb.active  # 激活当前表
        self.ws.append(['标题', '链接', '媒体'])  # 添加表头，必须是以列表的形式传参

    #发起请求
    def get_data(self,params):
        response = requests.get(self.url,headers=self.headers,params=params).json()
        # print(response)
        return response

    #解析数据
    def parse_data(self,data):
        titles = jsonpath(data,'$..title')#标题
        links = jsonpath(data,'$..url')
        media_names = jsonpath(data,'$..media_name')#出版社
        for title,link,media_name in zip(titles,links,media_names):
            # print('标题',title)
            # print('链接',link)
            # print('出版社',media_name)
            self.save_data(title,link,media_name)

        self.wb.save('腾讯新闻.xlsx')  # 运行并保存


    #保存数据
    def save_data(self,title,link,media_name):
        # lst = [title,link,media_name]
        self.ws.append([title,link,media_name])


    def run(self):
        for i in range(0,141,20):
            self.params = {
                'sub_srv_id': '24hours',
                'srv_id': 'pc',
                'offset': i,
                'limit': '20',
                'strategy': '1',
                'ext': '{"pool":["top","hot"],"is_filter":7,"check_type":true}'
            }
            json_data = self.get_data(self.params)
            self.parse_data(json_data)


if __name__ == '__main__':
    me = Spider()
    me.run()




