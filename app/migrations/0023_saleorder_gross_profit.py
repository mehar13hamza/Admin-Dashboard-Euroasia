# Generated by Django 3.0.5 on 2020-10-06 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20200927_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleorder',
            name='gross_profit',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]