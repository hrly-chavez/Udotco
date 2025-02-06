from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'it'

urlpatterns = [ 
#________________________department_____________________________________
    path('department/', views.department, name='department'), 
    path('operational/', views.operational, name='operational'), 
    path('it_dep/', views.it_dep, name='it_dep'), 
    path('transportation/', views.transportation, name='transportation'), 
    path('vehicle_maintenance', views.vm, name='vm'), 
    path('HR/', views.hr, name='hr'), 
    path('finance_dept/', views.finance, name='finance'), 
    path('fuel/', views.fuel, name='fuel'), 
    path('safety/', views.safety, name='safety'), 
    path('dispatch/', views.dispatch, name='dispatch'), 
    path('officer/', views.officer, name='officer'), 

#__________________________employee_______________________________________
    path('add_employee/', views.add_employee, name='add_employee'),
    path('edit_employee/<int:emp_id>/', views.edit_employee, name='edit_employee'),
    path('delete_employee/<int:emp_id>/', views.delete_employee, name='delete_employee'),

#___________________________bus____________________________________________
    path('bus/', views.bus, name='bus'), 
    path('add_bus/', views.add_bus, name='add_bus'),
    path('edit_bus/<str:bus_unit_num>/', views.edit_bus, name='edit_bus'),
    path('delete_bus/<str:bus_unit_num>/', views.delete_bus, name='delete_bus'),

#_____________________________joborder______________________________________
    path('JO/', views.JO, name='JO'), 

#_____________________________ack_req_______________________________________
    path('AR/', views.AR, name='AR'), 

#________________________________purchase_order_________________________________
    # path('purchase_ordr/', views.it_purchase_odr, name='purchase_odr'), 
    # path('purchase_order_it/view/<int:po_num>/', views.it_purchase_odr, name='view_purchase_odr'),  # View specific purchase order
    path('purchase_ordr/', views.it_purchase_odr, name='purchase_odr'), 
    path('purchase_order_it/view/<int:po_num>/', views.it_purchase_odr, name='view_purchase_odr'),  # View specific purchase order
    path('purchase_order_it/filter/', views.filter_purchase_orders, name='filter_purchase_orders'),

#________________________________materials________________________________________
    path('materials_it/', views.materials_it, name='materials_it'), 

#_________________________________accounts________________________________________
    path('Accounts/', views.account, name='Accounts'),
    path('add_account/', views.add_account, name='add_account'),
    path('delete_account/<str:username>/', views.delete_account, name='delete_account'),
    path('edit_account/<str:username>/', views.edit_account, name='edit_account'),
    
#________________________________logout_____________________________________________
    path('logout/', views.logout_view, name='logout'),
    
 ]

if settings.DEBUG:
    urlpatterns += static('/IT/images/', document_root='./IT/images/')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)