# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import json


class GbpostsPipeline:
    books = []

    def process_item(self, item, spider):
        self.books.append(item)

        with open(f'homework/hw5/{spider.name}.json', 'a', encoding='utf8') as f:
            json.dump(self.books, f)
