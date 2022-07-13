from django.db import models

from apps.regions.models import District
from apps.technics.models import Technique
from apps.tools.models import AgroLeasingBranch, FarmerSTIR


class Order(models.Model):
    order_num = models.CharField(max_length=20)
    order_date = models.DateField()
    operator = models.CharField(max_length=150)
    soato = models.CharField(max_length=30, null=True)

    branch_name = models.ForeignKey(AgroLeasingBranch, on_delete=models.SET_NULL, null=True)  # название филиала
    technique = models.ForeignKey(Technique, on_delete=models.SET_NULL, null=True)
    farmer_stir = models.ForeignKey(FarmerSTIR, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "Order"


class Statement(models.Model):
    statement_date = models.DateField(auto_now_add=True, null=True)
    statement_num = models.CharField(max_length=20, null=True)
    statement_type = models.TextField(null=True)

    payment_solvency_file = models.ForeignKey('files_app.File', null=True, on_delete=models.CASCADE, related_name='+')
    business_plan_file = models.ForeignKey('files_app.File', null=True, on_delete=models.CASCADE, related_name='+')
    expert_opinion_file = models.ForeignKey('files_app.File', null=True, on_delete=models.CASCADE, related_name='+')
    financial_stability_file = models.ForeignKey('files_app.File', null=True, on_delete=models.CASCADE,
                                                 related_name='+')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "Statement"


class FuturesContract(models.Model):
    futures_contract_num = models.CharField(max_length=20, null=True)
    futures_contract_date = models.DateField(null=True)
    harvest_year = models.IntegerField(null=True)
    type_of_grown_product = models.CharField(max_length=20, null=True)
    contour_of_crop = models.CharField(max_length=20, null=True)
    hectares_of_arable_land = models.IntegerField(null=True)
    financing_percent = models.IntegerField(null=True)
    financing_price = models.BigIntegerField(null=True)
    contract_price = models.BigIntegerField(null=True)

    statement = models.ForeignKey(Statement, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "FuturesContract"


class ExpertsStatement(models.Model):
    jshshir = models.BigIntegerField()
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)

    statement = models.ForeignKey(Statement, on_delete=models.CASCADE, null=True)
