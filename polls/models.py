from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin

class Question(models.Model):

    q_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published") #human readable name for the field

    def __str__(self):
        return self.q_text

    @admin.display(
            boolean = True,
            ordering = "pub_date",
            description = "Published Recently?",

    )
    def was_published_recently(self):
        now = timezone.now()
        return  now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    q = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice

