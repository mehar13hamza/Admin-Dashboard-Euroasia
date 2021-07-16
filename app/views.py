from django.shortcuts import render, redirect, get_object_or_404
from django.http import StreamingHttpResponse
from django.shortcuts import render
import json
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.contrib.admin import AdminSite
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
import json
from .forms import *
from .models import *
from datetime import datetime
from django.http import HttpResponse
import csv
from datetime import datetime, timedelta, date
from django.db.models import Sum, F
from django.core import serializers

last_month = datetime.today() - timedelta(days=30)
last_year = datetime.today() - timedelta(days=365)

def handler404(request,exception):
    return render(request, '404.html', status=404)


def get_bank_values():
    queryset = []
    banks = BankAccount.objects.all()

    for b in banks:

        payments_received = PaymentReceived.objects.filter(bankaccount=b.id).aggregate(Sum('amount'))

        payments_received = payments_received['amount__sum'] if payments_received['amount__sum'] else 0

        payments_made = PaymentMade.objects.filter(bankaccount=b.id).aggregate(Sum('amount'))
        payments_made =  payments_made['amount__sum'] if payments_made['amount__sum'] else 0

        expenses = NewExpense.objects.filter(bankaccount=b.id).aggregate(Sum('amount'))

        expenses = expenses['amount__sum'] if expenses['amount__sum'] else 0
        net_balance = payments_received - (expenses+payments_made)

        queryset.append({'id':b.id, 'bank_account_id':b.bank_account_id, 'bank_account_name':b.bank_account_name, 'net_balance':net_balance})
    return queryset

def get_profit_in_pkr():
    monthly_earnings_usd = SaleOrder.objects.filter(order_date__gte=last_month, currency=1).aggregate(amou__sum=Sum('gross_profit'))
    yearly_earnings_usd = SaleOrder.objects.filter(order_date__gte=last_year, currency=1).aggregate(amou__sum=Sum('gross_profit'))
    exchange_rate_usd = ExchangeRates.objects.filter(base_currency="USD", secondary_currency="PKR")[0].exchange_rate
    monthly_earnings_usd = monthly_earnings_usd['amou__sum']*exchange_rate_usd if monthly_earnings_usd['amou__sum'] else 0
    yearly_earnings_usd = yearly_earnings_usd['amou__sum']*exchange_rate_usd if yearly_earnings_usd['amou__sum'] else 0


    monthly_earnings_pkr = SaleOrder.objects.filter(order_date__gte=last_month, currency=2).aggregate(amou__sum=Sum('gross_profit'))
    yearly_earnings_pkr = SaleOrder.objects.filter(order_date__gte=last_year, currency=2).aggregate(amou__sum=Sum('gross_profit'))
    exchange_rate_pkr = 1
    monthly_earnings_pkr = monthly_earnings_pkr['amou__sum']*exchange_rate_pkr if monthly_earnings_pkr['amou__sum'] else 0
    yearly_earnings_pkr = yearly_earnings_pkr['amou__sum']*exchange_rate_pkr if yearly_earnings_pkr['amou__sum'] else 0

    monthly_earnings_eur = SaleOrder.objects.filter(order_date__gte=last_month, currency=3).aggregate(amou__sum=Sum('gross_profit'))
    yearly_earnings_eur = SaleOrder.objects.filter(order_date__gte=last_year, currency=3).aggregate(amou__sum=Sum('gross_profit'))
    exchange_rate_eur = ExchangeRates.objects.filter(base_currency="EUR", secondary_currency="PKR")[0].exchange_rate
    monthly_earnings_eur = monthly_earnings_eur['amou__sum']*exchange_rate_eur if monthly_earnings_eur['amou__sum'] else 0
    yearly_earnings_eur = yearly_earnings_eur['amou__sum']*exchange_rate_eur if yearly_earnings_eur['amou__sum'] else 0

    monthly_earnings_gbp = SaleOrder.objects.filter(order_date__gte=last_month, currency=4).aggregate(amou__sum=Sum('gross_profit'))
    yearly_earnings_gbp = SaleOrder.objects.filter(order_date__gte=last_year, currency=4).aggregate(amou__sum=Sum('gross_profit'))
    exchange_rate_gbp = ExchangeRates.objects.filter(base_currency="GBP", secondary_currency="PKR")[0].exchange_rate
    monthly_earnings_gbp = monthly_earnings_gbp['amou__sum']*exchange_rate_gbp if monthly_earnings_gbp['amou__sum'] else 0
    yearly_earnings_gbp = yearly_earnings_gbp['amou__sum']*exchange_rate_gbp if yearly_earnings_gbp['amou__sum'] else 0

    monthly_earnings_cad = SaleOrder.objects.filter(order_date__gte=last_month, currency=5).aggregate(amou__sum=Sum('gross_profit'))
    yearly_earnings_cad = SaleOrder.objects.filter(order_date__gte=last_year, currency=5).aggregate(amou__sum=Sum('gross_profit'))
    exchange_rate_cad = ExchangeRates.objects.filter(base_currency="CAD", secondary_currency="PKR")[0].exchange_rate
    monthly_earnings_cad = monthly_earnings_cad['amou__sum']*exchange_rate_cad if monthly_earnings_cad['amou__sum'] else 0
    yearly_earnings_cad = yearly_earnings_cad['amou__sum']*exchange_rate_cad if yearly_earnings_cad['amou__sum'] else 0

    monthly_earnings = monthly_earnings_cad + monthly_earnings_eur + monthly_earnings_gbp + monthly_earnings_pkr + monthly_earnings_usd
    yearly_earnings = yearly_earnings_cad + yearly_earnings_eur + yearly_earnings_gbp + yearly_earnings_pkr +yearly_earnings_usd

    return monthly_earnings, yearly_earnings



