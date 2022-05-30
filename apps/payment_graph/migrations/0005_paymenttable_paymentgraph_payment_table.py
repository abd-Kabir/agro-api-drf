# Generated by Django 4.0.4 on 2022-05-24 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment_graph', '0004_remove_paymentgraph_total_quarterly_lease_term_part_of_value_and_more'),
    ]

    operations = [
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
            ],
            options={
                'db_table': 'PaymentTable',
            },
        ),
        migrations.AddField(
            model_name='paymentgraph',
            name='payment_table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment_graph.paymenttable'),
        ),
    ]
