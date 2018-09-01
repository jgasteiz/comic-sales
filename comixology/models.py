import logging
from urllib import parse

from django.db import models


class Sale(models.Model):
    platform_id = models.IntegerField()
    title = models.CharField(max_length=256)
    date_end = models.DateField()
    url = models.URLField()
    num_items = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    cover_url = models.URLField(blank=True)

    class Meta:
        ordering = ['-created_at', 'title']

    def __str__(self):
        return f'{self.title} - {self.num_items} items - ends on {self.date_end}'


class WishListComic(models.Model):
    platform_id = models.IntegerField(blank=True)
    url = models.URLField()
    title = models.CharField(max_length=256, blank=True)
    notified = models.BooleanField(default=False)

    def __str__(self):
        return self.title or self.url

    def save(self, **kwargs):
        try:
            url = parse.urlparse(self.url)
            # The url.path will look like this: /<comic-name>/digital-comic/<comic-id>/
            path_components = list(filter(None, url.path.split('/')))
            self.title = path_components[0].replace('-', ' ')
            self.platform_id = int(path_components[-1])
        except Exception:
            logging.error("It wasn't possible extracting the platform id from the comic URL.")
        super().save(**kwargs)
