# -*- coding: utf-8 -*-
import scrapy
import logging


class HeadersSpider(scrapy.Spider):
    name = 'headers'

    def __init__(self, *args, **kwargs):
        super(HeadersSpider, self).__init__(*args, **kwargs)
        start_urls = [kwargs.get('meta')['url']]
        print("start urls below")
        print(start_urls)
      # self.link = [kwargs.get('meta')['url']]
        custom_settings = {
            'DEPTH_LIMIT': kwargs.get('meta')['depth']
        }
        print("inside spider init")

    def parse(self, response):
        print("Inside parse")
        f2 = file("xyz.txt","w")
        f2.write("inside parse")
        f2.close()
        h1 = response.xpath('//h1/text()').extract()
        h2 = response.xpath('//h2/text()').extract()
        h3 = response.xpath('//h3/text()').extract()
        h4 = response.xpath('//h4/text()').extract()
        h5 = response.xpath('//h5/text()').extract()
               
        data = {"url": response.url, "h1": h1,
                "h2": h2, "h3": h3, "h4": h4, "h5": h5}
        for x in data.values():
            if type(x) is not str:
                for i in range(0, len(x)):
                    x[i] = x[i].strip()
        print(data)
        self.data_list.append(data)
       # print(data_list)
        f3 = file("results.txt","w")
        f3.write(data_list)
        f3.close()
