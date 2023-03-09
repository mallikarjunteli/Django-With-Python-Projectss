from django.urls import path

from FamilyLogin import views

urlpatterns=[
    path('',views.home),
    path('loginpage',views.login_page,name='loginpage'),   # redirect to login.html
    path('loginuser',views.login_user,name='loginuser'),

    path('registerpage',views.register_page,name='registerpage'),   # redirect to register.html
    path('registeruser', views.register_user),

    path('gotohome', views.go_to_home, name="gotohome"),  # redirect to family_person.html page

    path('addfamilymembers', views.add_family, name='addfamily'),   # redirect to add_member.html page
    path('addingmember',views.adding_member,name='addingmember'),   # adding members to table
    path('seefamily',views.seefamily,name='seefamily'),    # display family member details

    path('addingexpenses', views.add_expenses, name="addexpenses"),   # redirect to expense page
    path('saveexpensedata',views.save_expense_data,name='saveexpenses'),   # adding expense to table
    path('viewexpenses', views.view_expenses, name="viewexpenses"),

    path('updatemem/<int:id>', views.update_family_mem, name="update"),  # update_family.html
    path('delmem/<int:id>', views.del_family_mem, name="delete"),

    path('updateExpenses/<int:id>', views.update_expenses, name="updateExpenses"),  #update_expense.html
    path('deleteExpenses/<int:id>',views.delete_expenses,name='deleteExpenses'),

    path('getmonthlyrecords', views.get_monthly_records),
    path('seemonthlyreport', views.see_monthly_report, name="seemonthlyreport"),

    path('getyearlyrecords', views.get_yearly_records, name="getyearlyrecords"),
    path('seeyearlyreport', views.see_yearly_report, name="seeyearlyreport"),

    path('totalexpense',views.total_expense),
    path('texpense',views.texpense,name="texpense"),
    path('logout',views.logout,name="logout")
]