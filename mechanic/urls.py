from django.urls import path
from . import views


app_name = 'mechanic'

urlpatterns = [

    path( '', views.joborder_list, name='joborder_list'),
    # __________________________________________JOB ORDER_________________________________________________________
    path('joborder-list/', views.joborder_list, name='joborder_list_view'),

    path( 'mechanic/', views.joborder_list, name='joborder_list'),
    path('joborder-list/', views.joborder_list, name='joborder_list'),

    path('update-job-status/', views.update_job_status, name='update_job_status'),

    # __________________________________________ITEM REQUEST______________________________________________________
    path('create_item_req/<int:job_order_id>/', views.create_item_req, name='create_item_req'),
    path('item-requests/', views.view_item_requests, name='view_req'),
    path('item-requests/<int:item_req_num>/', views.view_item_requests, name='view_req_details'),
    path('fetch_approved_materials/', views.fetch_approved_materials, name='fetch_approved_materials'),
    path('fetch_materials/', views.fetch_materials, name='fetch_materials'),
    path('assign-mat-used/<str:item_req_num>/', views.assign_mat_used, name='assign_mat_used'),
    path('assign-material/<int:item_req_num>/', views.assign_material_to_job_order, name='assign_material_to_job_order'),
    path('request-new-material/', views.request_new_material, name='request_new_material'),
    path('view-mat-odr/', views.view_mat_odr, name='view_mat_odr'),

    # __________________________________________INVENTORY_________________________________________________________
    path('inventory/', views.inventory, name='inventory'),

    # __________________________________________ACK REC___________________________________________________________
    path('ack_rec/', views.ack_rec, name='ack_rec'),


    path('logout/', views.logout_view, name='logout'),






]