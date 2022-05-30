from django.db import models

from apps.regions.models import MFY
from apps.technics.models import Technique
from apps.tools.models import AgroLeasingBranch


class Order(models.Model):
    stir = models.BigIntegerField()
    fullname = models.CharField(max_length=150)
    activity_type = models.TextField()  # тип деятельности
    organizational_legal_form = models.TextField()  # организационно-правовая форма
    legal_address = models.TextField()  # юридический адрес
    postal_code = models.IntegerField()  # почтовый индекс
    home_address = models.CharField(max_length=200)  # адрес дома
    phone_num = models.CharField(max_length=20)
    mfo = models.TextField()
    account_num = models.IntegerField()  # номер счета
    bank_name = models.TextField()
    chief_name = models.TextField()  # имя начальника
    chief_phone_num = models.CharField(max_length=20)  # номер начальника
    accountant_name = models.TextField()  # имя бугалтера
    accountant_phone_num = models.CharField(max_length=20)  # номер бугалтера

    order_num = models.CharField(max_length=20)
    order_date = models.DateField()
    operator = models.CharField(max_length=150)
    branch_name = models.ForeignKey(AgroLeasingBranch, on_delete=models.SET_NULL, null=True)  # название филиала
    technique = models.ForeignKey(Technique, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "Order"
