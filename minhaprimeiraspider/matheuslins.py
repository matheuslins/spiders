import scrapy


class MatheusLinsSpider(scrapy.Spider):
    name = 'matheuslins'
    start_urls = ['http://www.matheuslins.com']

    def parse(self, response):
        self.log(response.body)