def index(request):
    if 'logged_in' in request.session:
        monthly_earnings, yearly_earnings = get_profit_in_pkr()

        receivables = SaleOrder.objects.filter(payment_remaining__gt=0)
        payables = PurchaseOrder.objects.filter(payment_remaining__gt=0)
        expenses = ExpenseEntry.objects.filter(payment_remaining__gt=0)

        banks_net = get_bank_values()



        gross_profit_usd = SaleOrder.objects.filter(currency=1).aggregate(Sum('gross_profit'))
        gross_profit_pkr = SaleOrder.objects.filter(currency=2).aggregate(Sum('gross_profit'))
        gross_profit_eur = SaleOrder.objects.filter(currency=3).aggregate(Sum('gross_profit'))
        gross_profit_gbp = SaleOrder.objects.filter(currency=4).aggregate(Sum('gross_profit'))
        gross_profit_cad = SaleOrder.objects.filter(currency=5).aggregate(Sum('gross_profit'))

        gross_profits = {

            'gross_profit_usd': gross_profit_usd['gross_profit__sum'] if gross_profit_usd['gross_profit__sum'] else 0,
            'gross_profit_pkr': gross_profit_pkr['gross_profit__sum'] if gross_profit_pkr['gross_profit__sum'] else 0,
            'gross_profit_eur':gross_profit_eur['gross_profit__sum'] if gross_profit_eur['gross_profit__sum'] else 0,
            'gross_profit_gbp':gross_profit_gbp['gross_profit__sum'] if gross_profit_gbp['gross_profit__sum'] else 0,
            'gross_profit_cad':gross_profit_cad['gross_profit__sum'] if gross_profit_cad['gross_profit__sum'] else 0

        }


        gross_profits_per = {

            'usd_per' : (gross_profits['gross_profit_usd']/40000)*100,
            'pkr_per' : (gross_profits['gross_profit_pkr']/4000000)*100,
            'eur_per' : (gross_profits['gross_profit_eur']/40000)*100,
            'gbp_per' : (gross_profits['gross_profit_gbp']/40000)*100,
            'cad_per' : (gross_profits['gross_profit_cad']/40000)*100,


        }





        return render(request, 'index.html', {'monthly_earnings':monthly_earnings, 'yearly_earnings':yearly_earnings, 'receivables':receivables, 'payables':payables, 'expenses':expenses, 'gross_profits':gross_profits, 'gross_profits_per':gross_profits_per, 'banks_net':banks_net})
    else:
        return redirect('login')

def gross_profit_details(request):
    if 'logged_in' in request.session:
        sale_orders_usd = SaleOrder.objects.filter(currency=1)
        sale_orders_pkr = SaleOrder.objects.filter(currency=2)
        sale_orders_eur = SaleOrder.objects.filter(currency=3)
        sale_orders_gbp = SaleOrder.objects.filter(currency=4)
        sale_orders_cad = SaleOrder.objects.filter(currency=5)

        gross_profit_usd = sale_orders_usd.aggregate(Sum('gross_profit'))
        gross_profit_pkr = sale_orders_pkr.aggregate(Sum('gross_profit'))
        gross_profit_eur = sale_orders_eur.aggregate(Sum('gross_profit'))
        gross_profit_gbp = sale_orders_gbp.aggregate(Sum('gross_profit'))
        gross_profit_cad = sale_orders_cad.aggregate(Sum('gross_profit'))

        orders = {

            'sale_orders_usd': sale_orders_usd,
            'sale_orders_pkr': sale_orders_pkr,
            'sale_orders_eur': sale_orders_eur,
            'sale_orders_gbp': sale_orders_gbp,
            'sale_orders_cad': sale_orders_cad
        }

        gross_profits = {

            'gross_profit_usd': gross_profit_usd['gross_profit__sum'] if gross_profit_usd['gross_profit__sum'] else 0,
            'gross_profit_pkr': gross_profit_pkr['gross_profit__sum'] if gross_profit_pkr['gross_profit__sum'] else 0,
            'gross_profit_eur':gross_profit_eur['gross_profit__sum'] if gross_profit_eur['gross_profit__sum'] else 0,
            'gross_profit_gbp':gross_profit_gbp['gross_profit__sum'] if gross_profit_gbp['gross_profit__sum'] else 0,
            'gross_profit_cad':gross_profit_cad['gross_profit__sum'] if gross_profit_cad['gross_profit__sum'] else 0

        }
        return render(request, 'gross_profit_details.html', {'orders':orders, 'gross_profits':gross_profits})
    else:
        return redirect('login')

def login(request):
    request.session.flush()
    if request.method=="POST":
        instance = admin.objects.filter(username=request.POST['username']).exists()
        if instance:
            instance = admin.objects.filter(username=request.POST['username'])[0]
            if check_password(request.POST['password'], instance.password):
                request.session['logged_in'] = {'id' : instance.id}
                return redirect('index')

        return render(request, 'login.html', {'message': 'Incorrect username or password'})

    else:
        return render(request, 'login.html')

def add_seller(request):
    if 'logged_in' in request.session:
        currencies = Currency.objects.all()
        if request.method == "POST":

            form = sellerForm(request.POST, request.FILES)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return render(request, 'add_seller.html', {'message': 'message','currencies':currencies})
            else:
                return render(request, 'add_seller.html', {'errors': form.errors,'currencies':currencies})


        return render(request, 'add_seller.html',{'currencies':currencies})
    else:
        return redirect('login')

def view_seller(request):
    if 'logged_in' in request.session:
        #sellers = PurchaseOrder.objects.values('seller','seller__seller_id','seller__currency__abbreviation','seller__seller_company', 'seller__email', 'seller__seller_type').annotate(Sum('payment_remaining'))
        sellers = seller.objects.all()


        return render(request, 'view_seller.html',{'sellers':sellers})
    else:
        return redirect('login')

def individual_seller(request,id):
    if 'logged_in' in request.session:
        sellers = get_object_or_404(seller, id=id)
        net_payable = PurchaseOrder.objects.filter(seller_id=id).aggregate(Sum('payment_remaining'))
        net_payable = net_payable['payment_remaining__sum']
        print(net_payable)
        return render(request, 'individual_seller.html',{'seller':sellers, 'net_payable':net_payable})
    else:
        return redirect('login')

def edit_seller(request, id):
    if 'logged_in' in request.session:
        sellers = get_object_or_404(seller,id=id)
        currencies = Currency.objects.all()

        if request.method=="POST":
            form = updateSellerForm(request.POST, request.FILES, instance=sellers)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return redirect('view_seller')
            else:
                render(request, 'edit_seller.html',{'errors':form.errors,'seller':sellers, 'currencies':currencies})



        return render(request, 'edit_seller.html',{'seller':sellers, 'currencies':currencies})
    else:
        return redirect('login')


