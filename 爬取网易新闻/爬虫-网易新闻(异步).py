# 网易新闻是异步刷新数据
'''
刚开始的数据在document文件中，后边的数据异步刷新在xhr文件中
'''

# success

import requests, json, re, csv
from jsonpath import jsonpath



class FirstSpider():
    def __init__(self):
        self.url = 'https://m.163.com/touch/news/'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36 Edg/113.0.1774.50'}

    def get_data(self, url, headers):
        response = requests.get(url, headers=headers).text
        content = re.findall('<script>window.__INITIAL_STATE__=(.*?)\(function', response, re.S)
        # print(content[0])
        return content[0][:-1]

    def parse_data(self, data):
        json_data = json.loads(data)
        # print(json_data)
        titles = jsonpath(json_data, '$..title')
        links = jsonpath(json_data, '$..link')
        sources = jsonpath(json_data, '$..source')
        for title, link, source in zip(titles, links, sources):
            print('标题：', title)
            print('链接：', link)
            print('来源：', source)
            self.save_data(title, link, source)

    def save_data(self, title, link, source):
        csx_w.writerow([title, link, source])

    def run(self):
        json_data = self.get_data(self.url, self.headers)
        # print(json_data)
        self.parse_data(json_data)


class SecondSpider():
    def __init__(self):
        # self.url = 'https://m.163.com/touch/reconstruct/article/list/BBM54PGAwangning/36-8.html'
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36}'}

    def get_data(self,url):
        response = requests.get(url,headers=self.headers).text
        # print(response.replace('artiList(','')[:-1])
        data = response.replace('artiList(','')[:-1]
        json_data = json.loads(data)
        # print(json_data)
        return json_data

    def parse_data(self,data):
        titles = jsonpath(data,'$..title')
        links = jsonpath(data,'$..url')
        sources = jsonpath(data,'$..source')
        for title,link,source in zip(titles,links,sources):
            print('标题：', title)
            print('链接：', link)
            print('来源：', source)
            self.save_data(title, link, source)

    def save_data(self, title, link, source):
        csx_w.writerow([title, link, source])

    def run(self,url):
        json_data = self.get_data(url)
        self.parse_data(json_data)

if __name__ == '__main__':
    with open('wangyinews.csv', 'w', newline='', encoding='utf-8') as f:
        csx_w = csv.writer(f)  # csv文件对象
        csx_w.writerow(['标题', '链接', '来源'])
        fspider = FirstSpider()
        fspider.run()
        sspider = SecondSpider()
        for i in range(36,200,8):
            url = f'https://m.163.com/touch/reconstruct/article/list/BBM54PGAwangning/{i}-8.html'
            sspider.run(url)








# ^((\(\d{2,3}\))|(\d{3}\-))?((13\d{9})|(15[389]\d{8}))$
