from django.db import models

# Create your models here.

class studentResponse(models.Model):
    username = models.CharField(max_length=255)
    categoryCode = models.CharField(max_length=255)
    questionSetID = models.CharField(max_length=255)
    response = models.TextField(default=None)
    sectionResults = models.TextField(default=None)
    marksObtained = models.DecimalField(default=None,max_digits=5,decimal_places=2)
    totalCorrectAnswer = models.IntegerField(default=None)
    totalWrongAnswer = models.IntegerField(default=None)
    totalTimeTaken = models.IntegerField(default=None)
    totalUnAttempted = models.IntegerField(default=None)
    totalAttempted = models.IntegerField(default=None)

    def __unicode__(self):
        return self.questionSetID

class averageResult(models.Model):
    categoryCode = models.CharField(max_length=255)
    questionSetID = models.CharField(max_length=255)
    attendedAvg = models.IntegerField(default=0)
    correctAvg = models.IntegerField(default=0)
    wrongAvg = models.IntegerField(default=0)
    timeAvg = models.IntegerField(default=0)
    marksAvg = models.IntegerField(default=0)
    lastSynced = models.DateField(default=None)


    def __unicode__(self):
        return self.questionSetID

class feedback(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    question_set = models.CharField(max_length=255)
    feedback = models.TextField(default=None)


    def __unicode__(self):
        return self.question_set


class monthlyReport(models.Model):
    report_id = models.CharField(max_length=255)
    qsets_include = models.TextField(default=None)


    def __unicode__(self):
        return self.report_id

