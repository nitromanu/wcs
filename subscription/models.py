from django.db import models

# Create your models here.

class paymentVoucher(models.Model):
    category_code = models.CharField(max_length=255)
    voucher_number = models.CharField(max_length=255)
    voucher_price = models.IntegerField()
    created_date = models.DateField(default=None)
    expiry_date = models.DateField(default=None)
    is_active = models.IntegerField(default=1)
    voucher_agent_code = models.CharField(max_length=255)
    used_by = models.CharField(max_length=255)
    number_of_days = models.IntegerField(default=30)
    total_attempts = models.IntegerField(default=4)

    def __unicode__(self):
        return self.voucher_number


class subscriptionDetails(models.Model):
    username = models.CharField(max_length=255)
    start_date = models.DateField(default=None)
    end_date = models.DateField(default=None)
    voucher_number = models.CharField(max_length=255)
    attempts_remaining = models.IntegerField(default=0)

    def __unicode__(self):
        return self.username