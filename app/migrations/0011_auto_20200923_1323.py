# Generated by Django 3.0.5 on 2020-09-23 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20200923_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='order_receipt_no',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='saleorder',
            name='order_invoice_no',
            field=models.CharField(max_length=300),
        ),
    ]
