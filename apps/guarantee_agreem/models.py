from django.db import models

from apps.leasing_agreem.models import LeasingAgreement


class GuaranteeAgreement(models.Model):
    guarantors_signed_count = models.IntegerField(null=True)  # число подписанных

    guarantor = models.TextField()
    payment_solvency = models.ForeignKey('files_app.File', null=True, on_delete=models.CASCADE, related_name='+')
    financial_stability = models.ForeignKey('files_app.File', null=True, on_delete=models.CASCADE, related_name='+')
    business_plan = models.ForeignKey('files_app.File', null=True, on_delete=models.CASCADE, related_name='+')
    expert_opinion = models.ForeignKey('files_app.File', null=True, on_delete=models.CASCADE, related_name='+')
    leasing_agreem = models.ForeignKey(LeasingAgreement, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'GuaranteeAgreement'
