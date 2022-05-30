# Generated by Django 4.0.4 on 2022-05-24 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment_graph', '0005_paymenttable_paymentgraph_payment_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentgraph',
            name='payment_table',
        ),
        migrations.AddField(
            model_name='paymenttable',
            name='payment_graph',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment_graph.paymentgraph'),
        ),
    ]
