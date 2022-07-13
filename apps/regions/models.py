from django.db import models


class Province(models.Model):
    name = models.TextField(null=False)
    nameru = models.TextField(null=True)
    region_prefix = models.TextField(null=False)
    soato_code = models.TextField(null=True)

    class Meta:
        db_table = 'Province'


class District(models.Model):
    name = models.TextField(null=True)
    nameru = models.TextField(null=True)
    district_prefix = models.TextField(null=False)
    soato_code = models.TextField(null=True)

    region_id = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'District'


class MFY(models.Model):
    name = models.TextField(null=True)
    nameru = models.TextField(null=True)
    mfy_prefix = models.TextField(null=False)
    soato_code = models.TextField(null=True)

    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'MFY'
