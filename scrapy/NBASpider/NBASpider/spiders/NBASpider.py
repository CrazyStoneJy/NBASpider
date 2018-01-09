# !/usr/bin/python3
# -*- encoding:utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request
import logging
from NBASpider.items import *
from lxml import etree


class NBASpider(CrawlSpider):
    name = 'nba'
    allowed_domain = 'stat-nba.com'
    start_urls = ['http://www.stat-nba.com/player/264.html']
    season_url = 'http://www.stat-nba.com/player/stat_box/{player_id}_season.html'
    playoff_url = 'http://www.stat-nba.com/player/stat_box/{player_id}_playoff.html'
    allstar_url = 'http://www.stat-nba.com/player/stat_box/{player_id}_allstar.html'

    rules = (
        Rule(LinkExtractor(allow='player/\d*.html'), follow=True, callback='parse_item'),
    )

    def __init__(self):
        super(NBASpider, self).__init__()
        self.infoDict = self.info_dict()

    def parse_item(self, response):
        print(response.url)
        try:
            if response is not None:
                selector = etree.HTML(response.text)
                user_name = selector.xpath('//*[@id="background"]/div[4]/div[2]/text()')
                # baidu_pedia = selector.xpath('//*[@id="background"]/div[4]/div[2]/a[1]')
                # wiki_pedia = selector.xpath('//*[@id="background"]/div[4]/div[2]/a[2]')
                all_div = selector.xpath('//*[@id="background"]/div[4]/div[3]/div')
                all_div_text = selector.xpath('//*[@id="background"]/div[4]/div[3]/div/text()')
                infoItem = PlayerInfoItem()
                if self.not_empty(all_div):
                    for i, div in enumerate(all_div):
                        key = div.findtext('div')
                        value = all_div_text[i]
                        print(value)
                        en_key = self.get_en_key(key)
                        if en_key is not None:
                            infoItem[en_key] = self.trim(value)
                if self.not_empty(user_name):
                    infoItem['user_name'] = self.trim(user_name[0])
                # if self.not_empty(baidu_pedia):
                #     infoItem['baidu_pedia'] = baidu_pedia[0].strip()
                # if self.not_empty(wiki_pedia):
                #     infoItem['wiki_pedia'] = wiki_pedia[0].strip()
                array = response.url.split('/')
                if array is not None and len(array) > 0:
                    number_array = array[-1].split('.')
                    if number_array is not None and len(number_array) > 0:
                        player_id = int(number_array[0])
                        infoItem['player_id'] = player_id
                        print('>>>>>>>hello>>>>>>>>')
                        self.crawl_game_data(player_id)

                infoItem['url'] = response.url
                print(infoItem)
                yield infoItem
            else:
                print('response is none')
        except Exception as e:
            logging.exception(e)

    def crawl_game_data(self, player_id):
        current_season_url = self.season_url.format(player_id=player_id)
        print('>>>>>>>>>>>>>>>>>>>')
        print(current_season_url)
        print('>>>>>>>>>>>>>>>>>>>')
        # current_playoff_url = self.playoff_url.format(player_id=player_id)
        # current_allstar_url = self.allstar_url.format(player_id=player_id)
        yield Request(current_season_url, callback=self.parse_season, meta={'player_id': player_id})
        # yield Request(current_playoff_url, callback=self.parse_playoff)
        # yield Request(current_allstar_url, callback=self.parse_allstar)

    def parse_season(self, response):
        try:
            if response is not None:
                selector = etree.HTML(response.text)
                trs = selector.xpath('//*[@id="stat_box_tot"]/tbody/tr')
                player_id = response.meta['player_id']
                if self.not_empty(trs):
                    for tr in trs:
                        season = tr.findtext('td[2]/a')
                        team = tr.findtext('td[3]/a')
                        attend = tr.findtext('td[4]')
                        first_lineup = tr.findtext('td[5]')
                        play_time = tr.findtext('td[6]')
                        percentage = tr.findtext('td[7]')
                        field_goal = tr.findtext('td[8]')
                        shoot = tr.findtext('td[9]')
                        three_percentage = tr.findtext('td[10]')
                        three_field_goal = tr.findtext('td[11]')
                        three_shoot = tr.findtext('td[12]')
                        free_throw_percentage = tr.findtext('td[13]')
                        free_throw_field_goal = tr.findtext('td[14]')
                        free_throw_shoot = tr.findtext('td[15]')
                        rebound = tr.findtext('td[16]')
                        offensive_rebound = tr.findtext('td[17]')
                        defensive_rebound = tr.findtext('td[18]')
                        assist = tr.findtext('td[19]')
                        steal = tr.findtext('td[20]')
                        block = tr.findtext('td[21]')
                        turnover = tr.findtext('td[22]')
                        fault = tr.findtext('td[23]')
                        scoring = tr.findtext('td[24]')
                        victory = tr.findtext('td[25]')
                        defeat = tr.findtext('td[26]')

                        item = SeasonDataItem()
                        if season is not None:
                            item['season'] = season.strip()
                        if team is not None:
                            item['team'] = season.strip()
                        if attend is not None:
                            item['attend'] = int(attend.strip())
                        if first_lineup is not None:
                            item['starting_linup'] = int(first_lineup.strip())
                        if play_time is not None:
                            item['play_duration'] = int(play_time.strip())
                        if percentage is not None:
                            item['percentage'] = float(percentage[:-1])
                        if field_goal is not None:
                            item['field_goal'] = int(field_goal.strip())
                        if shoot is not None:
                            item['shoot'] = int(shoot.strip())
                        if three_percentage is not None:
                            item['three_percentage'] = float(three_percentage.strip())
                        if three_field_goal is not None:
                            item['three_field_goal'] = int(three_field_goal)
                        if three_shoot is not None:
                            item['three_shoot'] = int(three_shoot)
                        if free_throw_percentage is not None:
                            item['free_throw_percentage'] = float(free_throw_percentage[:-1])
                        if free_throw_field_goal is not None:
                            item['free_throw_field_goal'] = int(free_throw_field_goal.strip())
                        if free_throw_shoot is not None:
                            item['free_throw_shoot'] = int(free_throw_shoot.strip())
                        if rebound is not None:
                            item['rebound'] = int(rebound.strip())
                        if offensive_rebound is not None:
                            item['offensive_rebound'] = int(offensive_rebound.strip())
                        if defensive_rebound is not None:
                            item['defensive_rebound'] = int(defensive_rebound.strip())
                        if assist is not None:
                            item['assist'] = int(assist.strip())
                        if steal is not None:
                            item['steal'] = int(steal.strip())
                        if block is not None:
                            item['block'] = int(block.strip())
                        if turnover is not None:
                            item['turnover'] = int(turnover.strip())
                        if fault is not None:
                            item['scoring'] = int(scoring.strip())
                        if victory is not None:
                            item['victory'] = int(victory.strip())
                        if defeat is not None:
                            item['defeat'] = int(defeat.strip())
                        item['player_id'] = player_id
                        item['type'] = 0
                        yield item
            else:
                print('%s is none' % response.url)
        except Exception as e:
            logging.exception(e)
        pass

    def parse_playoff(self, response):
        pass

    def parse_allstar(self, response):
        pass

    def not_empty(self, list_obj):
        return list_obj is not None and len(list_obj) > 0

    def trim(self, string):
        if string is not None:
            return string.replace('\n', '').replace('\r', '').strip()

    def info_dict(self):
        info_dict = dict()
        info_dict['位　　置:'] = 'play_position'
        info_dict['全　　名:'] = 'english_name'
        info_dict['身　　高:'] = 'height'
        info_dict['体　　重:'] = 'weight'
        info_dict['出生日期:'] = 'birthday'
        info_dict['出生城市:'] = 'birth_city'
        info_dict['高　　中:'] = 'high_school'
        info_dict['大　　学:'] = 'university'
        info_dict['选秀情况:'] = 'draft'
        info_dict['当前薪金:'] = 'salary'
        info_dict['球衣号码:'] = 'shirt_number'
        return info_dict

    def get_en_key(self, key):
        if key in self.infoDict.keys():
            return self.infoDict[key]
        else:
            print('unknow key:' + key)
            # return 'unkown'

