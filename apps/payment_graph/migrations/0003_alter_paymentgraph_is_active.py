# Generated by Django 4.0.4 on 2022-06-20 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_graph', '0002_paymentgraph_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentgraph',
            name='is_active',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
