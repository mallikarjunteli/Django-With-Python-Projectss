from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.datetime_safe import datetime

from FamilyLogin.models import FamilyMembers, Expenses


def home(request):
    return render(request,'index.html')


def login_page(request):
    return render(request,'login.html',{'data': ''})


def login_user(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return render(request, "family_person.html")
    else:
        return render(request, 'login.html', {'data': 'failed'})


def register_page(request):
    return render(request,'register.html')


def register_user(request):
    email = request.POST['email']
    password = request.POST['password']
    username = request.POST['username']
    if User.objects.filter(username=username).exists():
        return render(request, 'register.html', {'user_available': True})
    elif User.objects.filter(email=email).exists():
        return render(request, 'register.html', {'email_available': True})
    else:
        user = User.objects.create_user(email=email, password=password, username=username)
        user.save()
        return render(request, 'login.html', {'data': ''})


def go_to_home(request):
    return render(request,'family_person.html')


def add_family(request):
    return render(request,'add_member.html')


def adding_member(request):
    income = request.POST['income']
    if income == '':
        context = {
            'null': True
        }
        return render(request, 'add_member.html', context)
    else:
        income = float(income)

    family_mem = FamilyMembers()
    family_mem.firstname = request.POST['firstname']
    family_mem.lastname = request.POST['lastname']
    family_mem.income = income
    family_mem.familyLead = request.user
    family_mem.save()
    return render(request, 'add_member.html')


def seefamily(request):
    family_member = FamilyMembers.objects.filter(familyLead=request.user)
    return render(request,'seefamily.html',{'data':family_member})


def add_expenses(request):
    redirect_data = FamilyMembers.objects.filter(familyLead=request.user)
    return render(request, 'add_expense.html', {'data': redirect_data})

from django.core.exceptions import MultipleObjectsReturned

def save_expense_data(request):
    exp = Expenses()
    exp.familyLead = request.user
    try:
        exp.name = FamilyMembers.objects.get(firstname=request.POST['name'])
    except MultipleObjectsReturned:
        exp.name = FamilyMembers.objects.filter(firstname=request.POST['name']).first()
    exp.purpose = request.POST['purpose']
    exp.expense = float(request.POST['expense'])
    date_from_user = request.POST.get('date')
    exp.date = datetime.strptime(date_from_user, '%Y-%m-%d')
    exp.save()
    return render(request, 'add_expense.html', {'data': FamilyMembers.objects.filter(familyLead=request.user)})


def view_expenses(request):
    all_expense = Expenses.objects.filter(familyLead=request.user)
    return render(request,'show_expense.html',{'x':all_expense})


def update_family_mem(request,id):
    family_mem = FamilyMembers.objects.get(id=id)
    if request.method == 'POST':
        family_mem.firstname = request.POST['firstname']
        family_mem.lastname = request.POST['lastname']
        family_mem.income = float(request.POST['income'])
        family_mem.save()
        get_all_data = FamilyMembers.objects.filter(familyLead=request.user)
        return render(request,'seefamily.html',{'data':get_all_data})

    return render(request,'update_family.html',{'data':family_mem})


def del_family_mem(request,id):
    family_mem = FamilyMembers.objects.get(id=id)
    family_mem.delete()
    all_updated_data = FamilyMembers.objects.filter(familyLead=request.user)
    return render(request,'seefamily.html',{'data':all_updated_data})


def update_expenses(request,id):
    obj = Expenses.objects.get(id=id)
    redirect_data = FamilyMembers.objects.filter(familyLead=request.user)
    if request.method == "POST":
        obj.familyLead = request.user
        obj.name = (FamilyMembers.objects.get(firstname=request.POST['name']))
        obj.purpose = request.POST['purpose']
        obj.expense = float(request.POST['expense'])
        date_user = request.POST.get('date')
        obj.date = datetime.strptime(date_user, '%Y-%m-%d')
        obj.save()
        get_all_data = Expenses.objects.all()
        return render(request,'show_expense.html',{'x':get_all_data})
    return render(request,'update_expense.html',{'x':obj,'data':redirect_data})


def delete_expenses(request,id):
    obj = Expenses.objects.get(id=id)
    obj.delete()
    get_data = Expenses.objects.all()
    return render(request,'show_expense.html',{'x':get_data})


def get_monthly_records(request):
        month = int(request.POST['month'])
        year = int(request.POST['year'])
        data = Expenses.objects.filter(familyLead=request.user, date__year=year, date__month=month)
        if len(data) == 0:
            no_records = " oops!! No records on that particular month and year"
            records = ""
        else:
            records = data
            no_records = ""
        list_years = list(range(2001, datetime.now().year + 1, 1))
        list_months = list(range(1, 13, 1))
        dict1 = {
            'years': list_years,
            'months': list_months,
            'records': records,
            'norecords': no_records,
            'start_month': month,
            'start_year': year,

        }
        return render(request, 'monthly_report.html', dict1)

def see_monthly_report(request):
    list_years = list(range(2002, datetime.now().year + 1, 1))
    list_months = list(range(2, 13, 1))
    dict1 = {
        'years': list_years,
        'months': list_months,
        'records': "",
        'norecords': "",
        'start_month': 1,
        'start_year': 2001
    }
    return render(request, 'monthly_report.html', dict1)


def get_yearly_records(request):
    year = int(request.POST['year'])
    data = Expenses.objects.filter(familyLead=request.user, date__year=year)
    if len(data) == 0:
        no_records = " oops!! No records on that particular  year"
        records = ""
    else:
        records = data
        no_records = ""
    list_years = list(range(2001, datetime.now().year + 1, 1))
    context = {
        'years': list_years,
        'records': records,
        'norecords': no_records,
        'start_year': year
    }
    return render(request, 'yearly_report.html', context)


def see_yearly_report(request):
    list_years = list(range(2002, datetime.now().year + 1, 1))
    context = {
        'years': list_years,
        'records': "",
        'norecords': "",
        'start_year': 2001
    }
    return render(request, 'yearly_report.html', context)

def texpense(request):
    list_years = list(range(2002, datetime.now().year + 1, 1))
    list_months = list(range(2, 13, 1))
    dict1 = {
        'years': list_years,
        'months': list_months,
        'records': "",
        'norecords': "",
        'start_month': 1,
        'start_year': 2001
    }

    return render(request,'total_expense.html',dict1)

def total_expense(request):
    # monthly expense
    month = int(request.POST['month'])
    year = int(request.POST['year'])
    data = Expenses.objects.filter(familyLead=request.user, date__year=year, date__month=month)
    e = Expenses()
    e = data
    total=0
    for i in e:
        total = total+i.expense

    # yearly expense
    year_data = Expenses.objects.filter(familyLead=request.user,date__year=year)
    e1 = Expenses()
    e1=  year_data
    yearly_total = 0
    for i in e1:
        yearly_total = yearly_total+i.expense

    list_years = list(range(2002, datetime.now().year + 1, 1))
    list_months = list(range(2, 13, 1))
    dict1 = {
        'years': list_years,
        'months': list_months,
        'start_month': 1,
        'start_year': 2001,
        'total_expense':total,
        'year_total':yearly_total
    }
    return render(request,'total_expense.html',dict1)


def logout(request):
    return redirect('loginpage')


