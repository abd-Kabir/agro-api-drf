# Generated by Django 4.0.4 on 2022-06-27 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expert_assessment', '0010_expertassessment_district'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expertassessment',
            name='district',
        ),
    ]
