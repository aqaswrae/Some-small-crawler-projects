# success

# 古诗文网需要输入四位验证码进行登录
# 使用超级鹰平台对验证码图片进行识别
# 先进行get请求得到验证码的图片链接，再对其发起请求，以二进制的形式保存在本地，使用超级鹰对本地的验证码图片进行识别，将得到的值传进参数里面，然后进行post请求成功登录

#对使用session的这一部分还存在疑问？？？？？？



import requests
from lxml import etree
from chaojiying_Python.chaojiying import Chaojiying_Client


class Spider():
    def __init__(self):
        self.post_url = 'https://so.gushiwen.cn/user/login.aspx'
        self.get_img_url = 'https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx'
        self.post_params = {
            '__VIEWSTATE': 'hpawdCPjZKGajClnvEZLkFC1n6JjzVnNPExFnZKxdQoHw18L/Vkgzp1ni2eIND93cDOmhrf2XZ/lM6kTn7zZupJuOfN3d4wNUmnNMJAPb9or4MY9Nd49n1XQmauhkTwSciVr/xWHGo5YnmHESbuZN0cGmbA=',
            '__VIEWSTATEGENERATOR': 'C93BE1AE',
            'from': 'http://so.gushiwen.cn/user/collect.aspx',
            'email': '875758159@qq.com',
            'pwd': 'gx123666000...',
            'code': 'TN33',
            'denglu': '登录'
        }
        self.headers = {
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }

        self.s = requests.session()

    def get_img(self):
        response = requests.get(self.get_img_url,headers=self.headers).text
        tree = etree.HTML(response)
        img_src = 'https://so.gushiwen.cn' + tree.xpath('//img[@id="imgCode"]/@src')[0]
        # print(img_src)
        img_data = self.s.get(img_src,headers=self.headers).content
        with open('code.jpg','wb')as f:
            f.write(img_data)
        result = self.get_img_code()
        self.post_login(result)


    def get_img_code(self):
        chaojiying = Chaojiying_Client('freeself', 'gx123666000...', '	949416')  # 用户中心>>软件ID 生成一个替换 96001
        im = open('code.jpg', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        # print(chaojiying.PostPic(im, 1004))
        result = chaojiying.PostPic(im, 1004)['pic_str']
        return result

    def post_login(self,result):
        self.post_params['code'] = result
        data = self.s.post(self.post_url,headers=self.headers,data=self.post_params)
        print(data.status_code)
        print(data.text)







if __name__ == '__main__':
    spider = Spider()
    spider.get_img()
    # spider.get_img_code()