def delete_seller(request, id):
    if 'logged_in' in request.session:
        sellers = get_object_or_404(seller, id=id)
        sellers.delete()
        return redirect('view_seller')
    else:
        return redirect('login')


def add_customer(request):
    if 'logged_in' in request.session:
        currencies = Currency.objects.all()
        if request.method == "POST":
            form = customerForm(request.POST, request.FILES)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return render(request, 'add_customer.html', {'message': 'message', 'currencies':currencies})
            else:
                return render(request, 'add_customer.html', {'errors':form.errors, 'currencies':currencies})
        return render(request, 'add_customer.html',{'currencies':currencies})
    else:
        return redirect('login')

def view_customer(request):
    if 'logged_in' in request.session:
        customers  = SaleOrder.objects.values('customer','customer__customer_id','customer__customer_name','customer__customer_phone', 'customer__customer_type', 'customer__currency__abbreviation').annotate(sum_payment_remaining=Sum(F('payment_remaining')/F('exchange_rate')))
        customers = Customer.objects.all()
        return render(request, 'view_customer.html',{'customers':customers})
    else:
        return redirect('login')

def individual_customer(request,id):
    if 'logged_in' in request.session:
        customer = get_object_or_404(Customer, id=id)
        net_balance_receivable = SaleOrder.objects.filter(customer_id=id).annotate(div=F('payment_remaining')/F('exchange_rate')).aggregate(Sum('div'))
        net_balance_receivable = net_balance_receivable['div__sum']
        return render(request, 'individual_customer.html',{'customer':customer, 'net_balance_receivable':net_balance_receivable})
    else:
        return redirect('login')

def edit_customer(request, id):
    if 'logged_in' in request.session:
        customer = get_object_or_404(Customer,id=id)
        currencies = Currency.objects.all()

        if request.method=="POST":
            form = updateCustomerForm(request.POST, request.FILES, instance=customer)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return redirect('view_customer')
            else:
                return render(request, 'edit_customer.html',{'errors':form.errors, 'customer':customer, 'currencies':currencies})



        return render(request, 'edit_customer.html',{'customer':customer, 'currencies':currencies})
    else:
        return redirect('login')


def delete_customer(request, id):
    if 'logged_in' in request.session:
        customers = get_object_or_404(Customer, id=id)
        customers.delete()
        return redirect('view_customer')
    else:
        return redirect('login')


def add_transport(request):
    if 'logged_in' in request.session:
        currencies = Currency.objects.all()
        if request.method=="POST":

            form = transportForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return render(request, 'add_transport.html', {'message':'message','currencies':currencies})
            else:
                return render(request, 'add_transport.html',{'errors':form.errors, 'currencies':currencies})


        return render(request, 'add_transport.html',{'currencies':currencies})
    else:
        return redirect('login')


def view_transport(request):
    if 'logged_in' in request.session:
        transport_companies = Transport.objects.all()
        return render(request, 'view_transport.html',{'transport_companies':transport_companies})
    else:
        return redirect('login')


def individual_transport(request, id):
    if 'logged_in' in request.session:
        transport_company = get_object_or_404(Transport, id=id)
        net_balance_payable = PurchaseOrder.objects.filter(freight_company=id, payment_remaining__gt=0).aggregate(Sum('freight_cost'))
        net_balance_payable = net_balance_payable['freight_cost__sum']
        print(net_balance_payable)
        return render(request, 'individual_transport.html',{'transport_company':transport_company, 'net_balance_payable':net_balance_payable})
    else:
        return redirect('login')




def edit_transport(request, id):
    if 'logged_in' in request.session:
        transport_company = get_object_or_404(Transport,id=id)
        currencies = Currency.objects.all()

        if request.method=="POST":
            form = updateTransportForm(request.POST, request.FILES, instance=transport_company)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return redirect('view_transport')
            else:
                return render(request, 'edit_transport.html',{'errors':form.errors,'transport_company':transport_company, 'currencies':currencies})



        return render(request, 'edit_transport.html',{'transport_company':transport_company, 'currencies':currencies})
    else:
        return redirect('login')


def delete_transport(request,id):
    if 'logged_in' in request.session:
        instance = get_object_or_404(Transport,id=id)
        instance.delete()
        return redirect('view_transport')
    else:
        return redirect('login')


def individual_employee(request, id):
    if 'logged_in' in request.session:
        employee = get_object_or_404(Employee, id=id)
        return render(request, 'individual_employee.html',{'employee':employee})
    else:
        return redirect('login')


def edit_employee(request, id):
    if 'logged_in' in request.session:
        employee = get_object_or_404(Employee, id=id)
        currencies = Currency.objects.all()
        if request.method == "POST":
            form = updateEmployeeForm(request.POST, request.FILES, instance=employee)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return redirect('view_employees')
            else:
                return render(request, 'edit_employee.html',{'errors':form.errors, 'employee':employee, 'currencies':currencies})


        return render(request, 'edit_employee.html',{'employee':employee, 'currencies':currencies})
    else:
        return redirect('login')


def delete_employee(request, id):
    if 'logged_in' in request.session:
        employee = get_object_or_404(Employee, id=id)
        employee.delete()
        return redirect('view_employees')
    else:
        return redirect('login')

def view_employees(request):
    if 'logged_in' in request.session:
        employees = Employee.objects.all()

        return render(request, 'view_employees.html',{'employees':employees})
    else:
        return redirect('login')

def add_employee(request):
    if 'logged_in' in request.session:
        currencies = Currency.objects.all()
        if request.method == "POST":
            form = EmployeeForm(request.POST, request.FILES)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return render(request, 'add_employee.html',{'message':'message', 'currencies':currencies})

            else:
                return render(request, 'add_employee.html',{'errors':form.errors, 'currencies':currencies})

        return render(request, 'add_employee.html',{'currencies':currencies})
    else:
        return redirect('login')


def add_bank(request):
    if 'logged_in' in request.session:
        currencies = Currency.objects.all()

        if request.method == "POST":
            form = BankAccountForm(request.POST, request.FILES)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return render(request, 'add_bank.html',{'currencies':currencies,'message':'message'})
            else:
                return render(request, 'add_bank.html',{'errors':form.errors, 'currencies':currencies})


        return render(request, 'add_bank.html',{'currencies':currencies})
    else:
        return redirect('login')


