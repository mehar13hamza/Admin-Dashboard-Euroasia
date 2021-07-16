# Generated by Django 3.0.5 on 2020-10-26 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_auto_20201027_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='freight_company',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchase_order_freight_company', to='app.Transport'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='freight_cost',
            field=models.FloatField(blank=True),
        ),
    ]