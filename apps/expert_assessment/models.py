from django.db import models

from apps.regions.models import District
from apps.tools.models import AgroLeasingBranch


class ExpertAssessment(models.Model):
    expert_assessment_num = models.CharField(max_length=20)
    expert_assessment_date = models.DateField()

    guarantors_count = models.SmallIntegerField(null=True)
    is_active = models.BooleanField(default=False)

    order_model = models.ForeignKey('orders.Order', null=True, on_delete=models.SET_NULL)
    branch_name = models.ForeignKey(AgroLeasingBranch, null=True, on_delete=models.SET_NULL)

    payment_solvency_file = models.ForeignKey('files_app.File', null=True, on_delete=models.CASCADE, related_name='+')
    business_plan_file = models.ForeignKey('files_app.File', null=True, on_delete=models.CASCADE, related_name='+')
    expert_opinion_file = models.ForeignKey('files_app.File', null=True, on_delete=models.CASCADE, related_name='+')
    financial_stability_file = models.ForeignKey('files_app.File', null=True, on_delete=models.CASCADE,
                                                 related_name='+')

    class Meta:
        db_table = 'ExpertAssessment'