def view_bank(request):
    if 'logged_in' in request.session:
        bankaccounts = BankAccount.objects.all()

        return render(request, 'view_bank.html',{'bankaccounts':bankaccounts})
    else:
        return redirect('login')


def individual_bank(request, id):
    if 'logged_in' in request.session:
        bankaccount = get_object_or_404(BankAccount,id=id)
        payments_received = PaymentReceived.objects.filter(bankaccount=bankaccount).annotate(amou=F('amount')*F('exchange_rate')).aggregate(Sum('amou'))
        payments_made = PaymentMade.objects.filter(bankaccount=bankaccount).aggregate(Sum('amount'))
        expense_made = NewExpense.objects.filter(bankaccount=bankaccount).aggregate(Sum('amount'))

        payments_received = payments_received['amou__sum'] if payments_received['amou__sum'] else 0
        payments_made = payments_made['amount__sum'] if payments_made['amount__sum'] else 0
        expense_made = expense_made['amount__sum'] if expense_made['amount__sum'] else 0

        net_balance = payments_received - (payments_made+expense_made)
        return render(request, 'individual_bank.html',{'bankaccount':bankaccount, 'net_balance':net_balance})
    else:
        return redirect('login')

def bank_transactions(request, id):
    if 'logged_in' in request.session:
        bankaccount = get_object_or_404(BankAccount,id=id)
        payments_received = PaymentReceived.objects.filter(bankaccount=bankaccount).annotate(amou=F('amount')*F('exchange_rate')).aggregate(Sum('amou'))
        payments_made = PaymentMade.objects.filter(bankaccount=bankaccount).aggregate(Sum('amount'))
        expense_made = NewExpense.objects.filter(bankaccount=bankaccount).aggregate(Sum('amount'))

        payments_received = payments_received['amou__sum'] if payments_received['amou__sum'] else 0
        payments_made = payments_made['amount__sum'] if payments_made['amount__sum'] else 0
        expense_made = expense_made['amount__sum'] if expense_made['amount__sum'] else 0

        net_balance = payments_received - (payments_made+expense_made)


        payments_received = PaymentReceived.objects.filter(bankaccount=bankaccount).order_by('-id')
        payments_made = PaymentMade.objects.filter(bankaccount=bankaccount).order_by('-id')
        expenses_made = NewExpense.objects.filter(bankaccount=bankaccount).order_by('-id')


        return render(request, 'bank_transactions.html',{'bankaccount':bankaccount, 'net_balance':net_balance, 'payments_received':payments_received, 'payments_made':payments_made, 'new_expenses':expenses_made})
    else:
        return redirect('login')

def edit_bank(request, id):
    if 'logged_in' in request.session:
        bankaccount = get_object_or_404(BankAccount,id=id)
        currencies = Currency.objects.all()

        if request.method == "POST":
            form = updateBankAccountForm(request.POST, request.FILES, instance=bankaccount)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return redirect('view_bank')
            else:
                return render(request, 'edit_bank.html',{'errors':form.errors, 'bankaccount':bankaccount, 'currencies':currencies})

        return render(request, 'edit_bank.html',{'bankaccount':bankaccount, 'currencies':currencies})
    else:
        return redirect('login')



def delete_bank(request, id):
    if 'logged_in' in request.session:
        instance = get_object_or_404(BankAccount, id=id)
        instance.delete()
        return redirect('view_bank')
    else:
        return redirect('login')


def payment_received_entry(request):
    if 'logged_in' in request.session:
        sale_orders = SaleOrder.objects.all()
        currencies = Currency.objects.all()
        bankaccounts = BankAccount.objects.all()
        if request.method == 'POST':
            recent_payment = PaymentReceived.objects.filter(order_invoice_no=request.POST['order_invoice_no']).order_by('-id')[0]
            payment_remaining = round(recent_payment.payment_remaining - (float(request.POST['amount'])*float(request.POST['exchange_rate'])), 2)
            entry = {}
            for keys in request.POST:
                entry[keys] = request.POST[keys]
            entry['payment_remaining'] = payment_remaining
            instance = SaleOrder.objects.get(id=request.POST['order_invoice_no'])
            instance.payment_remaining = payment_remaining
            instance.save()

            form = paymentReceivedForm(entry, request.FILES)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return render(request, 'payment_received_entry.html',{'sale_orders':sale_orders,'currencies':currencies,'bankaccounts':bankaccounts, 'message':'message'})
            else:
                print(form.errors)

        return render(request, 'payment_received_entry.html',{'sale_orders':sale_orders,'currencies':currencies,'bankaccounts':bankaccounts})

    else:
        return redirect('login')


def sale_order(request):
    if 'logged_in' in request.session:
        customers = Customer.objects.all()
        purchase_orders = PurchaseOrder.objects.all()
        currencies = Currency.objects.all()
        bankaccounts = BankAccount.objects.all()

        if request.method == "POST":

            order = {}
            for keys in request.POST:
                order[keys] = request.POST[keys]
            total = round((float(order['selling_quantity'])*float(order['selling_price']) - float(order['admin_cost'])), 2)
            order['total'] = total
            form = saleOrderForm(order, request.FILES)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                payment_remaining = total - (float(order['advance'])*float(order['exchange_rate']))
                instance = SaleOrder.objects.all().order_by('-id')[0]
                entry = {'order_invoice_no':instance.id, 'payment_date':order['order_date'], 'amount':order['advance'], 'currency':order['customer_account_currency'], 'bankaccount':order['bank_account_payment'], 'payment_method':order['payment_method'],'payment_remaining':payment_remaining, 'banking_charges': order['banking_charges'],'amount_received': order['amount_received'], 'exchange_rate':order['exchange_rate'],'notes':'none'}
                form = paymentReceivedForm(entry, request.FILES)

                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.save()

                    return render(request, 'sale_order.html',{'customers':customers,'purchase_orders':purchase_orders, 'currencies':currencies, 'bankaccounts':bankaccounts, 'message':'message'})
                else:
                    return render(request, 'sale_order.html',{'errors':form.errors,'customers':customers,'purchase_orders':purchase_orders, 'currencies':currencies, 'bankaccounts':bankaccounts})

            else:
                return render(request, 'sale_order.html',{'errors':form.errors, 'customers':customers,'purchase_orders':purchase_orders, 'currencies':currencies, 'bankaccounts':bankaccounts})

        return render(request, 'sale_order.html',{'customers':customers,'purchase_orders':purchase_orders, 'currencies':currencies, 'bankaccounts':bankaccounts})
    else:
        return redirect('login')

