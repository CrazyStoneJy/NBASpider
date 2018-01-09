# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NbaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PlayerInfoItem(scrapy.Item):
    nick_name = scrapy.Field()
    user_name = scrapy.Field()
    english_name = scrapy.Field()
    play_position = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    birthday = scrapy.Field()
    birth_city = scrapy.Field()
    high_school = scrapy.Field()
    shirt_number = scrapy.Field()
    draft = scrapy.Field()
    salary = scrapy.Field()
    baidu_pedia = scrapy.Field()
    wiki_pedia = scrapy.Field()
    university = scrapy.Field()
    player_id = scrapy.Field()
    url = scrapy.Field()

    pass

class SeasonDataItem(scrapy.Item):
    # 赛季
    season = scrapy.Field()
    # 球队
    team = scrapy.Field()
    # 出场
    attend = scrapy.Field()
    # 首发
    starting_linup = scrapy.Field()
    # 场均上场时间
    play_duration = scrapy.Field()
    # 总命中率
    percentage = scrapy.Field()
    # 总命中个数
    field_goal = scrapy.Field()
    # 总出手数
    shoot = scrapy.Field()
    # 三分命中率
    three_percentage = scrapy.Field()
    # 三分命中数
    three_field_goal = scrapy.Field()
    # 三分出手数
    three_shoot = scrapy.Field()
    # 罚球命中率
    free_throw_percentage = scrapy.Field()
    # 罚球命中数
    free_throw_field_goal = scrapy.Field()
    # 罚球出手数
    free_throw_shoot = scrapy.Field()
    # 总篮板数
    rebound = scrapy.Field()
    # 前场板(进攻篮板)
    offensive_rebound = scrapy.Field()
    # 后场板(防守篮板)
    defensive_rebound = scrapy.Field()
    # 助攻
    assist = scrapy.Field()
    # 抢断
    steal = scrapy.Field()
    # 盖帽
    block = scrapy.Field()
    # 失误
    turnover = scrapy.Field()
    # 犯规
    fault = scrapy.Field()
    # 得分
    scoring = scrapy.Field()
    # 胜利
    victory = scrapy.Field()
    # 失败
    defeat = scrapy.Field()
    # player id
    player_id = scrapy.Field()
    # type {0 season 1 playoff 2 allstar}
    type = scrapy.Field()

class UrlRecordItem(scrapy.Item):
    url = scrapy.Field()




