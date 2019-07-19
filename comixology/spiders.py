import json
import logging
from datetime import datetime
from urllib import parse

import scrapy

from . import email_tasks, models


class SalesSpider(scrapy.Spider):
    name = "sales"

    def start_requests(self):
        urls = ["https://m.comixology.co.uk/comics-sale"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        sales_text = response.css("#server-vars::text").extract_first()
        sales_json = json.loads(sales_text)
        sliders = sales_json.get("pageSliders")
        sale_ids = [s.get("id") for s in sliders]

        for sale_id in sale_ids:
            yield response.follow(
                f"https://m.comixology.co.uk/comics-sale?list_id={sale_id}",
                self.parse_sale,
            )

    def parse_sale(self, response):
        """
        Parse the sale page and extract the sale information.
        """
        # Title
        sale_title = response.css(".list-title-header::text").extract_first()
        if not sale_title:
            sale_title = response.css(".list-title::text").extract_first()
        # Url
        sale_url = response.url
        # Cover url
        sale_cover_url = response.css(".content-img::attr(src)").extract_first()
        # End date of the sale
        date_end_str = response.css(".subtitle-text::text").extract_first()
        date_end_str = date_end_str.split(", ")[-1]
        sale_date_end = datetime.strptime(date_end_str, "%d/%m/%Y").date()
        # Num items on sale
        sale_num_items = response.css(".list-count::text").extract_first()
        if not sale_num_items:
            sale_num_items = 1
        else:
            # Get the number of items from the last part of a string like `1-29 of 300`
            sale_num_items = sale_num_items.split(" of ")[-1]
            # Replace commas in the number if it's over 1000. E.g. 1,300
            sale_num_items = sale_num_items.replace(",", "")
            # Make an integer from it.
            sale_num_items = int(sale_num_items)
        # Sale platform id
        try:
            url = parse.urlparse(sale_url)
            sale_platform_id = parse.parse_qs(url.query)["list_id"][0]
        except Exception:
            logging.error(
                "It wasn't possible extracting the platform id from the sale URL."
            )
            return

        # Retrieve an existing sale or create a new one
        try:
            sale = models.Sale.objects.get(platform_id=sale_platform_id)
            created = False
        except models.Sale.DoesNotExist:
            sale = models.Sale(platform_id=sale_platform_id)
            created = True

        # Populate its properties and save it.
        sale.title = sale_title
        sale.url = sale_url
        sale.num_items = sale_num_items
        sale.cover_url = sale_cover_url
        sale.date_end = sale_date_end
        sale.save()

        # If it's a new sale, send an email.
        if created:
            email_tasks.send_sale_email(sale)


class WishlistComicSpider(scrapy.Spider):
    name = "wishlist_comics"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wishlist_ids = models.WishListComic.objects.filter(
            notified=False
        ).values_list("platform_id", flat=True)

    def start_requests(self):
        urls = ["https://m.comixology.co.uk/comics-sale"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        sales_text = response.css("#server-vars::text").extract_first()
        sales_json = json.loads(sales_text)
        sliders = sales_json.get("pageSliders")
        sale_ids = [s.get("id") for s in sliders]

        for sale_id in sale_ids:
            yield response.follow(
                f"https://m.comixology.co.uk/comics-sale?list_id={sale_id}",
                self.parse_sale_wishlist,
            )

    def parse_sale_wishlist(self, response):
        """
        Look for comics in the wishlist_ids list.
        """
        for comic_id in self.wishlist_ids:
            comic_urls = response.css(
                ".comic-item .content-img-link::attr(href)"
            ).extract()
            matches = [url for url in comic_urls if url.endswith(str(comic_id))]
            if len(matches) > 0:
                wishlist_comic = models.WishListComic.objects.get(platform_id=comic_id)
                email_tasks.send_wishlist_item_email(wishlist_comic)
                wishlist_comic.notified = True
                wishlist_comic.save()

        # Go to the next page
        next_url = response.css(".pagination-page.next a::attr(href)").extract_first()
        if next_url and next_url != "#":
            yield response.follow(next_url, self.parse_sale_wishlist)
