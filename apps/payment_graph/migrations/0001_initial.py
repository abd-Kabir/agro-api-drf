# Generated by Django 4.0.4 on 2022-06-07 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('acts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentGraph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('act', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='acts.act')),
            ],
            options={
                'db_table': 'PaymentGraph',
            },
        ),
        migrations.CreateModel(
            name='PaymentTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('residual_amount', models.FloatField()),
                ('date', models.DateField()),
                ('days_count', models.IntegerField()),
                ('quarterly_lease_term_part_of_value', models.FloatField()),
                ('quarterly_percent_lease_term_payment', models.FloatField()),
                ('quarterly_lease_term_payment', models.FloatField()),
                ('is_paid', models.BooleanField()),
                ('payment_graph', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment_graph.paymentgraph')),
            ],
            options={
                'db_table': 'PaymentTable',
            },
        ),
    ]
