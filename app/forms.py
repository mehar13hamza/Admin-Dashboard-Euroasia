from django import forms
from .models import admin, seller, Customer, Currency, Transport, Employee, BankAccount, SaleOrder, PurchaseOrder, ExpenseEntry, PaymentReceived, PaymentMade, NewExpense, ExchangeRates

class adminForm(forms.ModelForm):
    class Meta:
        model = admin
        fields = [
            'username',
            'password',


        ]

class sellerForm(forms.ModelForm):
    class Meta:
        model = seller
        fields = [

            'seller_id',
            'seller_company',
            'email',
            'seller_phone',
            'seller_type',
            'seller_mobile',
            'seller_fax',
            'address',
            'city',
            'country',
            'postal_code',
            'currency',
            'opening_balance',
            'pdf_attachment_box',
            'notes'
        ]


class customerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [

            'customer_id',
            'customer_name',
            'customer_phone',
            'customer_type',
            'customer_mobile',
            'customer_fax',
            'billing_address',
            'shipping_address',
            'city',
            'country',
            'postal_code',
            'currency',
            'bank_account_iban',
            'bank_account_title',
            'opening_balance',
            'pdf_attachment_box',
            'notes',


        ]

class currencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = [

            'currency_name',
            'currency_symbol',
            'abbreviation'

        ]

class transportForm(forms.ModelForm):
    class Meta:
        model = Transport
        fields = [

            'transport_company_id',
            'transport_company_name',
            'transport_company_address',
            'transport_company_city',
            'transport_company_country',
            'transport_company_postal_code',
            'transport_company_account_currency',
            'pdf_attachment_box',
            'notes'
        ]


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [

            'employee_id',
            'employee_name',
            'employee_address',
            'city',
            'country',
            'postal_code',
            'currency',
            'pdf_attachment_box',
            'notes'


        ]

class purchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = [

            'order_receipt_no',
            'order_date',
            'seller',
            'transaction_type',
            'material',
            'purchase_quantity',
            'unit',
            'purchase_price',
            'freight_cost',
            'freight_company',
            'container_no',
            'advance',
            'advance_currency',
            'seller_currency',
            'payment_due_date',
            'bank_account_payment',
            'pdf_attachment_box',
            'notes',
            'exchange_rate',



        ]


class saleOrderForm(forms.ModelForm):
    class Meta:
        model = SaleOrder
        fields = [

            'order_invoice_no',
            'order_date',
            'customer',
            'customer_account_currency',
            'material',
            'purchase_order',
            'selling_quantity',
            'selling_price',
            'date_of_arrival',
            'advance',
            'currency',
            'payment_due_date',
            'payment_method',
            'bank_account_payment',
            'pdf_attachment_box',
            'notes',
            'exchange_rate',
            'total',
            'admin_cost',
            'unit',
            'banking_charges',
            'amount_received'

        ]



class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = [

            'bank_account_id',
            'bank_account_title',
            'bank_account_name',
            'bank_account_address',
            'opening_balance',
            'city',
            'country',
            'postal_code',
            'currency',
            'pdf_attachment_box',
            'notes'



        ]


class expenseEntryForm(forms.ModelForm):
    class Meta:
        model = ExpenseEntry
        fields = [

            'expense_id',
            'expense_type',
            'expense_date',
            'material',
            'currency',
            'bankaccount',
            'expense_quantity',
            'expense_cost',
            'amount',
            'pdf_attachment_box',
            'notes',

        ]


class newExpenseForm(forms.ModelForm):
    class Meta:
        model = NewExpense
        fields = [

            'expense_id',
            'expense_type',
            'expense_date',
            'material',
            'currency',
            'bankaccount',
            'amount',
            'payment_remaining',
            'pdf_attachment_box',
            'notes',

        ]


class paymentReceivedForm(forms.ModelForm):
    class Meta:
        model = PaymentReceived
        fields = [

            'order_invoice_no',
            'payment_date',
            'amount',
            'currency',
            'bankaccount',
            'payment_method',
            'payment_remaining',
            'exchange_rate',
            'pdf_attachment_box',
            'notes',
            'banking_charges',
            'amount_received'

        ]



class paymentMadeForm(forms.ModelForm):
    class Meta:
        model = PaymentMade
        fields = [
            'purchase_order_receipt_no',
            'payment_date',
            'amount',
            'currency',
            'bankaccount',
            'pdf_attachment_box',
            'notes',
            'payment_remaining',
            'exchange_rate',

        ]

class exchangeRatesForm(forms.ModelForm):
    class Meta:
        model = ExchangeRates
        fields = [

            'base_currency',
            'secondary_currency',
            'exchange_rate'


        ]


