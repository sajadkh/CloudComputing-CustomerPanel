from django.db import models


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(blank=True)
    total_price = models.FloatField(default=0.0, blank=True)
    status = models.BooleanField(default=False)
    restaurant = models.CharField(max_length=255, blank=False)
    customer = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.order_id