from django.db import models


class AgroLeasingBranch(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'AgroLeasingBranch'


class FarmerSTIR(models.Model):
    stir = models.CharField(max_length=9, null=True)
    full_name = models.CharField(max_length=60, null=True)
    short_name = models.CharField(max_length=40, null=True)
    business_type = models.CharField(max_length=40, null=True)
    business_structure = models.CharField(max_length=40, null=True)
    legal_address = models.CharField(max_length=200, null=True)
    postcode = models.CharField(max_length=20, null=True)
    home_address = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    bank_name = models.CharField(max_length=50, null=True)
    mfo = models.CharField(max_length=20, null=True)
    payment_account = models.CharField(max_length=20, null=True)
    director = models.CharField(max_length=60, null=True)
    director_number = models.CharField(max_length=20, null=True)
    accountant = models.CharField(max_length=60, null=True)
    accountant_number = models.CharField(max_length=20, null=True)

    soato = models.CharField(max_length=30, null=True)

    class Meta:
        db_table = 'FarmerSTIR'
