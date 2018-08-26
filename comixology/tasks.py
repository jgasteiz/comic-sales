import json
import os
from datetime import datetime

import scrapy
import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail
from scrapy.crawler import CrawlerProcess

from comixology.models import Sale


def parse_sales():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(SalesSpider)
    process.start()


def send_sale_email(sale):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(os.environ.get('FROM_EMAIL'))
    to_email = Email(os.environ.get('TO_EMAIL'))
    subject = f"New comic sale - {sale.title}"
    content = Content("text/plain", sale.url)
    mail = Mail(from_email, subject, to_email, content)
    sg.client.mail.send.post(request_body=mail.get())


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

        for sale_id in sale_ids:
            yield response.follow(
                f'https://m.comixology.co.uk/browse/ajaxSlider?id={sale_id}',
                self.parse_sale)

    def parse_sale(self, response):
        sale_json = json.loads(response.body_as_unicode())

        platform_id = sale_json.get('id')

        try:
            sale = Sale.objects.get(platform_id=platform_id)
            created = False
        except Sale.DoesNotExist:
            sale = Sale(platform_id=platform_id)
            created = True
        sale.title = sale_json.get('title')
        sale.url = sale_json.get('listUrl')
        sale.num_items = int(sale_json.get('count'))
        date_end_str = sale_json.get('subtitle').split(',')[-1].strip()
        sale.date_end = datetime.strptime(date_end_str, '%d/%m/%Y').date()
        sale.save()

        # If it's a new sale, send an email
        if created:
            send_sale_email(sale)
