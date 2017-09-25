# -*- coding: utf-8 -*-
import scrapy


class UdacitySpider(scrapy.Spider):
    name = 'udacity'
    start_urls = ['https://br.udacity.com/courses/all/']

    def parse(self, response):
        courses = response.xpath(
            '//div[contains(@class, "course-summary-card")]')
        for course in courses:
            link = course.xpath('.//h3//a')
            href = link.xpath('./@href').extract_first()
            img = course.xpath(
                './/img[contains(@class, "img-responsive")]/@src'
            ).extract_first()
            # import ipdb; ipdb.set_trace()
            yield scrapy.Request(
                url='https://br.udacity.com{}'.format(href),
                callback=self.parse_detail,
                meta={'img': img}
            )

    def parse_detail(self, response):
        title = response.xpath('//title/text()').extract_first()
        # headline = response.xpath(
        #     '//h6[contains(@class, "big")]//text()'
        # ).extract_first()
        img = response.meta['img']
        instructors = response.xpath(
            '//div[@class="scroller"]//div[@class="card"]')

        list_instructors = []
        for instructor in instructors:
            name = instructor.xpath(
                './/*[@class="name"]//text()').extract_first()
            bio = instructor.xpath(
                './/*[contains(@class, "bio")]//text()').extract_first()
            img = instructor.xpath('.//*[@class="image"]/@src').extract_first()
            position = instructor.xpath(
                '//*[@class="title h6"]//text()').extract_first()
            list_instructors.append(
                {
                    'name': name,
                    'bio': bio,
                    'img': img,
                    'position': position
                }
            )
        yield {
            'title': title,
            'headline': headline,
            'img': img,
            'instructors': list_instructors
        }
