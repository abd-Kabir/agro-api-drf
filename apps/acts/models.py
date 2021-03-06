from django.db import models

from apps.leasing_agreem.models import LeasingAgreement
from apps.tools.models import AgroLeasingBranch, FarmerSTIR


class Trustee(models.Model):
    stir = models.CharField(null=True, max_length=20)
    fullname = models.CharField(null=True, max_length=50)
    phone_number = models.CharField(null=True, max_length=13)
    trust_num = models.CharField(null=True, max_length=50)
    date = models.DateField(null=True)
    postal_code = models.IntegerField(null=True)


class Act(models.Model):
    act_num = models.CharField(max_length=20, null=True)
    act_date = models.DateField(null=True)
    seller_stir = models.ForeignKey(FarmerSTIR, on_delete=models.SET_NULL, null=True)  # продавец
    seller_sign = models.CharField(max_length=12, null=True, default=None)  # продавец подпись
    lessor_sign = models.CharField(max_length=12, null=True, default=None)  # арендодатель подпись
    lessee_sign = models.CharField(max_length=12, null=True, default=None)  # арендатор подпись
    detected_defects_header = models.CharField(max_length=40, null=True)  # заголовок об обнаруженных дефектах
    detected_defects_info = models.TextField(null=True)  # текст-ареа, обнаруженных дефектах
    quality_conclusion_header = models.CharField(max_length=40, null=True)  # заголовок заключения о качестве
    quality_conclusion_info = models.TextField(null=True)  # информация о заключении по качеству
    is_delivered = models.BooleanField(default=False)

    trustee = models.ForeignKey(Trustee, on_delete=models.SET_NULL, null=True,
                                related_name='+')  # доверенный представитель
    leasing_agreem = models.ForeignKey(LeasingAgreement, on_delete=models.SET_NULL, null=True)
    branch_name = models.ForeignKey(AgroLeasingBranch, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'Act'