class updateTransportForm(forms.ModelForm):
    class Meta:
        model = Transport
        fields = [

            'transport_company_id',
            'transport_company_name',
            'transport_company_address',
            'transport_company_city',
            'transport_company_country',
            'transport_company_postal_code',
            'transport_company_account_currency',
            'pdf_attachment_box',
            'notes'
        ]

        def save(self, commit=True):
            transport = self.instance
            transport.transport_company_id = self.cleaned_data['transport_company_id']
            transport.transport_company_name = self.cleaned_data['transport_company_name']
            transport.transport_company_address = self.cleaned_data['transport_company_address']
            transport.transport_company_city = self.cleaned_data['transport_company_city']
            transport.transport_company_country = self.cleaned_data['transport_company_country']
            transport.transport_company_postal_code = self.cleaned_data['transport_company_postal_code']
            transport.notes = self.cleaned_data['notes']

            if self.cleaned_data['pdf_attachment_box']:
                transport.pdf_attachment_box = self.cleaned_data['pdf_attachment_box']

            if commit:
                transport.save()
            return transport



class updateSellerForm(forms.ModelForm):
    class Meta:
        model = seller
        fields = [

            'seller_id',
            'seller_company',
            'email',
            'seller_phone',
            'seller_type',
            'seller_mobile',
            'seller_fax',
            'address',
            'city',
            'country',
            'postal_code',
            'currency',
            'opening_balance',
            'pdf_attachment_box',
            'notes'



        ]

        def save(self, commit=True):
            seller = self.instance
            seller.seller_id = self.cleaned_data['seller_id']
            seller.seller_company = self.cleaned_data['seller_company']
            seller.email = self.cleaned_data['email']
            seller.seller_phone = self.cleaned_data['seller_phone']
            seller.seller_type = self.cleaned_data['seller_type']
            seller.seller_mobile = self.cleaned_data['seller_mobile']
            seller.seller_fax = self.cleaned_data['seller_fax']
            seller.others = self.cleaned_data['others']
            seller.website = self.cleaned_data['website']
            seller.billing_address = self.cleaned_data['billing_address']
            seller.city = self.cleaned_data['city']
            seller.country = self.cleaned_data['country']
            seller.postal_code = self.cleaned_data['postal_code']
            seller.currency = self.cleaned_data['currency']
            seller.opening_balance = self.cleaned_data['opening_balance']
            seller.terms = self.cleaned_data['terms']
            seller.notes = self.cleaned_data['notes']
            seller.location = self.cleaned_data['location']


            if self.cleaned_data['pdf_attachment_box']:
                seller.pdf_attachment_box = self.cleaned_data['pdf_attachment_box']

            if commit:
                seller.save()
            return seller


class updateCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [

            'customer_id',
            'customer_name',
            'customer_phone',
            'customer_type',
            'customer_mobile',
            'customer_fax',
            'billing_address',
            'shipping_address',
            'city',
            'country',
            'postal_code',
            'currency',
            'bank_account_iban',
            'bank_account_title',
            'opening_balance',
            'pdf_attachment_box',
            'notes',




        ]

        def save(self, commit=True):
            customer = self.instance
            customer.customer_id = self.cleaned_data['customer_id']
            customer.customer_name = self.cleaned_data['customer_name']
            customer.customer_phone = self.cleaned_data['customer_phone']
            customer.customer_type = self.cleaned_data['customer_type']
            customer.customer_mobile = self.cleaned_data['customer_mobile']
            customer.customer_fax = self.cleaned_data['customer_fax']
            customer.others = self.cleaned_data['others']
            customer.website = self.cleaned_data['website']
            customer.billing_address = self.cleaned_data['billing_address']
            customer.city = self.cleaned_data['city']
            customer.country = self.cleaned_data['country']
            customer.postal_code = self.cleaned_data['postal_code']
            customer.currency = self.cleaned_data['currency']
            customer.bank_account_iban = self.cleaned_data['bank_account_iban']
            customer.bank_account_title = self.cleaned_data['bank_account_title']
            customer.opening_balance = self.cleaned_data['opening_balance']
            customer.terms = self.cleaned_data['terms']
            customer.notes = self.cleaned_data['notes']
            customer.payment_method = self.cleaned_data['payment_method']


            if self.cleaned_data['pdf_attachment_box']:
                customer.pdf_attachment_box = self.cleaned_data['pdf_attachment_box']

            if commit:
                customer.save()
            return customer


class updateEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [

            'employee_id',
            'employee_name',
            'employee_address',
            'city',
            'country',
            'postal_code',
            'currency',
            'pdf_attachment_box',
            'notes'


        ]

        def save(self, commit=True):
            employee = self.instance
            employee.employee_id = self.cleaned_data['employee_id']
            employee.employee_name = self.cleaned_data['employee_name']
            employee.employee_address = self.cleaned_data['employee_address']
            employee.city = self.cleaned_data['city']
            employee.country = self.cleaned_data['country']
            employee.postal_code = self.cleaned_data['postal_code']
            employee.currency = self.cleaned_data['currency']
            employee.notes = self.cleaned_data['notes']

            if self.cleaned_data['pdf_attachment_box']:
                employee.pdf_attachment_box = self.cleaned_data['pdf_attachment_box']

            if commit:
                employee.save()
            return employee


class updateBankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = [

            'bank_account_id',
            'bank_account_title',
            'bank_account_name',
            'bank_account_address',
            'opening_balance',
            'city',
            'country',
            'postal_code',
            'currency',
            'pdf_attachment_box',
            'notes'
        ]

        def save(self, commit=True):
            bankaccount = self.instance
            bankaccount.bank_account_id = self.cleaned_data['bank_account_id']
            bankaccount.bank_account_title = self.cleaned_data['bank_account_title']
            bankaccount.bank_account_name = self.cleaned_data['bank_account_name']
            bankaccount.bank_account_address = self.cleaned_data['bank_account_address']
            bankaccount.opening_balance = self.cleaned_data['opening_balance']
            bankaccount.city = self.cleaned_data['city']
            bankaccount.country = self.cleaned_data['country']
            bankaccount.postal_code = self.cleaned_data['postal_code']
            bankaccount.currency = self.cleaned_data['currency']
            bankaccount.notes = self.cleaned_data['notes']

            if self.cleaned_data['pdf_attachment_box']:
                bankaccount.pdf_attachment_box = self.cleaned_data['pdf_attachment_box']

            if commit:
                bankaccount.save()
            return bankaccount


class updatePaymentMadeForm(forms.ModelForm):
    class Meta:
        model = PaymentMade
        fields = [
            'purchase_order_receipt_no',
            'payment_date',
            'amount',
            'currency',
            'bankaccount',
            'pdf_attachment_box',
            'notes',
            'payment_remaining',
            'exchange_rate',
        ]

        def save(self, commit=True):
            paymentmade = self.instance
            paymentmade.purchase_order_receipt_no = self.cleaned_data['purchase_order_receipt_no']
            paymentmade.payment_date = self.cleaned_data['payment_made']
            paymentmade.amount = self.cleaned_data['amount']
            paymentmade.currency = self.cleaned_data['currency']
            paymentmade.bankaccount = self.cleaned_data['bankaccount']
            paymentmade.notes = self.cleaned_data['notes']
            paymentmade.payment_remaining = self.cleaned_data['payment_remaining']
            paymentmade.exchange_rate = self.cleaned_data['exchange_rate']



            if self.cleaned_data['pdf_attachment_box']:
                paymentmade.pdf_attachment_box = self.cleaned_data['pdf_attachment_box']

            if commit:
                paymentmade.save()
            return paymentmade


class editPaymentReceivedForm(forms.ModelForm):
    class Meta:
        model = PaymentReceived
        fields = [

            'order_invoice_no',
            'payment_date',
            'amount',
            'currency',
            'bankaccount',
            'payment_method',
            'payment_remaining',
            'exchange_rate',
            'pdf_attachment_box',
            'notes',
            'banking_charges',
            'amount_received'

        ]

        def save(self, commit=True):
            paymentreceived = self.instance

            paymentreceived.order_invoice_no = self.cleaned_data['order_invoice_no']
            paymentreceived.payment_date = self.cleaned_data['payment_made']
            paymentreceived.amount = self.cleaned_data['amount']
            paymentreceived.currency = self.cleaned_data['currency']
            paymentreceived.bankaccount = self.cleaned_data['bankaccount']
            paymentreceived.payment_method = self.cleaned_data['payment_method']
            paymentreceived.payment_remaining = self.cleaned_data['payment_remaining']
            paymentreceived.exchange_rate = self.cleaned_data['exchange_rate']
            paymentreceived.notes = self.cleaned_data['notes']
            paymentreceived.banking_charges = self.cleaned_data['banking_charges']
            paymentreceived.amount_received = self.cleaned_data['amount_received']


            if self.cleaned_data['pdf_attachment_box']:
                paymentreceived.pdf_attachment_box = self.cleaned_data['pdf_attachment_box']

            if commit:
                paymentreceived.save()
            return paymentreceived



class updateNewExpenseForm(forms.ModelForm):
    class Meta:
        model = NewExpense
        fields = [

            'expense_id',
            'expense_type',
            'expense_date',
            'material',
            'currency',
            'bankaccount',
            'amount',
            'payment_remaining',
            'pdf_attachment_box',
            'notes',

        ]

        def save(self, commit=True):
            expense = self.instance

            expense.expense_id = self.cleaned_data['expense_id']
            expense.expense_type = self.cleaned_data['expense_type']
            expense.expense_date = self.cleaned_data['expense_date']
            expense.material = self.cleaned_data['material']
            expense.currency = self.cleaned_data['currency']
            expense.bankaccount = self.cleaned_data['bankaccount']
            expense.amount = self.cleaned_data['amount']
            expense.payment_remaining = self.cleaned_data['payment_remainig']
            expense.notes = self.cleaned_data['notes']


            if self.cleaned_data['pdf_attachment_box']:
                expense.pdf_attachment_box = self.cleaned_data['pdf_attachment_box']

            if commit:
                expense.save()
            return expense


