from django.db import models

# Create your models here.

class UserProfile(models.Model):
    email = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50, default=None)
    school_name = models.TextField(default=None)


    def __unicode__(self):
        return self.email
