from django.db import models

from apps.orders.models import Order


class LeasingAgreement(models.Model):
    leasing_num = models.CharField(max_length=20)
    leasing_date = models.DateField()
    contract_price = models.BigIntegerField()  # цена договора
    number_of_techs = models.IntegerField()  # количество техники
    lessor_sign = models.CharField(max_length=12, null=True)  # арендодатель подпись
    lessee_sign = models.CharField(max_length=12, null=True)  # арендатор подпись
    guarantor_sign = models.CharField(max_length=12, null=True)  # поручитель подпись

    order_model = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'LeasingAgreement'
