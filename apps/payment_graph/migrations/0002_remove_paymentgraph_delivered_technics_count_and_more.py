# Generated by Django 4.0.4 on 2022-05-16 05:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('acts', '0004_rename_guarantor_sign_act_seller_sign'),
        ('payment_graph', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentgraph',
            name='delivered_technics_count',
        ),
        migrations.RemoveField(
            model_name='paymentgraph',
            name='leasing_agreem',
        ),
        migrations.RemoveField(
            model_name='paymentgraph',
            name='technique',
        ),
        migrations.AddField(
            model_name='paymentgraph',
            name='act',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='acts.act'),
        ),
        migrations.AddField(
            model_name='paymentgraph',
            name='days_count',
            field=models.SmallIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paymentgraph',
            name='last_payment_day',
            field=models.DateField(),
        ),
    ]