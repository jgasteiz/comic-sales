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
    url = models.URLField()
    title = models.CharField(max_length=256, blank=True)
    cover_url = models.URLField(blank=True)

    def __str__(self):
        return self.title
