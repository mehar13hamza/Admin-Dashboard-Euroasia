# Generated by Django 3.0.5 on 2020-09-23 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20200923_1518'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expenseentry',
            old_name='selling_price',
            new_name='purchase_price',
        ),
        migrations.RenameField(
            model_name='expenseentry',
            old_name='selling_quantity',
            new_name='purchase_quantity',
        ),
    ]