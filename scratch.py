# encoding: utf-8

import json
import requests
from lxml import html
from utils import log


__author__ = 'hua'


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


def house_from_div(div):
    rel_href = div.xpath('.//a[@class="list-info-title js-title"]/@href')[0]
    # 应对复杂链接
    if 'http' not in rel_href:
        abs_href = 'http://bj.ganji.com' + rel_href
    else:
        abs_href = rel_href
    log(abs_href)
    item_page = requests.get(abs_href)
    item_div = html.fromstring(item_page.content)
    house = House()
    title = item_div.xpath('.//div[@class="col-cont title-box"]/h1')[0].text
    if title is None:
        title = '无标题'
    house.title = title
    house.rent = item_div.xpath('.//b[@class="basic-info-price fl"]')[0].text
    house.situation = item_div.xpath('.//ul[@class="basic-info-ul"]/li/text()')[4]
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
    houses = [house_from_div(div) for div in house_divs]
    try:
        next_page_url = root.xpath('//ul[@class="pageLink clearfix"]//a[@class="next"]/@href')[0]
        abs_next_page_url = 'http://bj.ganji.com' + next_page_url
    except IndexError as e:
        abs_next_page_url = 'over'
    return houses, abs_next_page_url


def main():
    url = 'http://bj.ganji.com/fang1/b2000e5000/'
    all_houses = []
    while True:
        houses, abs_next_page_url = houses_from_url(url)
        all_houses += houses
        if abs_next_page_url == 'over':
            break
        url = abs_next_page_url
    log(all_houses[:20])

    # houses.sort(key=lambda m: m.rating)
    # for house in houses:
    #     log(house)


if __name__ == '__main__':
    main()
