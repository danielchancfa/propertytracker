import scrapy
from ..items import FangItem
import datetime
from bs4 import BeautifulSoup
from lxml import etree
import json

class ZhenShenFang(scrapy.Spider):
    name = 'zhenshenFang'
    page_number = 1
    start_urls = [
        'https://sz.esf.fang.com/'
    ]
    headers = {
        "content - encoding": "gzip, deflate, br",
        "accept": "text / html, application / xhtml + xml, application / xml; q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange; v = b3; q = 0.7",
        "accept - language": "zh - TW, zh; q = 0.9, en - US; q = 0.8, en; q = 0.7",
        "content - type": "text / html; charset = utf - 8",
        "user-agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    # custom_settings = {
    #     'LOG_LEVEL':'ERROR'
    # }


    def parse(self, response):
        table = response.xpath('//div[@class="shop_list shop_list_4"]/dl')
        unit_dict = {'万': 10000, '千': 1000}
        items = FangItem()

        for div in table:

            title = div.xpath('dd/h4/a/@title').get()

            size = div.xpath('dd/p[@class="tel_shop"]/text()[2]').get()
            price = div.xpath('dd[@class="price_right"]/span[@class="red"]/b/text()').get()
            if title:
                date = datetime.datetime.today().date()
                size = size.replace("\n", "").replace("\t", "")
                price = float(price)
                price_unit = div.xpath('dd[@class="price_right"]/span[@class="red"][1]/text()[2]').get()
                price = float(price) * unit_dict[price_unit]
                address = div.xpath('dd/p[@class="add_shop"]/span/text()').get()
                community = div.xpath('dd/p[@class="add_shop"]/a/text()').get().replace("\n", "").replace("\t", "")
                extend_link = div.xpath('dd/h4/a/@href').get()
                link = response.urljoin(extend_link)

                items['date'] = date
                items['title'] = title
                items['size'] = size
                items['price'] = price
                items['address'] = address
                items['community'] = community
                items['link'] = link

                yield items
        next_page = f'https://sz.esf.fang.com/house/i3{str(self.page_number)}/'
        if self.page_number <= 5:
            self.page_number += 1

            yield response.follow(next_page, callback=self.parse, encoding="utf-8")




    # def parse_details(self, response):
    #
    #     items = ChinapropertyItem()
    #
    #     raw_data = response.body
    #     date = response.xpath('//span[i[@class="icon-clock"]]/text()').extract()[0]
    #     date = datetime.strptime(date, "%Y-%m-%d %H:%M").date()
    #     area = response.xpath('//tr[td[text()="合计"]]')[1].xpath('td[3]/text()').extract()[0]
    #     volume = response.xpath('//tr[td[text()="合计"]]')[1].xpath('td[2]/text()').extract()[0]
    #
    #     items['date'] = date
    #     items['area'] = area
    #     items['volume'] = volume
    #
    #     yield items