def paymentMadeFill(posts, Files):

    form = paymentMadeForm({'purchase_order_receipt_no': posts.id, 'payment_date':posts.order_date, 'amount':posts.advance, 'currency' : posts.advance_currency, 'bankaccount':posts.bank_account_payment, 'notes': posts.notes,'payment_remaining':posts.payment_remaining, 'exchange_rate':posts.exchange_rate},Files )

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return True
    else:
        print(form.errors)
        return False


def add_exchange_rate(base_currency, secondary_currency, record_date, exchange_rate):
    last_entry = ExchangeRates.objects.all().order_by('-id')
    last_entry = last_entry[0] if last_entry else None
    if last_entry == None:
            currencies = ['USD', 'PKR', 'EUR', 'CAD', 'GBP']
            form = exchangeRatesForm({'record_date':record_date, 'base_currency':base_currency, 'secondary_currency': secondary_currency, 'exchange_rate':exchange_rate})
            if form.is_valid():
                instance = form.save(commit=True)

            for currency in currencies:
                if currency == secondary_currency:
                    continue
                else:
                    curr = base_currency+"_"+currency
                    response = requests.get("https://free.currconv.com/api/v7/convert?q="+curr+"&compact=ultra&apiKey=f16c12803234e5c11e25")
                    response = response.json()
                    print(response)
                    form = exchangeRatesForm({'record_date':record_date, 'base_currency':base_currency, 'secondary_currency': currency, 'exchange_rate':response[curr]})
                    if form.is_valid():
                        instance = form.save(commit=True)

            for currency in currencies:
                curr = currency+"_"+base_currency
                response = requests.get("https://free.currconv.com/api/v7/convert?q="+curr+"&compact=ultra&apiKey=f16c12803234e5c11e25")
                response = response.json()
                print(response)
                form = exchangeRatesForm({'record_date':record_date, 'base_currency':currency, 'secondary_currency': base_currency, 'exchange_rate':response[curr]})
                if form.is_valid():
                    instance = form.save(commit=True)
    else:
        if last_entry.record_date != datetime.today().strftime('%Y-%m-%d'):
            currencies = ['USD', 'PKR', 'EUR', 'CAD', 'GBP']
            form = exchangeRatesForm({'record_date':record_date, 'base_currency':base_currency, 'secondary_currency': secondary_currency, 'exchange_rate':exchange_rate})
            if form.is_valid():
                instance = form.save(commit=True)

            for currency in currencies:
                if currency == secondary_currency:
                    continue
                else:
                    curr = base_currency+"_"+currency
                    response = requests.get("https://free.currconv.com/api/v7/convert?q="+curr+"&compact=ultra&apiKey=f16c12803234e5c11e25")
                    response = response.json()
                    print(response)
                    form = exchangeRatesForm({'record_date':record_date, 'base_currency':base_currency, 'secondary_currency': currency, 'exchange_rate':response[curr]})
                    if form.is_valid():
                        instance = form.save(commit=True)

            for currency in currencies:
                curr = currency+"_"+base_currency
                response = requests.get("https://free.currconv.com/api/v7/convert?q="+curr+"&compact=ultra&apiKey=f16c12803234e5c11e25")
                print(response)
                form = exchangeRatesForm({'record_date':record_date, 'base_currency':currency, 'secondary_currency': base_currency, 'exchange_rate':response[curr]})
                if form.is_valid():
                    instance = form.save(commit=True)


def purchase_order(request):
    if 'logged_in' in request.session:
        sellers = seller.objects.all()
        transport_companies = Transport.objects.all()
        currencies = Currency.objects.all()
        bankaccounts = BankAccount.objects.all()

        if request.method == "POST":

            order = {}
            for keys in request.POST:
                order[keys] = request.POST[keys]
            order['seller_account_currency'] = seller.objects.get(id=request.POST['seller']).currency.id
            form = purchaseOrderForm(order, request.FILES)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                last_post = PurchaseOrder.objects.all().order_by('-id')[0]

                #add_exchange_rate(last_post.advance_currency.abbreviation, last_post.seller_currency.abbreviation, last_post.order_date, last_post.exchange_rate)

                if paymentMadeFill(last_post, request.FILES):
                    return render(request, 'purchase_order.html',{'sellers':sellers, 'transport_companies':transport_companies,'message':'message', 'currencies':currencies, 'bankaccounts':bankaccounts})
                else:
                    return render(request, 'purchase_order.html',{'errors':"Invalid Entry",'sellers':sellers, 'transport_companies':transport_companies, 'currencies':currencies, 'bankaccounts':bankaccounts})


            else:
                return render(request, 'purchase_order.html',{'errors':form.errors,'sellers':sellers, 'transport_companies':transport_companies, 'currencies':currencies, 'bankaccounts':bankaccounts})


        return render(request, 'purchase_order.html',{'sellers':sellers, 'transport_companies':transport_companies, 'currencies':currencies, 'bankaccounts':bankaccounts})
    else:
        return redirect('login')


def get_purchase_order(request):
    id = request.GET.get("id", None)

    data = {

        'exists' : PurchaseOrder.objects.filter(id=id).exists(),
        'purchase_quantity': PurchaseOrder.objects.get(id=id).purchase_quantity,
        'purchase_price': PurchaseOrder.objects.get(id=id).purchase_price,
    }

    return JsonResponse(data)

def all_sale_orders(request):
    if 'logged_in' in request.session:
        sale_orders = SaleOrder.objects.all().order_by('-id')
        return render(request, 'all_sale_orders.html',{'sale_orders':sale_orders})
    else:
        return redirect('login')

def all_purchase_orders(request):
    if 'logged_in' in request.session:
        purchase_orders = PurchaseOrder.objects.all().order_by('-id')
        return render(request, 'all_purchase_orders.html',{'purchase_orders':purchase_orders})
    else:
        return redirect('login')

