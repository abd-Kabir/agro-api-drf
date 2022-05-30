# Generated by Django 4.0.4 on 2022-05-05 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
        ('guarantee_agreem', '0001_initial'),
        ('files_app', '0001_initial'),
        ('leasing_agreem', '0001_initial'),
        ('technics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='guarantee_agreem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='guarantee_agreem.guaranteeagreement'),
        ),
        migrations.AddField(
            model_name='file',
            name='leasing_agreem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='leasing_agreem.leasingagreement'),
        ),
        migrations.AddField(
            model_name='file',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='orders.order'),
        ),
        migrations.AddField(
            model_name='file',
            name='technique',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='technics.technique'),
        ),
    ]
