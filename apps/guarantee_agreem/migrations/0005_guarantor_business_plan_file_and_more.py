# Generated by Django 4.0.4 on 2022-06-07 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files_app', '0002_initial'),
        ('guarantee_agreem', '0004_remove_guarantor_business_plan_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='guarantor',
            name='business_plan_file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='files_app.file'),
        ),
        migrations.AddField(
            model_name='guarantor',
            name='expert_opinion_file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='files_app.file'),
        ),
        migrations.AddField(
            model_name='guarantor',
            name='financial_stability_file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='files_app.file'),
        ),
        migrations.AddField(
            model_name='guarantor',
            name='guarantee_agreem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='guarantee_agreem.guaranteeagreement'),
        ),
        migrations.AddField(
            model_name='guarantor',
            name='guarantor_sign',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='guarantor',
            name='payment_solvency_file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='files_app.file'),
        ),
        migrations.AddField(
            model_name='guarantor',
            name='stir',
            field=models.BigIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='guarantor',
            table='Guarantor',
        ),
    ]