def all_expenses(request):
    if 'logged_in' in request.session:
        expenses =  ExpenseEntry.objects.all().order_by('-id')
        return render(request, 'all_expenses.html',{'expenses':expenses})
    else:
        return redirect('login')


def payment_made_ledger(request):
    if 'logged_in' in request.session:
        payments_made = PaymentMade.objects.all()

        return render(request, 'payment_made_ledger.html', {'payments_made':payments_made})
    else:
        return redirect('login')

def delete_payment_received(request, id):
    if 'logged_in' in request.session:
        instance = PaymentReceived.objects.get(id=id)
        instance.delete()
        return redirect('payment_received_ledger')
    else:
        return redirect('login')

def delete_payment_made(request, id):
    if 'logged_in' in request.session:
        instance = PaymentMade.objects.get(id=id)
        instance.delete()
        return redirect('payment_made_ledger')
    else:
        return redirect('login')


def edit_payment_made_ledger(request, id):
    if 'logged_in' in request.session:
        payment_made = PaymentMade.objects.get(id=id)
        expenses = ExpenseEntry.objects.all()
        purchase_orders = PurchaseOrder.objects.all()
        currencies = Currency.objects.all()
        bankaccounts = BankAccount.objects.all()

        if request.method == "POST":
            recent_payment = PaymentMade.objects.filter(purchase_order_receipt_no=request.POST['purchase_order_receipt_no']).order_by('-id')[0]
            payment_remaining = round(recent_payment.payment_remaining - (float(request.POST['amount'])*float(request.POST['exchange_rate'])), 2)
            entry = {}
            for keys in request.POST:
                entry[keys] = request.POST[keys]
            entry['payment_remaining'] = payment_remaining

            form = updatePaymentMadeForm(entry, request.FILES, instance=payment_made)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return redirect('payment_made_ledger')
            else:
                return render(request, 'edit_payment_made_ledger.html', {'errors':form.errors,'payment_made':payment_made, 'currencies':currencies,'bankaccounts':bankaccounts, 'expenses':expenses, 'purchase_orders':purchase_orders})


        return render(request, 'edit_payment_made_ledger.html', {'payment_made':payment_made,'currencies':currencies,'bankaccounts':bankaccounts, 'expenses':expenses, 'purchase_orders':purchase_orders})
    else:
        return redirect('login')


def print_bank_invoice(request, id):
    if 'logged_in' in request.session:
        bank = BankAccount.objects.get(id=id)
        payments_made = PaymentMade.objects.filter(bankaccount=id)
        payments_received = PaymentReceived.objects.filter(bankaccount=id)
        expenses = ExpenseEntry.objects.filter(bankaccount=id)

        details = []
        total = 0

        for p in payments_received:
            date = p.payment_date
            description = p.order_invoice_no.order_invoice_no
            credit = p.amount
            currency = bank.currency.abbreviation
            total = total+p.amount
            details.append({'date':date, 'description':description, 'credit':credit, 'debit':'', 'currency':currency, 'total':total})

        for p in payments_made:
            date = p.payment_date
            description = p.purchase_order_receipt_no.order_receipt_no
            debit = p.amount
            currency = bank.currency.abbreviation
            total = total-p.amount
            details.append({'date':date, 'description':description, 'credit':'', 'debit':debit, 'currency':currency, 'total':total})


        for p in expenses:
            date = p.payment_date
            description = p.expense.expense_id
            debit = p.amount
            currency = bank.currency.abbreviation
            total = total-p.amount
            details.append({'date':date, 'description':description, 'credit':'', 'debit':debit, 'currency':currency, 'total':total})

        details.sort(key = lambda x:x['date'])

        return render(request, 'print_bank_invoice.html', {'bank':bank,'details':details, 'total':total})
    else:
        return redirect('login')


def print_purchase_order(request, id):
    if 'logged_in' in request.session:
        purchase_order = PurchaseOrder.objects.get(id=id)
        return render(request, 'print_purchase_order.html', {'purchase_order':purchase_order})
    else:
        return redirect('login')

def print_sale_order(request, id):
    if 'logged_in' in request.session:
        sale_order = SaleOrder.objects.get(id=id)
        return render(request, 'print_sale_order.html', {'sale_order':sale_order})
    else:
        return redirect('login')


def customer_sale_orders(request, id):
    if 'logged_in' in request.session:
        sale_orders = SaleOrder.objects.filter(customer=id).order_by('-id')
        customer = Customer.objects.get(id=id)
        return render(request, 'all_sale_orders.html',{'sale_orders':sale_orders, 'customer':customer})
    else:
        return redirect('login')

def seller_purchase_orders(request, id):
    if 'logged_in' in request.session:
        purchase_orders = PurchaseOrder.objects.filter(seller=id).order_by('-id')
        Seller = seller.objects.get(id=id)
        return render(request, 'all_purchase_orders.html',{'purchase_orders':purchase_orders, 'seller':Seller})
    else:
        return redirect('login')

def transport_purchase_orders(request, id):
    if 'logged_in' in request.session:
        purchase_orders = PurchaseOrder.objects.filter(freight_company=id).order_by('-id')
        transport_company = Transport.objects.get(id=id)
        return render(request, 'all_purchase_orders.html', {'purchase_orders':purchase_orders, 'transport_company':transport_company})
    else:
        return redirect('login')


def edit_payment_received_ledger(request, id):
    if 'logged_in' in request.session:
        payment_received = PaymentReceived.objects.get(id=id)
        sale_orders = SaleOrder.objects.all()
        currencies = Currency.objects.all()
        bankaccounts = BankAccount.objects.all()
        if request.method == 'POST':
            recent_payment = PaymentReceived.objects.filter(order_invoice_no=request.POST['order_invoice_no']).order_by('-id')[0]
            payment_remaining = round(recent_payment.payment_remaining - (float(request.POST['amount'])*float(request.POST['exchange_rate'])), 2)
            entry = {}
            for keys in request.POST:
                entry[keys] = request.POST[keys]
            entry['payment_remaining'] = payment_remaining


            form = editPaymentReceivedForm(entry, request.FILES, instance=payment_received)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return redirect('payment_received_ledger')
            else:
                return render(request, 'edit_payment_received_ledger.html',{'errors':form.errors, 'sale_orders':sale_orders,'currencies':currencies,'bankaccounts':bankaccounts, 'payment_received':payment_received})


        return render(request, 'edit_payment_received_ledger.html',{'sale_orders':sale_orders,'currencies':currencies,'bankaccounts':bankaccounts, 'payment_received':payment_received})
    else:
        return redirect('login')

