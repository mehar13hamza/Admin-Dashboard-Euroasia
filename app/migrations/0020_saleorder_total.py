# Generated by Django 3.0.5 on 2020-09-23 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_paymentreceived_exchange_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleorder',
            name='total',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]