# Generated by Django 3.0.5 on 2020-09-23 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_saleorder_payment_method'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentReceived',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField()),
                ('amount', models.FloatField()),
                ('payment_method', models.CharField(max_length=150)),
                ('payment_remaining', models.FloatField()),
                ('pdf_attachment_box', models.FileField(blank=True, upload_to='Files')),
                ('notes', models.CharField(max_length=150)),
                ('bankaccount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_received_bank_account', to='app.BankAccount')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_received_currency', to='app.Currency')),
                ('order_invoice_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_received', to='app.SaleOrder')),
            ],
        ),
    ]