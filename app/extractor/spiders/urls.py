import scrapy
from scrapy.linkextractors import LinkExtractor


class UrlsSpider(scrapy.Spider):
    name = 'urlsd'

    def __init__(self, *args, **kwargs):
        super(UrlsSpider, self).__init__(*args, **kwargs)
        print(kwargs)
        print(kwargs.get('meta')['url'])
        print(kwargs.get('meta')['depth'])

        self.start_urls = [kwargs.get('meta')['url']]
        # custom_settings = {
        #    'DEPTH_LIMIT': kwargs.get('meta')['depth']
        # }

    def parse(self, response):
        le = LinkExtractor()
        for link in le.extract_links(response):
            self.data_list.append(link.url)
        print(self.data_list)
