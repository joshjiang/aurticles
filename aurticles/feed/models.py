import datetime

from django.utils import timezone
from django.db import models
from django.forms import ModelForm
from bs4 import BeautifulSoup


class User(models.Model):
    time_published = models.DateTimeField('date published')
    name = models.CharField(max_length = 200, blank = True)

    def was_recently_published(self):
        return self.time_published  >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return str(self.id)

class Article(models.Model):
    title = models.CharField(max_length = 500)
    publisher = models.CharField(max_length = 500)
    body = models.TextField()
    time_published = models.DateTimeField('date published')
    time_added = models.DateTimeField('date added')
    hyperlink = models.URLField()
    # TODO: audio, categories
    # audio = models.FileField(upload_to=None, max_length=100)
    # categories = foreignkey models.Categories 
    # user = models.ForeignKey(User, on_delete=models.CASCADE)    
    def __str__(self):
        return self.title