# Generated by Django 4.0.4 on 2022-05-05 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Act',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('act_num', models.CharField(max_length=20)),
                ('act_date', models.DateField()),
                ('lessor_sign', models.CharField(default=None, max_length=12, null=True)),
                ('lessee_sign', models.CharField(default=None, max_length=12, null=True)),
                ('guarantor_sign', models.CharField(default=None, max_length=12, null=True)),
                ('seller', models.CharField(default='APIdan keladi', max_length=60)),
                ('detected_defects_header', models.CharField(max_length=40)),
                ('detected_defects_info', models.TextField()),
                ('quality_conclusion_header', models.CharField(max_length=40)),
                ('quality_conclusion_info', models.TextField()),
            ],
            options={
                'db_table': 'Act',
            },
        ),
        migrations.CreateModel(
            name='Trustee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stir', models.CharField(max_length=20)),
                ('fullname', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=13)),
                ('trust_num', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('postal_code', models.IntegerField()),
            ],
        ),
    ]
