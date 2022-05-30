from django.db import models


class AgroLeasingBranch(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'AgroLeasingBranch'
