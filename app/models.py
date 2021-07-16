from django.db import models
import datetime
# Create your models here.
import requests

class admin(models.Model):
    username = models.CharField(max_length=150, null=False)
    password = models.CharField(max_length=150, null=False)

class Currency(models.Model):
    currency_name = models.CharField(max_length=150, null=False)
    currency_symbol = models.CharField(max_length=150, null=False)
    abbreviation = models.CharField(max_length=150)




class seller(models.Model):
    seller_id = models.CharField(max_length=150, null=False)
    seller_company = models.CharField(max_length=150, null=False)
    email = models.EmailField(max_length=150, blank=True)
    seller_phone = models.CharField(max_length=150, blank=True)
    seller_type = models.CharField(max_length=150, null=False)
    seller_mobile = models.CharField(max_length=150, blank=True)
    seller_fax = models.CharField(max_length=150, blank=True)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=150, blank=True)
    postal_code = models.CharField(max_length=150, blank=True)
    currency = models.ForeignKey(Currency, related_name="seller", on_delete=models.CASCADE)
    opening_balance = models.FloatField(null=False)
    pdf_attachment_box = models.FileField(upload_to="Files", blank=True)
    notes = models.TextField(blank=True)

class Customer(models.Model):
    customer_id = models.CharField(max_length=150, null=False)
    customer_name = models.CharField(max_length=150, null=False)
    customer_phone = models.CharField(max_length=150, blank=True)
    customer_type = models.CharField(max_length=150, null=False)
    customer_mobile = models.CharField(max_length=150, blank=True)
    customer_fax = models.CharField(max_length=150, blank=True)
    billing_address = models.TextField(null=False)
    shipping_address = models.TextField(null=False)
    city = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=150, blank=True)
    postal_code = models.CharField(max_length=150, blank=True)
    currency = models.ForeignKey(Currency, related_name="customer", on_delete=models.CASCADE)
    bank_account_iban = models.CharField(max_length=150, blank=True)
    bank_account_title = models.CharField(max_length=150, blank=True)
    opening_balance = models.FloatField(null=False)
    pdf_attachment_box = models.FileField(upload_to="Files", blank=True)
    notes = models.TextField(blank=True)



class Transport(models.Model):
    transport_company_id = models.CharField(max_length=150, null=False)
    transport_company_name = models.CharField(max_length=150, null=False)
    transport_company_address = models.TextField(null=False)
    transport_company_city = models.CharField(max_length=150, blank=True)
    transport_company_country = models.CharField(max_length=150, blank=True)
    transport_company_postal_code = models.CharField(max_length=150, blank=True)
    transport_company_account_currency = models.ForeignKey(Currency, related_name='transport', on_delete=models.CASCADE)
    pdf_attachment_box = models.FileField(upload_to='Files', blank=True)
    notes = models.TextField(blank=True)

class Employee(models.Model):
    employee_id = models.CharField(max_length=150, null=False)
    employee_name = models.CharField(max_length=150, null=False)
    employee_address = models.TextField(null=False)
    city = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=150, blank=True)
    postal_code = models.CharField(max_length=150, blank=True)
    currency = models.ForeignKey(Currency, related_name="employee", on_delete=models.CASCADE)
    pdf_attachment_box = models.FileField(upload_to="Files", blank=True)
    notes = models.TextField(blank=True)


class BankAccount(models.Model):
    bank_account_id = models.CharField(max_length=150, null=False)
    bank_account_title = models.CharField(max_length=150, null=False)
    bank_account_name = models.CharField(max_length=150, null=False)
    bank_account_address = models.TextField(null=False)
    opening_balance = models.FloatField(null=False)
    net_balance = models.FloatField()
    city = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=150, blank=True)
    postal_code = models.CharField(max_length=150, blank=True)
    currency = models.ForeignKey(Currency, related_name="bank_account", on_delete=models.CASCADE)
    pdf_attachment_box = models.FileField(upload_to="Files", blank=True)
    notes = models.TextField(blank=True)

    def get_net_balance(self):
        return self.opening_balance


    def save(self, *args, **kwargs):
        if not self.net_balance:
            self.net_balance = self.get_net_balance()

        super().save(*args, **kwargs)



