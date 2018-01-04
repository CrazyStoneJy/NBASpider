# !/usr/bin/python3
# -*- encoding: utf-8 -*-
import requests
from lxml import etree
from fake_useragent import UserAgent
import logging
import random, time
from pymongo import MongoClient


class CrawlIp():
    base_url = 'http://www.xicidaili.com/{type}/{page}'
    PAGE_LIMIT = 10
    CONNECTION_TIME_LIMIT = 1
    SPEED_TIME = 1

    def __init__(self):
        self.ua = UserAgent()
        self.cleint = MongoClient('127.0.0.1', 27017)
        self.db = self.cleint['selfplay']

    def crawl(self):
        for k, v in self.proxy_type().items():
            # print(k,v)
            url = self.base_url.format(type=v, page=1)
            self.loop(url, v, 1)

    def loop(self, url, proxy_type, page):
        headers = {
            'User-Agent': self.ua.random
        }
        response = requests.get(url, headers=headers)
        print(url)
        try:
            if page <= self.PAGE_LIMIT:
                if response is not None:
                    selector = etree.HTML(response.text)
                    lis = selector.xpath('//table[@id="ip_list"]/tr')
                    # print(lis)
                    self.print_element(lis[0])
                    if lis is not None and len(lis) > 0:
                        for i, li in enumerate(lis):
                            if i > 0:
                                image = li.find('td[1]/img')
                                ip = li.findtext('td[2]')
                                port = li.findtext('td[3]')
                                server_address = li.findtext('td[4]/a')
                                anynomous = li.findtext('td[5]')
                                type = li.findtext('td[6]')
                                speed = li.find('td[7]/div')
                                connection_time = li.find('td[8]/div')
                                alive_time = li.findtext('td[9]')
                                validate_time = li.findtext('td[10]')

                                crawlDict = dict()
                                if image is not None:
                                    crawlDict['country'] = image.get('alt')
                                if ip is not None:
                                    crawlDict['ip'] = ip
                                if port is not None:
                                    crawlDict['port'] = port
                                if server_address is not None:
                                    crawlDict['server_address'] = server_address
                                if anynomous is not None:
                                    crawlDict['anynomous'] = anynomous
                                if type is not None:
                                    crawlDict['type'] = type
                                if speed is not None:
                                    speed_number = speed.get('title')[:-1]
                                    crawlDict['speed'] = float(speed_number)
                                if connection_time is not None:
                                    connection_number = connection_time.get('title')[:-1]
                                    crawlDict['connection_time'] = float(connection_number)
                                if alive_time is not None:
                                    crawlDict['alive_time'] = alive_time
                                if validate_time is not None:
                                    crawlDict['validate_tmie'] = validate_time
                                print(crawlDict)
                                self.save2mongo(crawlDict)

                        time.sleep(random.random() * 5)
                        page = page + 1
                        next_url = self.base_url.format(type=proxy_type, page=page)
                        print(next_url)
                        self.loop(next_url, proxy_type, page)
                    pass
                else:
                    print('response is none')
            else:
                print('{}页以后不抓取了'.format(self.PAGE_LIMIT))
        except Exception as e:
            logging.exception(e)
            print('server exception')

    def save2mongo(self, data):
        table = self.db['ip_proxy']
        if data['connection_time'] <= self.CONNECTION_TIME_LIMIT and data['speed'] <= self.SPEED_TIME:
            table.update_one({'ip': data['ip'], 'port': data['port']}, {'$set': data}, True, False)

    def not_empty(self, li):
        return li is not None and len(li) > 0

    def print_element(self, element):
        string = etree.tostring(element, pretty_print=True).decode('utf-8')
        print(string)

    def proxy_type(self):
        proxy_dict = dict()
        proxy_dict[0] = 'nn'
        proxy_dict[1] = 'nt'
        proxy_dict[2] = 'wn'
        proxy_dict[3] = 'wt'
        # print(proxy_dict)
        return proxy_dict

    def test(self):
        string = 'abcde'
        print(string[:-1])


if __name__ == '__main__':
    crawl = CrawlIp()
    crawl.crawl()
    # crawl.test()
