from django.db import models

class Link(models.Model):
    url = models.URLField(unique=True, db_index=True, max_length=1024)
    created = models.DateTimeField(db_index=True, auto_now=True)
    lifetime = models.IntegerField()
