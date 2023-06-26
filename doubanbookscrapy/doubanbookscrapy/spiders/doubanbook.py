import scrapy
from doubanbookscrapy.items import DoubanbookscrapyItem


class DoubanbookSpider(scrapy.Spider):
    name = "doubanbook"
    allowed_domains = ["book.douban.com"]
    start_urls = ["https://book.douban.com/latest"]

    def parse(self, response):
        names = response.xpath('//ul[@class="chart-dashed-list"]/li/div[@class="media__body"]/h2/a/text()').extract()
        contents = response.xpath('//ul[@class="chart-dashed-list"]/li/div[@class="media__body"]/p[1]/text()').extract()
        links = response.xpath('//ul[@class="chart-dashed-list"]/li/div[@class="media__body"]/h2/a/@href').extract()

        for name,content,link in zip(names,contents,links):
            item = DoubanbookscrapyItem()
            item['name'] = name
            item['content'] = content.strip()
            item['link'] = link
            #将数据返回给引擎
            # yield item
            yield scrapy.Request(url=item['link'],callback=self.parse_detail,meta={'item':item})

        #翻页
        page_url = response.xpath('//span[@class="next"]/a/@href').extract_first()
        #拼接完整的链接
        next_url = response.urljoin(page_url)
        # print('下一页的链接：',next_url)
        #构造请求对象，返回给引擎
        yield scrapy.Request(url=next_url,callback=self.parse)


    #接下来用得到的书籍的链接来获取书籍详情页的内容简介，因为是不同的处理逻辑，所以我们要定义一个新的函数来处理详情页的数据
    def parse_detail(self,response):
        #内容简介
        t = response.xpath('//span[@class="all hidden"]//div[@class="intro"]//p/text()').extract()
        # print(t)
        item = response.meta['item']
        item['txt'] = ''.join(t)
        print(item)
        yield item
