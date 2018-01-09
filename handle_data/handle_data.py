# ! /usr/bin/python3
# -*- encoding:utf-8 -*-

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['selfplay']
table_info = db['player_info']
result = table_info.find({})
for res in result:
    r = dict(res)

    if 'shirt_number' in r.keys():
        shirt_number = r['shirt_number']
        if shirt_number is not None:
            numbers = shirt_number.split(',')
            # todo 分割的numbers中有字符串的形式
            numbers_int = [int(x) for x in numbers]
            r['shirt_numbers'] = numbers_int
    if 'user_name' in r.keys():
        user_name = r['user_name']
        if user_name is not None:
            names = user_name.split('/')
            r['chinese_name'] = names[0].strip()
    if 'play_position' in r.keys():
        play_position = r['play_position']
        if play_position is not None:
            position = play_position.split('-')
            r['position'] = position
    if 'height' in r.keys():
        height = r['height']
        if height is not None:
            end = height.find('米')
            r['height_number'] = float(height[0:end])
    if 'weight' in r.keys():
        weight = r['weight']
        if weight is not None:
            end = weight.find('公斤')
            r['weight_number'] = float(weight[0:end])
    print(r)
    table_info.update_one({'_id': r['_id']}, {'$set': dict(r)}, True, False)


    # 科比
