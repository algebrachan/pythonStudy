from django.db import models

# Create your models here.
class activity(models.Model):
    """docstring"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    cost = models.CharField(max_length=20)
    deposit = models.CharField(max_length=20)
    activity_price_deposit = models.CharField(max_length=20)
    toplimit = models.CharField(max_length=20)
    Statement = models.CharField(max_length=20)
    