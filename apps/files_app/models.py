from django.db import models

from apps.expert_assessment.models import ExpertAssessment
from apps.guarantee_agreem.models import Guarantor
from apps.orders.models import Order
from apps.leasing_agreem.models import LeasingAgreement
from apps.technics.models import Technique


class File(models.Model):
    name = models.CharField(max_length=300)
    gen_name = models.CharField(max_length=100)
    size = models.IntegerField()
    path = models.TextField()
    content_type = models.CharField(max_length=100)
    extension = models.CharField(max_length=30)

    technique = models.ForeignKey(Technique, on_delete=models.CASCADE, null=True, related_name='+')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='+')
    leasing_agreem = models.ForeignKey(LeasingAgreement, on_delete=models.CASCADE, null=True, related_name='+')
    guarantee_agreem = models.ForeignKey(Guarantor, on_delete=models.CASCADE, null=True, related_name='+')
    expert_assessment = models.ForeignKey(ExpertAssessment, on_delete=models.CASCADE, null=True, related_name='+')

    class Meta:
        db_table = "Uploads"
