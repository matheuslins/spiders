# -*- coding: utf-8 -*-
import scrapy


class CourseraSpider(scrapy.Spider):
    name = 'coursera'
    start_urls = ['https://www.coursera.org/browse?languages=pt']

    def parse(self, response):
        self.log(response.body)
