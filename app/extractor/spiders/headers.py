# -*- coding: utf-8 -*-
import scrapy
import logging


class HeadersSpider(scrapy.Spider):
    name = 'headers'
    start_urls = [self.url, ]
    custom_settings = {
        'DEPTH_LIMIT': self.depth
    }

    def parse(self, response):
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

        self.data_list.append(data)
