# Generated by Django 4.0.4 on 2022-06-16 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert_assessment', '0005_remove_expertassessment_expert_assessment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expertassessment',
            name='guarantors_count',
            field=models.SmallIntegerField(null=True),
        ),
    ]