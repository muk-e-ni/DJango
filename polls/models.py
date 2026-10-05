from django.db import models


class Question(models.Model):
    q_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published") #human readable name for the field

    def __str__(self):
        return self.q_text

class Choice(models.Model):
    q = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice