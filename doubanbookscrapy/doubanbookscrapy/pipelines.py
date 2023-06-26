# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter
import pymysql


class DoubanbookscrapyPipeline:
    def __init__(self):
        self.file = open('doubannewbook.json','a',encoding='utf-8')

    def process_item(self, item, spider):
        dict_item = dict(item)
        #保存为json数据
        json_data = json.dumps(dict_item,ensure_ascii=False) + ',\n'
        self.file.write(json_data)
        return item

    def __del__(self):#del是当整个函数运行完之后再调用
        self.file.close()

class DoubanbookscrapyPipelineMysql:#写好之后，要去settings.py文件对应的位置ITEM_PIPELINES设置好
    def __init__(self):
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            db='scrapy-spider',
            charset='utf8'
        )
        self.cur = self.db.cursor()

    def process_item(self, item, spider):
        dict_item = dict(item)
        try:
            sql = 'insert into doubanbook(name,content,link,txt) values(%s,%s,%s,%s)'
            self.cur.execute(sql,[item['name'],item['content'],item['link'],item['txt'],])
            self.db.commit()
            print('保存成功')
        except Exception as e:
            print(e)
            self.db.rollback()

        return item

    def close_spider(self):#scrapy内置的方法，当所属类运行完成之后，这个方法就会运行，将cur和db关掉
        self.cur.close()
        self.db.close()