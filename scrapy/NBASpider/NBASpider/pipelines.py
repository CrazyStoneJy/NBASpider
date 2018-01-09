# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from NBASpider.items import *


class NbaspiderPipeline(object):
    def __init__(self):
        self.client = MongoClient('127.0.0.1', 27017)
        self.db = self.client['selfplay']

    def process_item(self, item, spider):
        if isinstance(item, PlayerInfoItem):
            table_player_info = self.db['player_info']
            table_player_info.update_one({'player_id': item['player_id']}, {'$set': dict(item)}, True, False)
        elif isinstance(item, SeasonDataItem):
            table_season = self.db['player_data']
            table_season.update_one({'player_id': item['player_id'], 'season': item['season'],'type': item['type']}, {'$set': dict(item)},
                                    True, False)
        return item

    def close_spider(self, spider):
        self.client.close()
