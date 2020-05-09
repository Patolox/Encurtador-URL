from hashlib import md5

from django.db import models


class URL(models.Model):
    full_url = models.URLField(unique=True)
    url_hash = models.URLField(unique=True)
    clicks = models.IntegerField(default=0)

    def clicked(self):
        self.clicks += 1
        self.save()

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)