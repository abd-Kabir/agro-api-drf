from django.db import models


class Region(models.Model):
    region_id = models.IntegerField(unique=True)
    regioncode = models.IntegerField()
    regioncode2 = models.IntegerField(null=True)
    nameru = models.CharField(max_length=60)
    nameuz = models.CharField(max_length=60)
    codelat = models.CharField(max_length=2)
    codecyr = models.CharField(max_length=2)
    admincenterru = models.CharField(max_length=30, null=True)
    admincenteruz = models.CharField(max_length=30, null=True)
    isdeleted = models.SmallIntegerField(null=True, default=0)

    class Meta:
        db_table = 'Region'


class District(models.Model):
    district_id = models.IntegerField(unique=True)
    region_id = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True,
                                  to_field="region_id", db_column="region_id")
    areacode = models.IntegerField()
    areatype = models.TextField(null=True)
    nameru = models.CharField(max_length=60)
    nameuz = models.CharField(max_length=60)
    admincenterru = models.CharField(max_length=30, null=True)
    admincenteruz = models.CharField(max_length=30, null=True)
    isdeleted = models.SmallIntegerField(null=True, default=0)

    class Meta:
        db_table = 'District'


class MFY(models.Model):
    mfy_id = models.IntegerField()
    district_id = models.ForeignKey(District, on_delete=models.SET_NULL, null=True,
                                    to_field="district_id", db_column="district_id")
    region_id = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True,
                                  to_field="region_id", db_column="region_id")
    nameuz = models.CharField(max_length=60, null=True)
    nameru = models.CharField(max_length=60, null=True)
    created_at = models.CharField(max_length=60)
    updated_at = models.CharField(max_length=60)

    class Meta:
        db_table = 'MFY'
