# Generated by Django 4.0.4 on 2022-06-07 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guarantee_agreem', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guarantor',
            name='stir',
        ),
    ]
