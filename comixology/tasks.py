import json
from datetime import datetime

import scrapy
from scrapy.crawler import CrawlerProcess

from comixology.models import Sale


def parse_sales():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(SalesSpider)
    process.start()


class SalesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://m.comixology.co.uk/comics-sale',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        sales_text = response.css('#server-vars::text').extract_first()
        sales_json = json.loads(sales_text)
        sliders = sales_json.get('pageSliders')
        sale_ids = [s.get('id') for s in sliders]

        for id in sale_ids:
            yield response.follow(
                f'https://m.comixology.co.uk/browse/ajaxSlider?id={id}',
                self.parse_sale)

    def parse_sale(self, response):
        sale_json = json.loads(response.body_as_unicode())

        platform_id = sale_json.get('id')

        try:
            sale = Sale.objects.get(platform_id=platform_id)
        except Sale.DoesNotExist:
            sale = Sale(platform_id=platform_id)
        sale.title = sale_json.get('title')
        sale.url = sale_json.get('listUrl')
        sale.num_items = int(sale_json.get('count'))
        date_end_str = sale_json.get('subtitle').split(',')[-1].strip()
        sale.date_end = datetime.strptime(date_end_str, '%d/%m/%Y').date()
        sale.save()
