import scrapy
from ..items import ChinapropertyItem
from datetime import datetime
import sqlite3
from bs4 import BeautifulSoup
from lxml import etree
import json


class WuHuan(scrapy.Spider):

    name = 'wuhuan'
    page_number = 1
    start_urls = [
        'http://fgj.wuhan.gov.cn/xxgk/xxgkml/sjfb/mrxjspfcjtjqk/index.shtml'
    ]
    # start_urls += [f'http://fgj.wuhan.gov.cn/xxgk/xxgkml/sjfb/mrxjspfcjtjqk/index_{i}.shtml' for i in range(1, 91)]

    def parse(self, response):

        items = ChinapropertyItem()

        main = response.css('.article-box')
        lis = main.css('li')
        for li in lis:
            date = li.css('span ::text').extract()[0]
            link = li.css('a::attr(href)').extract()[0]
            title = li.css('a::text').extract()[0]

            # items['title'] = title
            # items['link'] = link
            # items['date'] = date
            yield scrapy.Request(link, callback=self.parse_details)

        next_page = f'http://fgj.wuhan.gov.cn/xxgk/xxgkml/sjfb/mrxjspfcjtjqk/index_{str(self.page_number)}.shtml'
        if self.page_number <= 91:
            self.page_number += 1
            print(next_page)
            yield response.follow(next_page, callback=self.parse)

    def parse_details(self, response):

        items = ChinapropertyItem()

        raw_data = response.body
        date = response.xpath('//span[i[@class="icon-clock"]]/text()').extract()[0]
        date = datetime.strptime(date, "%Y-%m-%d %H:%M").date()
        area = response.xpath('//tr[td[text()="合计"]]')[1].xpath('td[3]/text()').extract()[0]
        volume = response.xpath('//tr[td[text()="合计"]]')[1].xpath('td[2]/text()').extract()[0]

        items['date'] = date
        items['area'] = area
        items['volume'] = volume

        yield items

