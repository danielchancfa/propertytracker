import scrapy
from bs4 import BeautifulSoup
from lxml import etree
import json

class ZhenShen(scrapy.Spider):
    name = 'zhenshen'
    start_urls = [
        'http://zjj.sz.gov.cn/xxgk/ztzl/pubdata/'
    ]
    custom_settings = {
        'LOG_LEVEL':'ERROR'
    }

    headers = {
    "Accept": "application / json, text / plain, * / *",
    "Accept - Encoding": "gzip, deflate",
    "Accept - Language": "zh - TW, zh; q = 0.9, en - US; q = 0.8, en; q = 0.7",
    "Connection": "keep - alive",
    "Content - Length": "63",
    "Content - Type": "application / json; charset = UTF - 8",
    "Host": "zjj.sz.gov.cn:8004",
    "Origin": "http: // zjj.sz.gov.cn: 8004",
    "User - Agent": """Mozilla / 5.0(Macintosh;
    Intel
    Mac
    OS
    X
    10_15_7) AppleWebKit / 537.36(KHTML, like
    Gecko) Chrome / 110.0
    .0
    .0
    Safari / 537.36"""
    }

    def parse(self, response):
        link = 'http://zjj.sz.gov.cn:8004/api/marketInfoShow/getFjzsInfoData'
        yield scrapy.Request(link,
                                 callback=self.parse_api,
                                 headers=self.headers)

    def parse_api(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        for d in data:
            for date in d['date']:
                print(date)



