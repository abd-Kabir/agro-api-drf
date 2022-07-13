from django.db import models

from apps.tools.models import FarmerSTIR


class GuaranteeAgreement(models.Model):
    guarantee_num = models.CharField(max_length=20)
    guarantee_date = models.DateField()
    is_active = models.BooleanField(default=False)

    lessor_sign = models.CharField(max_length=12, null=True)  # арендодатель подпись
    lessee_sign = models.CharField(max_length=12, null=True)  # арендатор подпись
    leasing_agreem = models.ForeignKey("leasing_agreem.LeasingAgreement", null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'GuaranteeAgreement'


class Guarantor(models.Model):
    payment_obligation = models.CharField(max_length=20)

    farmer_stir = models.ForeignKey(FarmerSTIR, on_delete=models.SET_NULL, null=True)
    payment_solvency_file = models.ForeignKey('files_app.File', null=True, on_delete=models.CASCADE, related_name='+')
    business_plan_file = models.ForeignKey('files_app.File', null=True, on_delete=models.CASCADE, related_name='+')
    expert_opinion_file = models.ForeignKey('files_app.File', null=True, on_delete=models.CASCADE, related_name='+')
    financial_stability_file = models.ForeignKey('files_app.File', null=True, on_delete=models.CASCADE,
                                                 related_name='+')
    guarantor_sign = models.CharField(max_length=12, null=True)  # поручитель подпись
    guarantee_agreem = models.ForeignKey(GuaranteeAgreement, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'Guarantor'
