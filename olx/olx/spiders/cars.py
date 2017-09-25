# -*- coding: utf-8 -*-
import scrapy


class CarsSpider(scrapy.Spider):
    name = 'cars'
    allowed_domains = ['pe.olx.com.br']
    start_urls = [
        'http://pe.olx.com.br/veiculos-e-acessorios/carros/ford',
        'http://pe.olx.com.br/veiculos-e-acessorios/carros/nissan',
        'http://pe.olx.com.br/veiculos-e-acessorios/carros/vw-volkswagen'
    ]

    def parse(self, response):
        items = response.xpath('//ul[@id="main-ad-list"]//li[not(contains'
                               '(@class, "list_native"))]')
        for item in items:
            url = item.xpath('./a/@href').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_detail)

        pagination = response.xpath('//a[@rel="next"]/@href').extract_first()
        if pagination:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                dont_filter=True
            )

    def parse_detail(self, response):
        _base_xpath = ('//p[@class="text"]//span[@class="term" '
                       'and contains(text(), "{}")]/following-s'
                       'ibling::strong[@class="description"]//text()').format

        title = response.xpath('//h1[@id="ad_title"]/text()').extract_first()
        category = response.xpath(_base_xpath('Categoria')).extract()[1]
        model = response.xpath(_base_xpath('Modelo')).extract_first()[1]
        year = response.xpath(_base_xpath('Ano')).extract()[1]
        km = response.xpath(_base_xpath('Quilometragem')).extract_first()
        fuel = response.xpath(_base_xpath('Combus')).extract()[1]
        gearbox = response.xpath(_base_xpath('mbio:')).extract_first()
        dors = response.xpath(_base_xpath('Portas')).extract_first()
        city = response.xpath(_base_xpath('Muni')).extract()[1]
        postal_code = response.xpath(_base_xpath('CEP')).extract_first()
        neighborhood = response.xpath(_base_xpath('Bairro')).extract_first()

        yield {
            'title': title,
            'category': category,
            'model': model,
            'year': year,
            'km': km,
            'fuel': fuel,
            'gearbox': gearbox,
            'dors': dors,
            'city': city,
            'postal_code': postal_code,
            'neighborhood': neighborhood
        }
