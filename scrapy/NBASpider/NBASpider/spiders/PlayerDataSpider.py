# !/usr/bin/python3
# -*- encoding:utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request
import logging
from scrapy import Spider
from NBASpider.items import *
from lxml import etree
from pymongo import MongoClient
import traceback


class PlayerDataSpider(Spider):
    name = 'data'
    season_url = 'http://www.stat-nba.com/player/stat_box/{player_id}_season.html'
    playoff_url = 'http://www.stat-nba.com/player/stat_box/{player_id}_playoff.html'
    allstar_url = 'http://www.stat-nba.com/player/stat_box/{player_id}_allstar.html'

    # start_urls = ['http://www.stat-nba.com/player/264.html']

    def start_requests(self):
        result = self.get_id_from_mongo()
        for r in result:
            player_id = r['player_id']
            print(player_id)
            if player_id is not None:
                current_season_url = self.allstar_url.format(player_id=player_id)
                yield Request(current_season_url, callback=self.parse_allstar, meta={'player_id': player_id})

    # def crawl_game_data(self, player_id):
    #     current_season_url = self.season_url.format(player_id=player_id)
    #     print('>>>>>>>>>>>>>>>>>>>')
    #     print(current_season_url)
    #     print('>>>>>>>>>>>>>>>>>>>')
    #     # current_playoff_url = self.playoff_url.format(player_id=player_id)
    #     # current_allstar_url = self.allstar_url.format(player_id=player_id)
    #     yield Request(current_season_url, callback=self.parse_season, meta={'player_id': player_id})
        # yield Request(current_playoff_url, callback=self.parse_playoff)
        # yield Request(current_allstar_url, callback=self.parse_allstar)

    # 解析season allstar 的数据方法(他们数据格式一致)
    def parse_season(self, response):
        try:
            if response is not None:
                selector = etree.HTML(response.text)
                trs = selector.xpath('//*[@id="stat_box_tot"]/tbody/tr[@class="sort"]')
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
                            item['attend'] = self.parse_int(attend.strip())
                        if first_lineup is not None:
                            item['starting_linup'] = self.parse_int(first_lineup.strip())
                        if play_time is not None:
                            item['play_duration'] = self.parse_int(play_time.strip())
                        if percentage is not None:
                            item['percentage'] = self.parse_float(percentage.strip())
                        if field_goal is not None:
                            item['field_goal'] = self.parse_int(field_goal.strip())
                        if shoot is not None:
                            item['shoot'] = self.parse_int(shoot.strip())
                        if three_percentage is not None:
                            item['three_percentage'] = self.parse_float(three_percentage.strip())
                        if three_field_goal is not None:
                            item['three_field_goal'] = self.parse_int(three_field_goal)
                        if three_shoot is not None:
                            item['three_shoot'] = self.parse_int(three_shoot)
                        if free_throw_percentage is not None:
                            item['free_throw_percentage'] = self.parse_float(free_throw_percentage.strip())
                        if free_throw_field_goal is not None:
                            item['free_throw_field_goal'] = self.parse_int(free_throw_field_goal.strip())
                        if free_throw_shoot is not None:
                            item['free_throw_shoot'] = self.parse_int(free_throw_shoot.strip())
                        if rebound is not None:
                            item['rebound'] = self.parse_int(rebound.strip())
                        if offensive_rebound is not None:
                            item['offensive_rebound'] = self.parse_int(offensive_rebound.strip())
                        if defensive_rebound is not None:
                            item['defensive_rebound'] = self.parse_int(defensive_rebound.strip())
                        if assist is not None:
                            item['assist'] = self.parse_int(assist.strip())
                        if steal is not None:
                            item['steal'] = self.parse_int(steal.strip())
                        if block is not None:
                            item['block'] = self.parse_int(block.strip())
                        if turnover is not None:
                            item['turnover'] = self.parse_int(turnover.strip())
                        if fault is not None:
                            item['scoring'] = self.parse_int(scoring.strip())
                        if victory is not None:
                            item['victory'] = self.parse_int(victory.strip())
                        if defeat is not None:
                            item['defeat'] = self.parse_int(defeat.strip())
                        item['player_id'] = player_id
                        item['type'] = 0
                        yield item
            else:
                print('%s is none' % response.url)
        except Exception as e:
            logging.exception(e)
            msg = traceback.format_exc()
            with open('error.log', 'a+') as f:
                f.write('url:' + response.url)
                f.write('\n')
                f.write('three_percentage>' + three_percentage + '<')
                f.write('\n')
                f.write(msg)
        pass

    def parse_int(self, string):
        # print('>>>>>>>>>')
        # print(string)
        # print('>>>>>>>>')
        if string is not None and string != ' ' and string != '':
            return int(string)
        else:
            return 0

    def parse_float(self, string):
        if string is None and string != ' ' and string != '':
            return float(string[:-1].strip())
        else:
            return 0

    def parse_playoff(self, response):
        try:
            if response is not None:
                selector = etree.HTML(response.text)
                trs = selector.xpath('//*[@id="stat_box_tot"]/tbody/tr[@class="sort"]')
                player_id = response.meta['player_id']
                if self.not_empty(trs):
                    for tr in trs:
                        season = tr.findtext('td[2]/a')
                        team = tr.findtext('td[3]/a')
                        attend = tr.findtext('td[4]')
                        # first_lineup = tr.findtext('td[5]')
                        play_time = tr.findtext('td[5]')
                        percentage = tr.findtext('td[6]')
                        field_goal = tr.findtext('td[7]')
                        shoot = tr.findtext('td[8]')
                        three_percentage = tr.findtext('td[9]')
                        three_field_goal = tr.findtext('td[10]')
                        three_shoot = tr.findtext('td[11]')
                        free_throw_percentage = tr.findtext('td[12]')
                        free_throw_field_goal = tr.findtext('td[13]')
                        free_throw_shoot = tr.findtext('td[14]')
                        rebound = tr.findtext('td[15]')
                        offensive_rebound = tr.findtext('td[16]')
                        defensive_rebound = tr.findtext('td[17]')
                        assist = tr.findtext('td[18]')
                        steal = tr.findtext('td[19]')
                        block = tr.findtext('td[20]')
                        turnover = tr.findtext('td[21]')
                        fault = tr.findtext('td[22]')
                        scoring = tr.findtext('td[23]')
                        victory = tr.findtext('td[24]')
                        defeat = tr.findtext('td[25]')

                        item = SeasonDataItem()
                        if season is not None:
                            item['season'] = season.strip()
                        if team is not None:
                            item['team'] = season.strip()
                        if attend is not None:
                            item['attend'] = self.parse_int(attend.strip())
                        # if first_lineup is not None:
                        #     item['starting_linup'] = self.parse_int(first_lineup.strip())
                        if play_time is not None:
                            item['play_duration'] = self.parse_int(play_time.strip())
                        if percentage is not None:
                            item['percentage'] = self.parse_float(percentage.strip())
                        if field_goal is not None:
                            item['field_goal'] = self.parse_int(field_goal.strip())
                        if shoot is not None:
                            item['shoot'] = self.parse_int(shoot.strip())
                        if three_percentage is not None:
                            item['three_percentage'] = self.parse_float(three_percentage.strip())
                        if three_field_goal is not None:
                            item['three_field_goal'] = self.parse_int(three_field_goal)
                        if three_shoot is not None:
                            item['three_shoot'] = self.parse_int(three_shoot)
                        if free_throw_percentage is not None:
                            item['free_throw_percentage'] = self.parse_float(free_throw_percentage.strip())
                        if free_throw_field_goal is not None:
                            item['free_throw_field_goal'] = self.parse_int(free_throw_field_goal.strip())
                        if free_throw_shoot is not None:
                            item['free_throw_shoot'] = self.parse_int(free_throw_shoot.strip())
                        if rebound is not None:
                            item['rebound'] = self.parse_int(rebound.strip())
                        if offensive_rebound is not None:
                            item['offensive_rebound'] = self.parse_int(offensive_rebound.strip())
                        if defensive_rebound is not None:
                            item['defensive_rebound'] = self.parse_int(defensive_rebound.strip())
                        if assist is not None:
                            item['assist'] = self.parse_int(assist.strip())
                        if steal is not None:
                            item['steal'] = self.parse_int(steal.strip())
                        if block is not None:
                            item['block'] = self.parse_int(block.strip())
                        if turnover is not None:
                            item['turnover'] = self.parse_int(turnover.strip())
                        if fault is not None:
                            item['scoring'] = self.parse_int(scoring.strip())
                        if victory is not None:
                            item['victory'] = self.parse_int(victory.strip())
                        if defeat is not None:
                            item['defeat'] = self.parse_int(defeat.strip())
                        item['player_id'] = player_id
                        item['type'] = 1
                        yield item
            else:
                print('%s is none' % response.url)
        except Exception as e:
            logging.exception(e)
            msg = traceback.format_exc()
            with open('error.log', 'a+') as f:
                f.write('url:' + response.url)
                f.write('\n')
                f.write('three_percentage>' + three_percentage + '<')
                f.write('\n')
                f.write(msg)
        pass

    def parse_allstar(self, response):
        try:
            if response is not None:
                selector = etree.HTML(response.text)
                trs = selector.xpath('//*[@id="stat_box_avg"]/tbody/tr[@class="sort"]')
                player_id = response.meta['player_id']
                if self.not_empty(trs):
                    for tr in trs:
                        season = tr.findtext('td[2]/a')
                        team = tr.findtext('td[3]/a')
                        # attend = tr.findtext('td[4]')
                        first_lineup = tr.findtext('td[4]')
                        play_time = tr.findtext('td[5]')
                        percentage = tr.findtext('td[6]')
                        field_goal = tr.findtext('td[7]')
                        shoot = tr.findtext('td[8]')
                        three_percentage = tr.findtext('td[9]')
                        three_field_goal = tr.findtext('td[10]')
                        three_shoot = tr.findtext('td[11]')
                        free_throw_percentage = tr.findtext('td[12]')
                        free_throw_field_goal = tr.findtext('td[13]')
                        free_throw_shoot = tr.findtext('td[14]')
                        rebound = tr.findtext('td[15]')
                        offensive_rebound = tr.findtext('td[16]')
                        defensive_rebound = tr.findtext('td[17]')
                        assist = tr.findtext('td[18]')
                        steal = tr.findtext('td[19]')
                        block = tr.findtext('td[20]')
                        turnover = tr.findtext('td[21]')
                        fault = tr.findtext('td[22]')
                        scoring = tr.findtext('td[23]')
                        victory = tr.findtext('td[24]')
                        defeat = tr.findtext('td[25]')

                        item = SeasonDataItem()
                        if season is not None:
                            item['season'] = season.strip()
                        if team is not None:
                            item['team'] = season.strip()
                        # if attend is not None:
                        #     item['attend'] = self.parse_int(attend.strip())
                        if first_lineup is not None:
                            item['starting_linup'] = self.parse_int(first_lineup.strip())
                        if play_time is not None:
                            item['play_duration'] = self.parse_int(play_time.strip())
                        if percentage is not None:
                            item['percentage'] = self.parse_float(percentage.strip())
                        if field_goal is not None:
                            item['field_goal'] = self.parse_int(field_goal.strip())
                        if shoot is not None:
                            item['shoot'] = self.parse_int(shoot.strip())
                        if three_percentage is not None:
                            item['three_percentage'] = self.parse_float(three_percentage.strip())
                        if three_field_goal is not None:
                            item['three_field_goal'] = self.parse_int(three_field_goal)
                        if three_shoot is not None:
                            item['three_shoot'] = self.parse_int(three_shoot)
                        if free_throw_percentage is not None:
                            item['free_throw_percentage'] = self.parse_float(free_throw_percentage.strip())
                        if free_throw_field_goal is not None:
                            item['free_throw_field_goal'] = self.parse_int(free_throw_field_goal.strip())
                        if free_throw_shoot is not None:
                            item['free_throw_shoot'] = self.parse_int(free_throw_shoot.strip())
                        if rebound is not None:
                            item['rebound'] = self.parse_int(rebound.strip())
                        if offensive_rebound is not None:
                            item['offensive_rebound'] = self.parse_int(offensive_rebound.strip())
                        if defensive_rebound is not None:
                            item['defensive_rebound'] = self.parse_int(defensive_rebound.strip())
                        if assist is not None:
                            item['assist'] = self.parse_int(assist.strip())
                        if steal is not None:
                            item['steal'] = self.parse_int(steal.strip())
                        if block is not None:
                            item['block'] = self.parse_int(block.strip())
                        if turnover is not None:
                            item['turnover'] = self.parse_int(turnover.strip())
                        if fault is not None:
                            item['scoring'] = self.parse_int(scoring.strip())
                        if victory is not None:
                            item['victory'] = self.parse_int(victory.strip())
                        if defeat is not None:
                            item['defeat'] = self.parse_int(defeat.strip())
                        item['player_id'] = player_id
                        item['type'] = 2
                        yield item
            else:
                print('%s is none' % response.url)
        except Exception as e:
            logging.exception(e)
            msg = traceback.format_exc()
            with open('error.log', 'a+') as f:
                f.write('url:' + response.url)
                f.write('\n')
                f.write('three_percentage>' + three_percentage + '<')
                f.write('\n')
                f.write(msg)
        pass

    def not_empty(self, list_obj):
        return list_obj is not None and len(list_obj) > 0

    def trim(self, string):
        if string is not None:
            return string.replace('\n', '').replace('\r', '').strip()

    def get_id_from_mongo(self):
        client = MongoClient('127.0.0.1', 27017)
        db = client['selfplay']
        table = db['player_info']
        result = table.find({})
        return result
