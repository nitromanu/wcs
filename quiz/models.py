from django.db import models

# Create your models here.

class Questions(models.Model):
    questionSetID = models.CharField(max_length=255)
    totalQuestions = models.IntegerField()
    questionSections = models.TextField()
    questionsJson = models.TextField()
    totalTime = models.IntegerField(default=60)
    categoryCode = models.CharField(max_length=255,default=None)
    startDate = models.DateField(default=None)
    endDate = models.DateField(default=None)
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.questionSetID


class Feedback(models.Model):
    username = models.CharField(max_length=255)
    questionSetID = models.CharField(max_length=255)
    feedback = models.TextField(default=None)