def export_to_csv(request, id):
    if 'logged_in' in request.session:

        if id == '1':

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="payments_made_ledger.csv"'

            writer = csv.writer(response)
            writer.writerow(['Sr.', 'Purchase Order Sr.', 'Payment Date', 'Amount', 'Currency', 'Bank Account', 'Payment remaining',  'Exchange Rate' 'PDF Attachment Box', 'Notes'])

            payments_made = PaymentMade.objects.all().values_list('id', 'purchase_order_receipt_no__order_receipt_no', 'payment_date', 'amount',  'currency__abbreviation', 'bankaccount__bank_account_name' , 'payment_remaining', 'exchange_rate', 'pdf_attachment_box', 'notes')
            for payment_made in payments_made:
                writer.writerow(payment_made)
        elif id== '2':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="payments_received_ledger.csv"'

            writer = csv.writer(response)
            writer.writerow(['Sr.', 'Sale Order Sr.', 'Payment Date', 'Amount', 'Currency', 'Bank Account', 'Payment Method', 'Payment Remaining', 'Exchange Rate', 'PDF Attachment Box', 'Notes'])

            payments_received = PaymentReceived.objects.all().values_list('id', 'order_invoice_no__order_invoice_no', 'payment_date', 'amount', 'currency__abbreviation', 'bankaccount__bank_account_name', 'payment_method', 'payment_remaining', 'exchange_rate', 'pdf_attachment_box', 'notes')
            for payment_received in payments_received:
                writer.writerow(payment_received)

        elif id== '3':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="expenses_made_ledger.csv"'

            writer = csv.writer(response)
            writer.writerow(['Sr.', 'Expense ID', 'Expense Date', 'Amount', 'Expense Type', 'Currency', 'Bank Account', 'Payment Remaining', 'PDF Attachment Box', 'Notes'])

            expenses_made = NewExpense.objects.all().values_list('id', 'expense_id__expense_id', 'expense_date', 'amount', 'expense_type', 'currency__abbreviation', 'bankaccount__bank_account_name', 'payment_remaining', 'pdf_attachment_box', 'notes')
            for expense_made in expenses_made:
                writer.writerow(expense_made)


        return response
    else:
        return redirect('login')


def payment_received_ledger(request):
    if 'logged_in' in request.session:
        payments_received = PaymentReceived.objects.all()

        return render(request, 'payment_received_ledger.html', {'payments_received':payments_received})
    else:
        return redirect('login')

def order_view(request, id):
    if 'logged_in' in request.session:
        sale_order = SaleOrder.objects.get(id=id)
        payments_received = PaymentReceived.objects.filter(order_invoice_no=id)

        final = {'total':0, 'fx_gains_losses':0, 'exchange_rate':0,'amount':0,'balance':0}
        for p in payments_received:
            final['total'] += p.amount
            final['fx_gains_losses'] += (sale_order.exchange_rate - p.exchange_rate)
            final['exchange_rate'] = p.exchange_rate
            final['balance'] = p.payment_remaining

        final['amount'] = final['total'] * final['exchange_rate']
        final['purchase_order_total'] =(sale_order.purchase_order.total)

        return render(request, 'order_view.html',{'sale_order':sale_order, 'payments_received':payments_received, 'final':final})
    else:
        return redirect('login')

def purchase_order_view(request, id):
    if 'logged_in' in request.session:
        purchase_order = PurchaseOrder.objects.get(id=id)
        payments_made = PaymentMade.objects.filter(purchase_order_receipt_no=id)
        final = {'total':0, 'fx_gains_losses':0, 'exchange_rate':0,'amount':0,'balance':0}

        for p in payments_made:
            final['total'] += p.amount
            final['fx_gains_losses'] += (p.exchange_rate - purchase_order.exchange_rate)
            final['exchange_rate'] = p.exchange_rate
            final['balance'] = p.payment_remaining


        final['amount'] = final['total'] * final['exchange_rate']

        return render(request, 'purchase_order_view.html', {'purchase_order':purchase_order, 'payments_made':payments_made, 'final':final})
    else:
        return redirect('login')

def payment_made_entry(request):
    if 'logged_in' in request.session:
        purchase_orders = PurchaseOrder.objects.all()
        currencies = Currency.objects.all()
        bankaccounts = BankAccount.objects.all()

        if request.method == "POST":
            recent_payment = PaymentMade.objects.filter(purchase_order_receipt_no=request.POST['purchase_order_receipt_no']).order_by('-id')[0]
            payment_remaining = round(recent_payment.payment_remaining - (float(request.POST['amount'])*float(request.POST['exchange_rate'])), 2)
            entry = {}
            for keys in request.POST:
                entry[keys] = request.POST[keys]
            entry['payment_remaining'] = payment_remaining
            instance = PurchaseOrder.objects.get(id=request.POST['purchase_order_receipt_no'])
            instance.payment_remaining = payment_remaining
            instance.save()

            form = paymentMadeForm(entry, request.FILES)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return render(request, 'payment_made_entry.html', {'purchase_orders':purchase_orders, 'currencies':currencies, 'bankaccounts':bankaccounts, 'message':'message'})
            else:
                return render(request, 'payment_made_entry.html', {'errors':form.errors, 'purchase_orders':purchase_orders, 'currencies':currencies, 'bankaccounts':bankaccounts})

        return render(request, 'payment_made_entry.html', {'purchase_orders':purchase_orders, 'currencies':currencies, 'bankaccounts':bankaccounts})
    else:
        return redirect('login')

