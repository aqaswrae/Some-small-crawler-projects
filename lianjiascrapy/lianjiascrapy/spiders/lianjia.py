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

        for name,price,link in zip(names,prices,links):
            #导入item.py中的类，然后实例化一个对象，将获取的数据传给item，键名必须和字段名统一
            item = LianjiascrapyItem()
            item['name'] = name.strip()
            item['price'] = price
            item['link'] = response.urljoin(link)
            # 将组建好的字典类型的数据通过yield返回给引擎，再由引擎返回给pipelines文件
            yield item

