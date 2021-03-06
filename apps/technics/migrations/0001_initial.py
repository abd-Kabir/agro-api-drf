# Generated by Django 4.0.4 on 2022-06-07 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('files_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechniqueType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'TechniqueType',
            },
        ),
        migrations.CreateModel(
            name='TechniqueName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='technics.techniquetype')),
            ],
            options={
                'db_table': 'TechniqueName',
            },
        ),
        migrations.CreateModel(
            name='Technique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100)),
                ('manufacturer', models.CharField(max_length=100)),
                ('country_name', models.CharField(max_length=100)),
                ('leasing_term', models.IntegerField()),
                ('price', models.BigIntegerField()),
                ('prepaid_percent', models.IntegerField()),
                ('prepaid_price', models.BigIntegerField(null=True)),
                ('yearly_leasing_percent', models.IntegerField()),
                ('subsidy', models.IntegerField(null=True)),
                ('guarantors_num', models.IntegerField()),
                ('guarantee_bail', models.CharField(max_length=100)),
                ('insurance', models.CharField(max_length=100)),
                ('name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='technics.techniquename')),
                ('technique_manual', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='files_app.file')),
                ('technique_passport', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='files_app.file')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='technics.techniquetype')),
            ],
            options={
                'db_table': 'Technique',
            },
        ),
    ]
