import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.conf import settings


class MySpider(scrapy.Spider):
    name = 'urlsd'
    start_urls = [url, ]
    custom_settings = {
        'DEPTH_LIMIT': self.depth
    }
    # def __init__(self, request, *args, **kwargs):
    #    super(MySpider, self).__init__(*args, **kwargs)
    #    print(request)
    # settings.overrides['DEPTH_LIMIT'] = request.meta['depth']
    # self.dom = request.meta["download_slot"]

    # allowed_domains = [request.url]
    # start_urls = [
    #    URL
    # ]

    def parse(self, response):

        le = LinkExtractor()
        for link in le.extract_links(response):
            self.data_list.append({"link": link.url})
