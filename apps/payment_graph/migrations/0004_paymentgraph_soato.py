# Generated by Django 4.0.4 on 2022-06-21 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_graph', '0003_alter_paymentgraph_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentgraph',
            name='soato',
            field=models.CharField(max_length=30, null=True),
        ),
    ]