def new_expense(request):
    if 'logged_in' in request.session:
        expenses = ExpenseEntry.objects.all()
        currencies = Currency.objects.all()
        bankaccounts = BankAccount.objects.all()

        if request.method == "POST":
            recent_expense = NewExpense.objects.filter(expense_id=request.POST['expense_id']).order_by('-id')[0]
            payment_remaining = round(recent_expense.payment_remaining - (float(request.POST['amount'])), 2)
            entry = {}
            for keys in request.POST:
                entry[keys] = request.POST[keys]
            entry['payment_remaining'] = payment_remaining
            instance = ExpenseEntry.objects.get(id=request.POST['expense_id'])
            instance.payment_remaining = payment_remaining
            instance.save()

            form = newExpenseForm(entry, request.FILES)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return render(request, 'new_expense.html', {'expenses':expenses, 'currencies':currencies, 'bankaccounts':bankaccounts, 'message':'message'})
            else:
                return render(request, 'new_expense.html', {'errors':form.errors,'expenses':expenses, 'currencies':currencies, 'bankaccounts':bankaccounts})

        return render(request, 'new_expense.html', {'expenses':expenses, 'currencies':currencies, 'bankaccounts':bankaccounts})
    else:
        return redirect('login')

def edit_expense_made_ledger(request, id):
    if 'logged_in' in request.session:
        expenses = ExpenseEntry.objects.all()
        currencies = Currency.objects.all()
        bankaccounts = BankAccount.objects.all()
        expense = NewExpense.objects.get(id=id)


        if request.method == "POST":
            recent_expense = NewExpense.objects.filter(expense_id=request.POST['expense_id']).order_by('-id')[0]
            payment_remaining = round(recent_expense.payment_remaining - (float(request.POST['amount'])), 2)
            entry = {}
            for keys in request.POST:
                entry[keys] = request.POST[keys]
            entry['payment_remaining'] = payment_remaining

            form = updateNewExpenseForm(entry, request.FILES, instance=expense)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                return redirect('expense_made_ledger')
            else:
                return render(request, 'edit_expense_made_ledger.html', {'errors':form.errors,'expenses':expenses, 'currencies':currencies, 'bankaccounts':bankaccounts, 'expense':expense})

        return render(request, 'edit_expense_made_ledger.html', {'expenses':expenses, 'currencies':currencies, 'bankaccounts':bankaccounts, 'expense':expense})
    else:
        return redirect('login')

def get_order_invoice_no(request):
    order_invoice_no = request.GET.get("order_invoice_no", None)
    print(order_invoice_no)
    data = {

        'currency' : SaleOrder.objects.get(id=order_invoice_no).currency.abbreviation

    }



    return JsonResponse(data)


def get_order_receipt_no(request):
    order_receipt_no = request.GET.get("order_receipt_no", None)
    data = {

        'currency' : PurchaseOrder.objects.get(id=order_receipt_no).seller_currency.abbreviation

    }



    return JsonResponse(data)

def get_next_sale_order(request):
    month = int(request.GET.get("date", None))

    if month!=0:
        date = datetime.today().date()
        month = date.month + month
        month2 = month+1
        if month>12:
            date = date.replace(month=month-12, year=date.year+1).replace(day=1)
            date2 = date.replace(month=month2-12)
        elif month2>12:
            date = date.replace(month=month).replace(day=1)
            date2 = date.replace(year=date.year+1, month=month2-12)
        else:
            date = date.replace(month=month).replace(day=1)
            date2 = date.replace(month=month2)

        print(date)
        print(date2)
        data = {

                'sale_orders' : serializers.serialize("json", SaleOrder.objects.filter(payment_due_date__gte=date,payment_due_date__lt=date2), use_natural_foreign_keys=True)

            }
        print(data['sale_orders'])
    else:
        data = {

            'sale_orders' : serializers.serialize("json", SaleOrder.objects.all(), use_natural_foreign_keys=True)

        }

    return JsonResponse(data)



def delete_purchase_order(request, id):
    if 'logged_in' in request.session:
        instance = get_object_or_404(PurchaseOrder, id=id)
        instance.delete()
        return redirect('all_purchase_orders')
    else:
        return redirect('login')


def delete_sale_order(request, id):
    if 'logged_in' in request.session:
        instance = get_object_or_404(SaleOrder, id=id)
        instance.delete()
        return redirect('all_sale_orders')
    else:
        return redirect('login')

def delete_expense_entry(request, id):
    if 'logged_in' in request.session:
        instance = get_object_or_404(ExpenseEntry, id=id)
        instance.delete()
        return redirect('all_expenses')
    else:
        return redirect('login')


def expense_made_ledger(request):
    if 'logged_in' in request.session:
        new_expenses = NewExpense.objects.all().order_by('-id')
        return render(request, 'expense_made_ledger.html', {'new_expenses':new_expenses})
    else:
        return redirect('login')

def expense_entry(request):
    if 'logged_in' in request.session:

        currencies = Currency.objects.all()
        bankaccounts = BankAccount.objects.all()

        if request.method=="POST":
            form = expenseEntryForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                last_entry = ExpenseEntry.objects.all().order_by('-id')[0]
                form = newExpenseForm({'expense_id':last_entry.id, 'expense_type':last_entry.expense_type, 'expense_date':last_entry.expense_date, 'material':last_entry.material, 'currency':last_entry.currency,
                                       'bankaccount':last_entry.bankaccount, 'amount':last_entry.amount, 'payment_remaining':last_entry.payment_remaining,
                                       "notes":last_entry.notes},request.FILES)
                if form.is_valid():
                    print(form)
                    instance = form.save(commit=False)
                    instance.save()
                    return render(request, 'expense_entry.html',{'message':'message', 'currencies':currencies, 'bankaccounts':bankaccounts})
                else:
                    return render(request, 'expense_entry.html',{'errors':form.errors, 'currencies':currencies, 'bankaccounts':bankaccounts})
            else:
                return render(request, 'expense_entry.html',{'errors':form.errors, 'currencies':currencies, 'bankaccounts':bankaccounts})




        return render(request, 'expense_entry.html',{ 'currencies':currencies, 'bankaccounts':bankaccounts})

    else:
        return redirect('login')




def delete_new_expense(request, id):
    if 'logged_in' in request.session:
        expense = get_object_or_404(NewExpense, id=id)
        expense.delete()
        return redirect('expense_made_ledger')
    else:
        return redirect('login')

def add_currency(request):
    if 'logged_in' in request.session:
        if request.method == "POST":
            form = currencyForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.save()
                return render(request, "add_currency.html",{'message':'message'})
            else:
                print(form.errors)


        return render(request, 'add_currency.html')
    else:
        return redirect('login')


def logout(request):
    if 'logged_in' in request.session:
        request.session.flush()

    return redirect('login')

def expense_view(request):
    return render(request, 'expense_view.html')