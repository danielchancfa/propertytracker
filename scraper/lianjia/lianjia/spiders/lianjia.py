import scrapy
import re
from ..items import LianjiaItem
from datetime import datetime
import sqlite3
from bs4 import BeautifulSoup
from lxml import etree
import json
from collections import defaultdict


class lianjia(scrapy.Spider):

    name = 'lianjia'
    page_number = 1
    start_urls = [
        'https://sz.lianjia.com/ershoufang/', #ShenZhen
        # 'https://wh.lianjia.com/ershoufang/' #WuHan
    ]
    headers = {
        "Accept": "application / json, text / javascript, * / *; q = 0.01",
        "Accept - Encoding": "gzip, deflate, br",
        "Accept - Language": "zh - TW, zh; q = 0.9, en - US; q = 0.8, en; q = 0.7",
        "User - Agent": "Mozilla / 5.0(Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 110.0.0.0 Safari / 537.36"
    }

    def parse(self, response):

        items = LianjiaItem()

        ul = response.xpath('//ul[@class="sellListContent"]')[0]
        divs = ul.xpath('//div[@class="info clear"]')
        unit_dic = defaultdict(lambda: 1)
        unit_dic['万'] = 10000
        date = datetime.today().date()
        for div in divs:
            title = div.xpath('div[@class="title"]/a/text()').get()
            link = div.xpath('div[@class="title"]/a/@href').get()
            region, house = div.xpath('div[@class="flood"]/div/a/text()').getall()
            price = div.xpath('div[@class="priceInfo"]//span/text()').get()
            price_unt = div.xpath('div[@class="priceInfo"]//span/text()').get()
            if price:
                price = float(price) * unit_dic[price_unt]
            size = div.xpath('div[@class="address"]/div/text()').get().split('| ')[1].strip()
            if size:
                size = float(re.findall(r'[\d\.\d]+', size)[0])
            housecode = div.xpath('div[@class="title"]/a/@data-housecode').get()

            items['title'] = title
            items['link'] = link
            items['region'] = region
            items['house'] = house
            items['price'] = price
            items['size'] = size
            items['housecode'] = housecode
            items['date'] = date

            yield items

        next_page = f'https://sz.lianjia.com/ershoufang/pg{str(self.page_number)}/' #ShenZhen
        # next_page = f'https://wh.lianjia.com/ershoufang/pg{str(self.page_number)}/' #WuHan
        if self.page_number <= 99:
            self.page_number += 1

            yield response.follow(next_page, callback=self.parse)




