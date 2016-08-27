# encoding: utf-8

import json
import requests
import sqlite3
from lxml import html
from utils import log

__author__ = 'hua'

id_data = 1


class Model(object):
    def __str__(self):
        class_name = self.__class__.__name__
        properties = (u'{0} = ({1})'.format(k, v) for k, v in self.__dict__.items())
        r = u'\n<{0}:\n  {1}\n>'.format(class_name, u'\n  '.join(properties))
        return r


class House(Model):
    def __init__(self):
        self.title = ''
        self.rent = ''
        self.situation = ''
        self.size = ''
        self.position = ''
        self.href = ''


def sql_init():
    conn = sqlite3.connect('data.db')
    log('initiate sql-database successfully')
    conn.execute(
        '''CREATE TABLE houses
        (ID INTEGER PRIMARY KEY NOT NULL,
        TITLE TEXT NOT NULL,
        RENT TEXT NOT NULL,
        SITUATION TEXT NOT NULL,
        SIZE TEXT NOT NULL,
        POSITION TEXT NOT NULL,
        HREF TEXT NOT NULL
        )'''
    )
    log('table created')
    conn.close()


def test_sql():
    conn = sqlite3.connect('data.db')
    # test_data = [(1, 'nothing to show', '2000', '便利的环境', '80m2', '120,32'),]
    # conn.executemany('INSERT INTO houses VALUES (?,?,?,?,?,?)', test_data)
    # conn.execute(
    #     '''
    #     DELETE FROM houses WHERE ID=1
    #     '''
    # )
    conn.commit()
    conn.close()
    log('操作数据库成功')


def house_from_div(div):
    rel_href = div.xpath('.//a[@class="list-info-title js-title"]/@href')[0]
    # 应对复杂链接
    if 'http' not in rel_href:
        abs_href = 'http://bj.ganji.com' + rel_href
    else:
        abs_href = rel_href
    log(abs_href)
    house = House()
    item_page = requests.get(abs_href)
    if item_page.status_code == 200:
        item_div = html.fromstring(item_page.content)
        house.href = abs_href
        try:
            title = item_div.xpath('.//div[@class="col-cont title-box"]/h1')[0].text
            if title is None:
                title = '无标题'
        except IndexError as e:
            title = '无标题'
        house.title = title
        house.rent = item_div.xpath('.//b[@class="basic-info-price fl"]')[0].text
        house.situation = item_div.xpath('.//ul[@class="basic-info-ul"]/li/text()')[4].lstrip()
        house.size = item_div.xpath('.//ul[@class="basic-info-ul"]/li/text()')[3].lstrip()
        try:
            geography = item_div.xpath('//div[@id="map_load"]/@data-ref')[0]
            geography_dict = json.loads(geography)
            house.position = geography_dict.get('lnglat')
        except IndexError as e:
            house.position = 'negative'
    return house


def houses_from_url(url):
    page = requests.get(url)
    root = html.fromstring(page.content)
    house_divs = root.xpath('//li[@class="list-img clearfix"]')
    # log(house_divs)
    # houses = [house_from_div(div) for div in house_divs]
    for div in house_divs:
        s_h = house_from_div(div)
        if s_h.title == '':
            continue
        conn = sqlite3.connect('data.db')
        global id_data
        single_house_info = [(id_data, s_h.title, s_h.rent, s_h.situation,
                              s_h.size, s_h.position, s_h.href),]
        conn.executemany('INSERT INTO houses VALUES (?,?,?,?,?,?,?)', single_house_info)
        conn.commit()
        conn.close()
        log('成功插入{}条数据'.format(id_data))
        id_data += 1
    try:
        next_page_url = root.xpath('//ul[@class="pageLink clearfix"]//a[@class="next"]/@href')[0]
        abs_next_page_url = 'http://bj.ganji.com' + next_page_url
    except IndexError as e:
        abs_next_page_url = 'over'
    return abs_next_page_url


def main():
    url = 'http://bj.ganji.com/fang1/b3000e5000/'
    while True:
        abs_next_page_url = houses_from_url(url)
        if abs_next_page_url == 'over':
            break
        url = abs_next_page_url


if __name__ == '__main__':
    main()
    # sql_init()
    # test_sql()

# TODO list
# 写入数据库