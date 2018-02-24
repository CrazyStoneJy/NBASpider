# !/usr/bin/python3
# -*- encoding:utf-8 -*-

from pymongo import MongoClient
from pyecharts import Radar


class NBA(object):
    def __init__(self):
        self.client = MongoClient('127.0.0.1', 27017)
        self.db = self.client['selfplay']

    def search_player(self, player_name):
        table_player = self.db['player_info']
        result = table_player.find({'user_name': {'$regex': player_name}}).limit(1)
        for r in result:
            # print(r)
            return r['player_id']

    def search_season_data(self, player_id):
        table_season_data = self.db['player_data']
        result = table_season_data.find({'player_id': player_id, 'type': 0}).limit(1)
        return result

    def get_player_data(self, player_name):
        player_id = self.search_player(player_name)
        print('player_id:' + str(player_id))
        result = self.search_season_data(player_id)
        for r in result:
            steal = r['steal']
            rebound = r['rebound']
            assist = r['assist']
            scoring = r['scoring']
            attend = r['attend']
            block = r['block']
            array = []
            average_steal = self.average_steal(steal, attend)
            average_scoring = self.average_scoring(scoring, attend)
            average_block = self.average_block(block, attend)
            average_assist = self.average_assist(assist, attend)
            average_rebound = self.average_rebound(rebound, attend)
            array.append(average_scoring)
            array.append(average_rebound)
            array.append(average_assist)
            array.append(average_steal)
            array.append(average_block)
            print('场均得分', '场均篮板', '场均助攻', '场均抢断', '场均盖帽')
            print('%.1f %.1f %.1f %.1f %.1f' % (
                average_scoring, average_rebound, average_assist, average_steal, average_block))
            return array
        pass

    def average_steal(self, steal, attend):
        return self.divide(steal, attend)

    def average_scoring(self, scoring, attend):
        return self.divide(scoring, attend)

    def average_block(self, block, attend):
        return self.divide(block, attend)

    def average_assist(self, assist, attend):
        return self.divide(assist, attend)

    def average_rebound(self, rebound, attend):
        return self.divide(rebound, attend)

    def divide(self, dividend, divisor):
        return round(dividend / divisor, 2)

    def visual(self, array):
        schema = [('得分', 35), ('篮板', 20), ('助攻', 15), ('抢断', 5), ('盖帽', 5)]
        radar = Radar()
        radar.config(schema)
        for player, data in array.items():
            radar.add(player, data, is_splitline=True, is_axisline_show=True)
        radar.render('player.html')

    def test(self,players_name):
        players = dict()
        for player_name in players_name:
            player = self.get_player_data(player_name)
            players[player_name] = [player]
        print(players)
        self.visual(players)

    def main(self):
        array = []
        array.append('斯蒂芬-库里')
        array.append('勒布朗-詹姆斯')
        array.append('德怀特-霍华德')
        array.append('丹尼-格林')
        self.test(array)

if __name__ == '__main__':
    nba = NBA()
    nba.search_player('斯蒂芬-库里')
    # 霍华德　丹尼-格林
    nba.main()
