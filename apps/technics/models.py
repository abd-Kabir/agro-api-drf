from django.db import models


class Technique(models.Model):
    model = models.CharField(max_length=100)  # модель техники
    manufacturer = models.CharField(max_length=100)  # производитель
    country_name = models.CharField(max_length=100)  # страна
    leasing_term = models.IntegerField()  # срок лизинга
    price = models.BigIntegerField()  # цена техники
    prepaid_percent = models.IntegerField()  # предоплата - процент
    prepaid_price = models.BigIntegerField(null=True)  # предоплата - цена
    yearly_leasing_percent = models.IntegerField()  # годовой лизинговый процент
    subsidy = models.IntegerField(null=True)
    guarantors_num = models.IntegerField()  # число поручителей
    guarantee_bail = models.CharField(max_length=100)  # гарантия - залог
    insurance = models.CharField(max_length=100)  # страховка
    technique_manual = models.ForeignKey('files_app.File', on_delete=models.SET_NULL, null=True, related_name='+')
    # справочник техники
    technique_passport = models.ForeignKey('files_app.File', on_delete=models.SET_NULL, null=True, related_name='+')
    # паспорт техники
    type = models.ForeignKey('TechniqueType', on_delete=models.SET_NULL, null=True, related_name='+')
    name = models.ForeignKey('TechniqueName', on_delete=models.SET_NULL, null=True, related_name='+')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.prepaid_price is None or self.prepaid_percent == '':
            self.prepaid_price = self.price * self.prepaid_percent / 100
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        db_table = 'Technique'


class TechniqueName(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey('TechniqueType', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'TechniqueName'


class TechniqueType(models.Model):
    name = models.CharField(max_length=80)

    class Meta:
        db_table = 'TechniqueType'
