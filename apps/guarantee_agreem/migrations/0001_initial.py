# Generated by Django 4.0.4 on 2022-05-05 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('files_app', '0001_initial'),
        ('leasing_agreem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuaranteeAgreement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guarantors_signed_count', models.IntegerField(null=True)),
                ('guarantor', models.TextField()),
                ('business_plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='files_app.file')),
                ('expert_opinion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='files_app.file')),
                ('financial_stability', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='files_app.file')),
                ('leasing_agreem', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='leasing_agreem.leasingagreement')),
                ('payment_solvency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='files_app.file')),
            ],
            options={
                'db_table': 'GuaranteeAgreement',
            },
        ),
    ]