class PurchaseOrder(models.Model):
    order_receipt_no = models.CharField(max_length=300,null=False)
    order_date = models.DateField()
    seller = models.ForeignKey(seller, related_name="purchase_order_seller", on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=150, null=False)
    material = models.CharField(max_length=150,blank=True, null=True)
    purchase_quantity = models.IntegerField(null=False)
    unit = models.CharField(max_length=150, null=False)
    purchase_price = models.FloatField(null=False)
    freight_cost = models.FloatField(blank=True)
    freight_company = models.ForeignKey(Transport, related_name="purchase_order_freight_company", on_delete=models.CASCADE, blank=True, null=True)
    container_no = models.IntegerField(null=False)
    advance = models.FloatField(null=False)
    advance_currency = models.ForeignKey(Currency, related_name="purchase_order_advance_currency", on_delete=models.CASCADE)
    seller_currency = models.ForeignKey(Currency, related_name="purchase_order_currency", on_delete=models.CASCADE)
    payment_due_date = models.DateField()
    bank_account_payment = models.ForeignKey(BankAccount, related_name="bank_account_payment_purchase_order", on_delete=models.CASCADE)
    pdf_attachment_box = models.FileField(upload_to="Files", blank=True)
    notes = models.TextField(blank=True, null=True)
    exchange_rate = models.FloatField(null=False)
    total = models.FloatField()
    payment_remaining = models.FloatField()
    display_name = models.TextField(null=False)

    def get_display_name(self):
        return str(self.seller.seller_company) + " " + str(self.material) + " " + str(self.order_date)


    def get_total(self):
        if not(self.freight_cost):
            self.freight_cost = 0

        return round((self.purchase_quantity * self.purchase_price) + self.freight_cost, 2)

    def get_payment_remaining(self):
        return round(self.total - self.advance * self.exchange_rate  , 2)


    def save(self, *args, **kwargs):
        if not self.total:
            self.total = self.get_total()
        if not self.payment_remaining:
            self.payment_remaining = self.get_payment_remaining()
        if not self.display_name:
            self.display_name = self.get_display_name()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_receipt_no



class SaleOrder(models.Model):
    order_invoice_no = models.CharField(max_length=300,null=False)
    order_date = models.DateField()
    customer = models.ForeignKey(Customer, related_name="sale_order", on_delete=models.CASCADE)
    customer_account_currency = models.ForeignKey(Currency, related_name="sale_order_customer_currency", on_delete=models.CASCADE)
    material = models.CharField(max_length=150, blank=True)
    purchase_order = models.ForeignKey(PurchaseOrder, related_name="sale_order_purchase_order", on_delete=models.CASCADE)
    selling_quantity = models.IntegerField(null=False)
    selling_price = models.FloatField(null=False)
    date_of_arrival = models.DateField()
    advance = models.FloatField(null=False)
    currency = models.ForeignKey(Currency, related_name="sale_order_currency", on_delete=models.CASCADE)
    payment_due_date = models.DateField()
    payment_method = models.CharField(max_length=150, null=False)
    bank_account_payment = models.ForeignKey(BankAccount, related_name="bank_account_payment_sale_order", on_delete=models.CASCADE)
    pdf_attachment_box = models.FileField(upload_to="Files", blank=True)
    notes = models.TextField(blank=True)
    exchange_rate = models.FloatField(null=False)
    total = models.FloatField(null=False)
    gross_profit = models.FloatField()
    payment_remaining = models.FloatField()
    display_name = models.TextField(null=False)
    admin_cost = models.FloatField(null=False)
    unit = models.CharField(max_length=150, null=False)
    banking_charges = models.FloatField()
    amount_received = models.FloatField()



    def get_display_name(self):
        return str(self.customer.customer_name) + " " + str(self.material) + " " + str(self.order_date)

    def get_profit(self):
        base_currency = self.purchase_order.seller_currency.abbreviation
        secondary_currency = self.currency.abbreviation
        print(base_currency+" "+secondary_currency)
        ex_rate = ExchangeRates.objects.filter(base_currency=base_currency,secondary_currency=secondary_currency)[0].exchange_rate

        return round(self.total - self.purchase_order.total * float(ex_rate) , 2)

    def get_payment_remaining(self):
        return round(self.total - self.advance * self.exchange_rate  , 2)

    def save(self, *args, **kwargs):
        if not self.gross_profit:
            self.gross_profit = self.get_profit()
        if not self.payment_remaining:
            self.payment_remaining = self.get_payment_remaining()
        if not self.display_name:
            self.display_name = self.get_display_name()

        super().save(*args, **kwargs)

