import scrapy
from lianjiascrapy.items import LianjiascrapyItem

class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["qd.lianjia.com"]
    start_urls = ["https://qd.lianjia.com/zufang/"]

    def parse(self, response):
        names = response.xpath('//div[@class="content__list"]/div/a/@title').extract()
        prices = response.xpath('//div[@class="content__list"]/div//em/text()').extract()
        links = response.xpath('//div[@class="content__list"]/div/a/@href').extract()
        total_page = response.xpath('//div[@class="content__pg"]/@data-totalpage').extract_first()#数据总页数total_page
        current_page = response.xpath('//div[@class="content__pg"]/@data-curpage').extract_first()#当前是第几页

        for name,price,link in zip(names,prices,links):
            #导入item.py中的类，然后实例化一个对象，将获取的数据传给item，键名必须和字段名统一
            item = LianjiascrapyItem()
            item['name'] = name.strip()
            item['price'] = price
            item['link'] = response.urljoin(link)
            # 将组建好的字典类型的数据通过yield返回给引擎，再由引擎返回给pipelines文件
            yield item
        #翻页。返回的网页源码中没有下一页的这个a标签，只有一个div标签，获取div标签的属性来进行翻页操作
        # 将翻页的请求对象写在if语句下，运行时只会给第二页的url why???
        if int(current_page) < int(total_page):
            #拼接完整的下一页的url
            next_url = 'https://qd.lianjia.com/zufang/pg' + str(int(current_page)+1)
            print('下一页的链接为：',next_url)
            yield scrapy.Request(url=next_url,callback=self.parse)
        else:
            print('不满足')

        #第二种方法就是获取到ul标签中所有的页面的url，循环挨个读取出来，构造请求对象返回给引擎

