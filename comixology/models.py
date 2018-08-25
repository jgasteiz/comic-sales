from django.db import models


class Sale(models.Model):
    platform_id = models.IntegerField()
    title = models.CharField(max_length=256)
    date_end = models.DateField()
    url = models.URLField()
    num_items = models.IntegerField()

    class Meta:
        ordering = ['date_end']

    def __str__(self):
        return f'{self.title} - {self.num_items} items - ends on {self.date_end}'
