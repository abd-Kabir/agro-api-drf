# Generated by Django 4.0.4 on 2022-06-16 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert_assessment', '0003_remove_expertassessment_leasing_agreem_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expertassessment',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
