# !/usr/bin/python3
# -*-encoding:utf-8 -*-
import requests
from pymongo import MongoClient
import random

def test():
    url = 'http://www.gushiwen.org/'
    data = get_proxy()
    proxy = ''
    if data['type'].lower() == 'http':
        proxy = 'http://' + data['ip'] + ':' + data['port']
    elif data['type'].lower() == 'https':
        proxy = 'https://' + data['ip'] + ':' + data['port']
    else:
        proxy = 'http://' + data['ip'] + ':' + data['port']
    print(proxy)
    proxies = {
        proxy
    }
    response = requests.get(url,proxies = proxies)
    # response = requests.get(url)
    if response is not None:
        print(response.text)

def get_proxy():
    client = MongoClient('localhost',27017)
    db = client['selfplay']
    table = db['ip_proxy']
    random_number = int(random.random()*500)
    print('random number:' + str(random_number))
    cursor = table.find({}).skip(random_number).limit(1)
    data = {}
    for c in cursor:
        data = c
    return data

if __name__ == '__main__':
    # for c in get_proxy():
    #     print(c)
    test()