class ExpenseEntry(models.Model):
    expense_id = models.CharField(max_length=300, null=False)
    expense_type = models.CharField(max_length=150, null=False)
    expense_date = models.DateField()
    material = models.CharField(max_length=150, blank=True)
    currency = models.ForeignKey(Currency, related_name="expense_currency", on_delete=models.CASCADE)
    bankaccount = models.ForeignKey(BankAccount, related_name="bank_account_expense", on_delete=models.CASCADE)
    expense_quantity = models.IntegerField(null=False)
    expense_cost = models.FloatField(null=False)
    amount = models.FloatField(null=False)
    payment_remaining = models.FloatField(null=False)
    pdf_attachment_box = models.FileField(upload_to="Files", blank=True)
    notes = models.TextField(blank=True)
    total = models.FloatField()

    def get_total(self):
        return round(self.expense_quantity*self.expense_cost, 2)

    def get_payment_remaining(self):
        return round(self.total-self.amount, 2)

    def save(self, *args, **kwargs):
        if not self.total:
            self.total = self.get_total()
        if not self.payment_remaining:
            self.payment_remaining = self.get_payment_remaining()


        super().save(*args, **kwargs)

class NewExpense(models.Model):
    expense_id = models.ForeignKey(ExpenseEntry, related_name="expense_id_new_expense", on_delete=models.CASCADE)
    expense_type = models.CharField(max_length=150, null=False)
    expense_date = models.DateField()
    material = models.CharField(max_length=150, blank=True)
    currency = models.ForeignKey(Currency, related_name="new_expense_currency", on_delete=models.CASCADE)
    bankaccount = models.ForeignKey(BankAccount, related_name="new_bank_account_expense", on_delete=models.CASCADE)
    amount = models.FloatField(null=False)
    payment_remaining = models.FloatField(null=False)
    pdf_attachment_box = models.FileField(upload_to="Files", blank=True)
    notes = models.TextField(blank=True)


class PaymentReceived(models.Model):
    order_invoice_no = models.ForeignKey(SaleOrder, related_name="payment_received", on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.FloatField()
    currency = models.ForeignKey(Currency, related_name="payment_received_currency", on_delete=models.CASCADE)
    bankaccount = models.ForeignKey(BankAccount, related_name="payment_received_bank_account", on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=150, null=False)
    payment_remaining = models.FloatField()
    exchange_rate = models.FloatField()
    pdf_attachment_box = models.FileField(upload_to="Files", blank=True)
    notes = models.TextField(blank=True)
    banking_charges = models.FloatField()
    amount_received = models.FloatField()

    def amount_in_selling_currency(self):
        return self.amount / self.exchange_rate

    def gains_losses(self, a,b):
        return a-b

class PaymentMade(models.Model):
    purchase_order_receipt_no = models.ForeignKey(PurchaseOrder, related_name="purchase_order_receipt_no", on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.FloatField()
    currency = models.ForeignKey(Currency, related_name="payment_made_currency", on_delete=models.CASCADE)
    bankaccount = models.ForeignKey(BankAccount, related_name="payment_made_bank_account", on_delete=models.CASCADE)
    pdf_attachment_box = models.FileField(upload_to="Files", blank=True)
    notes = models.TextField(blank=True)
    payment_remaining = models.FloatField()
    exchange_rate = models.FloatField()

class ExchangeRates(models.Model):
    base_currency = models.CharField(max_length=150, null=False)
    secondary_currency = models.CharField(max_length=150, null=False)
    exchange_rate = models.FloatField()
