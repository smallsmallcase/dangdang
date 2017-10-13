# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import pymysql
from dangdang import settings


class Drop(object):
    def __init__(self):
        self.itemset = set()

    def process_item(self, item, spider):
        if not item['name']:
            DropItem('isempty')
        elif str(item['name']) in self.itemset:
            DropItem('repete')
        else:
            self.itemset.add(str(item['name']))
            return item


class DangdangPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8'
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        name = item['name'][0]
        price = item['price'][0]
        print(name, price)
        print()
        try:
            sql = 'insert into comp2(name, price)VALUES (%s, %s)'
            data = name, price
            self.cursor.execute(sql, data)
            self.connect.commit()
        except Exception as err:
            print(err)
        return item

