# Generated by Django 4.0.4 on 2022-06-07 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guarantee_agreem', '0003_guarantor_stir'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guarantor',
            name='business_plan_file',
        ),
        migrations.RemoveField(
            model_name='guarantor',
            name='expert_opinion_file',
        ),
        migrations.RemoveField(
            model_name='guarantor',
            name='financial_stability_file',
        ),
        migrations.RemoveField(
            model_name='guarantor',
            name='guarantee_agreem',
        ),
        migrations.RemoveField(
            model_name='guarantor',
            name='guarantor_sign',
        ),
        migrations.RemoveField(
            model_name='guarantor',
            name='payment_solvency_file',
        ),
        migrations.RemoveField(
            model_name='guarantor',
            name='stir',
        ),
        migrations.AlterModelTable(
            name='guarantor',
            table=None,
        ),
    ]
