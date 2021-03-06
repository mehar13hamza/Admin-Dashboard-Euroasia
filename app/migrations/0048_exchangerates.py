# Generated by Django 3.0.5 on 2020-11-02 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0047_auto_20201201_2350'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_date', models.DateField()),
                ('base_currency', models.CharField(max_length=150)),
                ('secondary_currency', models.CharField(max_length=150)),
                ('exchange_rate', models.FloatField()),
            ],
        ),
    ]
