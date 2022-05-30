from django.db import models

from apps.acts.models import Act
from apps.technics.models import Technique


class PaymentGraph(models.Model):
    act = models.ForeignKey(Act, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'PaymentGraph'


class PaymentTable(models.Model):
    residual_amount = models.FloatField()
    date = models.DateField()
    days_count = models.IntegerField()
    quarterly_lease_term_part_of_value = models.FloatField()
    quarterly_percent_lease_term_payment = models.FloatField()
    quarterly_lease_term_payment = models.FloatField()
    is_paid = models.BooleanField()
    payment_graph = models.ForeignKey(PaymentGraph, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'PaymentTable'
