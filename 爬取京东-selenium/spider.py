#success--selenium爬取京东


import time,json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By #选择器
from selenium.webdriver.common.keys import Keys #键盘
from selenium.webdriver.support.wait import WebDriverWait #等待页面加载完毕，寻找某些元素
from selenium.webdriver.support import expected_conditions as EC #等待指定标签加载完毕
from selenium.webdriver.chrome.options import Options #无头模式
#添加无头模式让京东、淘宝等网站识别不了是一个selenium自动化程序


class Jd():
    def __init__(self):
        self.url = 'https://www.jd.com'
        self.options = webdriver.ChromeOptions()#配置文件对象
        self.options.add_experimental_option('excludeSwitches',['enable-automation'])#写入参数
        # 驱动浏览器
        self.brower = webdriver.Chrome(options=self.options)

    def get_data(self):
        self.brower.get(self.url)
        wait = WebDriverWait(self.brower, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="mod_service"]')))
        # 寻找输入框，查找iphone商品(等待页面加载完成之后)
        input_text = self.brower.find_element(By.CSS_SELECTOR, 'input')
        input_text.send_keys('iphone')  # 向输入框中输入
        time.sleep(2)
        # self.brower.find_element(By.XPATH, '//button[@class="button"]').click()  # 找到搜索的按钮并点击
        input_text.send_keys(Keys.ENTER)#按下回车
        time.sleep(3)
        # html_code = self.brower.page_source
        # print(html_code)#复制页面的数据到得到的源码中搜不到，因为页面加载需要时间
        # return html_code
        self.to_bottom()


    #将页面滑到底部，因为是异步加载，滑到最底部才会显示出全部的商品信息,然后获取网页源码
    def to_bottom(self):
        index_page = 1
        while True:
            print(f'正在爬取第{index_page}页')
            self.brower.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(2)
            data = self.brower.page_source
            self.parse_data(data)
            wait = WebDriverWait(self.brower, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.pn-next')))
            try:
                self.brower.find_element(By.CSS_SELECTOR,'#J_bottomPage > span.p-num > a.pn-next').click()
                time.sleep(2)
                index_page += 1
            except Exception as e:
                print(e)
                print('数据爬取完毕')
                break

    def parse_data(self,data):
        soup = BeautifulSoup(data,'lxml')
        names = soup.select('div #J_goodsList .p-name em')
        prices = soup.select('div #J_goodsList .p-price i')#css选择器
        shops = soup.select('div #J_goodsList .p-shop')
        commodity_info = {}
        for name,price,shop in zip(names,prices,shops):
            n = name.get_text().replace('拍拍','').strip()
            p = price.get_text()
            s = shop.get_text().replace('\n','')
            commodity_info['商品名'] = n
            commodity_info['价格'] = p
            commodity_info['店铺名'] = s
            print(n)
            print(p)
            print(s)
            print('----------------')
            with open('goods.json','a',encoding='utf--8')as f:
                f.write(json.dumps(commodity_info,ensure_ascii=False) + ',\n')


        print(len(shops))


    def run(self):
        self.get_data()



if __name__ == '__main__':
    jd = Jd()
    jd.run()