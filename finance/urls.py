# from django.urls import path
# from . import views

# app_name='finance'

# urlpatterns = [
#     path('finance/', views.mechanic_req, name = 'mechanic_req'),
#     path('mechanic request/', views.mechanic_req, name = 'mechanic_req'),
#     path('itemreq/', views.mechanic_req, name='itemreq'),
#     path('approve-material/<int:mat_req_id>/', views.approve_material, name='approve_material'),
#     path('deny-material/<int:mat_req_id>/', views.deny_material, name='deny_material'),
    
# #___________________________________________MATERIAL_________________________________________________

#     path('material/edit/<int:mat_code>/', views.edit_material, name='edit_material'),
#     path('material/delete/<int:mat_code>/', views.delete_material, name='delete_material'),
#     path('materials/', views.materials, name = 'materials'),
#     path('material/add/', views.add_material, name='add_material'),
    

# #_________________________________________PURCHASE ODR___________________________________________________
    
#     path('make_purchase_odr/', views.create_purchase_order, name='make_purchase_odr'),
#     path('purchase_order/', views.purchase_odr, name='purchase_odr'),  
#     path('purchase_order/view/<int:po_num>/', views.purchase_odr, name='view_purchase_odr'),  
#     path('edit_purchase_order/<int:po_num>/', views.edit_purchase_order, name='edit_purchase_odr'),
#     path('purchase_order/delete/<int:po_num>/', views.delete_purchase_order, name='delete_purchase_odr'),
#     path('purchase_order/filter/', views.filter_purchase_orders, name='filter_purchase_orders'),

# #_________________________________________ACKNOWLEDGE RECEIPT_____________________________________________
#     path('ack-rep/', views.ack_rep, name='ack_rep'),
#     path('create-ack-rep/', views.create_ack_rep, name='create_ack_rep'),
# #_________________________________________________________________________________________________________
#     path('logout/', views.logout_view, name='logout'),
    
# ] 

from django.urls import path
from . import views

app_name='finance'

urlpatterns = [
    path('finance/', views.mechanic_req, name = 'mechanic_req'),
    path('mechanic request/', views.mechanic_req, name = 'mechanic_req'),
    path('itemreq/', views.mechanic_req, name='itemreq'),
    path('approve-material/<int:mat_req_id>/', views.approve_material, name='approve_material'),
    path('deny-material/<int:mat_req_id>/', views.deny_material, name='deny_material'),
    
#___________________________________________MATERIAL_________________________________________________

    path('material/edit/<int:mat_code>/', views.edit_material, name='edit_material'),
    path('material/delete/<int:mat_code>/', views.delete_material, name='delete_material'),
    path('materials/', views.materials, name = 'materials'),
    path('material/add/', views.add_material, name='add_material'),
    

#_________________________________________PURCHASE ODR___________________________________________________
    
    
    path('purchase_order/create/', views.create_purchase_order, name='create_purchase_order'),
    path('purchase_order/', views.purchase_odr, name='purchase_odr'),  
    path('purchase_order/view/<int:po_num>/', views.purchase_odr, name='view_purchase_odr'),  
    path('edit_purchase_order/<int:po_num>/', views.edit_purchase_order, name='edit_purchase_odr'),
    path('purchase_order/delete/<int:po_num>/', views.delete_purchase_order, name='delete_purchase_odr'),
    path('purchase_order/filter/', views.filter_purchase_orders, name='filter_purchase_orders'),
    path('approve-material-order/<int:mat_odr_id>/', views.approve_material_order, name='approve_material_order'),
    path('decline-material-order/<int:mat_odr_id>/', views.deny_material_order, name='decline_material_order'),
    
#_________________________________________ACKNOWLEDGE RECEIPT_____________________________________________
    path('ack-rep/', views.ack_rep, name='ack_rep'),
    path('create-ack-rep/', views.create_ack_rep, name='create_ack_rep'),
    path('delete/<int:ar_num>/', views.delete_ack_rep, name='delete_ack_rep'),
#_________________________________________________________________________________________________________
    path('logout/', views.logout_view, name='logout'),
    
]