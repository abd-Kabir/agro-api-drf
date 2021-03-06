# Generated by Django 4.0.4 on 2022-06-07 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('acts', '0001_initial'),
        ('leasing_agreem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='act',
            name='leasing_agreem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='leasing_agreem.leasingagreement'),
        ),
        migrations.AddField(
            model_name='act',
            name='trustee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='acts.trustee'),
        ),
    ]
