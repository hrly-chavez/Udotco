from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from shared.models import *
from .forms import *
from django.db.models import Q
from django.contrib.auth import logout
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from collections import defaultdict 
from operator import itemgetter
from django.utils.dateparse import parse_date
from datetime import datetime 
from django.db.models import Prefetch
from django.contrib import messages

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login:login')  # Redirect to login page if not logged in
        return view_func(request, *args, **kwargs)
    return wrapper 
# ___________________________________________JOB ORDER_________________________________________________________

# def joborder_list(request): 
#     # Define statuses and statuses to disable
#     statuses = Item_Request.IR_STAT_CHOICES
#     statuses_to_disable = ['Pending','Done']

#     # Filter by status if provided
#     status_filter = request.GET.get('status', '')

#     # Apply filters
#     filters = Q()
#     if status_filter:
#         filters &= Q(j_o_status=status_filter)

#     # Sort job orders by status and then by job order number
#     pending_jobs = JobOrder.objects.filter(filters & Q(j_o_status="Pending")).order_by('j_o_number')
#     ongoing_jobs = JobOrder.objects.filter(filters & Q(j_o_status="Ongoing")).order_by('j_o_number')
#     completed_jobs = JobOrder.objects.filter(filters & Q(j_o_status="Done")).order_by('j_o_number')

#     # Combine results
#     job_orders = list(pending_jobs) + list(ongoing_jobs) + list(completed_jobs)

#     # Fetch employees from the Vehicle Maintenance Department
#     vehicle_maintenance_employees = Employee.objects.filter(dept_id__dept_name="Vehicle Maintenance Department")

#     # Render template with context
#     return render(request, 'mechanic/manage_jo/joborder_list.html', {
#         'statuses': statuses,
#         'job_orders': job_orders,
#         'statuses_to_disable': statuses_to_disable,
#         'employees': vehicle_maintenance_employees,
#     })
@login_required
def joborder_list(request): 
    # Define statuses and statuses to disable
    statuses = Item_Request.IR_STAT_CHOICES
    statuses_to_disable = ['Pending','Done']

    # Filter by status if provided
    status_filter = request.GET.get('status', '')

    # Apply filters
    filters = Q()
    if status_filter:
        filters &= Q(j_o_status=status_filter)

    # Sort job orders by status and then by job order number
    pending_jobs = JobOrder.objects.filter(filters & Q(j_o_status="Pending")).order_by('j_o_number')
    ongoing_jobs = JobOrder.objects.filter(filters & Q(j_o_status="Ongoing")).order_by('j_o_number')
    completed_jobs = JobOrder.objects.filter(filters & Q(j_o_status="Done")).order_by('j_o_number')

    # Combine results
    job_orders = list(pending_jobs) + list(ongoing_jobs) + list(completed_jobs)

    # Fetch employees from the Vehicle Maintenance Department
    vehicle_maintenance_employees = Employee.objects.filter(dept_id__dept_name="Vehicle Maintenance Department")

    # Fetch related Item Requests for each Job Order
    item_requests = Item_Request.objects.filter(job_order__in=job_orders)

    # Render template with context
    return render(request, 'mechanic/manage_jo/joborder_list.html', {
        'statuses': statuses,
        'job_orders': job_orders,
        'statuses_to_disable': statuses_to_disable,
        'employees': vehicle_maintenance_employees,
        'item_requests': item_requests,
    })


@login_required
@csrf_exempt
def update_job_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        job_order_id = data.get('job_order_id')
        next_status = data.get('next_status')
        assigned_mechanic = data.get('assigned_mechanic', None)

        try:
            job_order = JobOrder.objects.get(j_o_number=job_order_id)

            # Assign mechanic if applicable
            if next_status == "Ongoing" and assigned_mechanic:
                mechanic = Employee.objects.get(emp_id=assigned_mechanic)
                job_order.j_o_checked_by = mechanic

            # Update status and date completed
            job_order.j_o_status = next_status
            if next_status == "Done":
                job_order.j_o_date_completed = now()
            
            job_order.save()
            return JsonResponse({'success': True, 'message': 'Status updated successfully.'})
        except JobOrder.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Job Order not found.'})
        except Employee.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Mechanic not found.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})
@login_required
def assign_mat_used(request, item_req_num):  # Assign Material Used
    # Fetch the item request details by numeric ID
    item_request = get_object_or_404(Item_Request, item_req_num=item_req_num)

    # Fetch related materials and material orders
    materials = Material_Requested.objects.filter(item_req_num=item_request).select_related(
        'mat_code', 'mat_code__mat_category'
    )
    material_orders = Material_Order.objects.filter(item_req_num=item_request)

    # Check if all materials and orders have been assigned already
    materials_assigned = all(material.mat_req_status == 'Approved' for material in materials)
    orders_assigned = all(order.mat_odr_status == 'Assigned' for order in material_orders)

    # Flags to determine if the assign button should be enabled
    assignable_materials = any(material.mat_req_status == 'Approved' for material in materials)
    assignable_orders = any(order.mat_odr_status == 'Approved' for order in material_orders)

    context = {
        'job_order': item_request.job_order,
        'materials': materials,
        'material_orders': material_orders,
        'item_request': item_request,
        'materials_assigned': materials_assigned,
        'orders_assigned': orders_assigned,
        'assignable_materials': assignable_materials,
        'assignable_orders': assignable_orders,
    }

    return render(request, 'mechanic/manage_jo/assign_mat_used.html', context)

@login_required
def assign_material_to_job_order(request, item_req_num):
    if request.method == "POST":
        item_request = get_object_or_404(Item_Request, item_req_num=item_req_num)
        materials = Material_Requested.objects.filter(item_req_num=item_request).select_related('mat_code')
        material_orders = Material_Order.objects.filter(item_req_num=item_request)

        job_order = item_request.job_order
        if not job_order:
            messages.error(request, "No job order is associated with this item request.")
            return redirect('mechanic:assign_mat_used', item_req_num=item_req_num)

        try:
            # Handle Material Requests
            for material in materials:
                if material.mat_req_status == 'Pending':
                    messages.error(request, "Cannot assign material(s) because one or more are still Pending.")
                    return redirect('mechanic:assign_mat_used', item_req_num=item_req_num)

                # Check if the material with the same mat_req_id has already been assigned
                if Material_Used.objects.filter(mat_req_id=material.mat_req_id).exists():
                    messages.error(request, f"The material {material.mat_code.mat_name} has already been assigned.")
                    return redirect('mechanic:assign_mat_used', item_req_num=item_req_num)

                # Assign the material
                Material_Used.objects.create(
                    mat_used_name=material.mat_code.mat_name,
                    mat_used_qty=material.mat_req_qty, 
                    mat_used_brand=material.mat_code.mat_brand,
                    mat_used_measurement=material.mat_code.mat_measurement,
                    mat_req_id=material.mat_req_id,  # Save the mat_req_id for future checks
                )
                material.mat_req_status = 'Assigned'  # Update status to 'Assigned'
                material.save()

            # Handle Material Orders
            for order in material_orders:
                if order.mat_odr_status == 'Pending':
                    messages.error(request, "Cannot assign material order(s) because one or more are still Pending.")
                    return redirect('mechanic:assign_mat_used', item_req_num=item_req_num)

                # Check if the material order (mat_odr) has already been assigned
                if Material_Used.objects.filter(mat_odr=order).exists():
                    messages.error(request, f"The material order {order.mat_odr_name} has already been assigned.")
                    return redirect('mechanic:assign_mat_used', item_req_num=item_req_num)

                # Assign the material order
                Material_Used.objects.create(
                    mat_used_name=order.mat_odr_name,
                    mat_used_qty=order.mat_odr_qty,
                    mat_used_brand=order.mat_odr_brand,
                    mat_used_measurement=order.mat_category.mat_name,
                    mat_odr=order,  # Save the relationship with Material_Order
                )
                order.mat_odr_status = 'Assigned'  # Update status to 'Assigned'
                order.save()

            messages.success(request, "Materials and material orders have been successfully assigned to the job order.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect('mechanic:joborder_list')

    messages.error(request, "Invalid request method.")
    return redirect('mechanic:assign_mat_used', item_req_num=item_req_num)




# ___________________________________________ITEM REQUEST__________________________________________________________
    
@login_required
def fetch_approved_materials(request):
    """
    Fetch materials with approved status from the Material_Requested model for the select2 dropdown.
    """
    if request.method == "GET":
        query = request.GET.get('q', '')

        # Fetch approved materials
        materials = Material_Requested.objects.filter(mat_req_status="Approved").select_related('mat_code')

        if query:
            materials = materials.filter(mat_code__mat_name__icontains=query)

        
        # Format results for select2
        results = [
            {
                'id': material.mat_code_id,
                'text': material.mat_code.mat_name,
                'mat_req_qty': material.mat_req_qty,
            }
            for material in materials
        ]
        return JsonResponse({'results': results})
@login_required   
def fetch_materials(request):
    material_id = request.GET.get("material_id")
    query = request.GET.get("q", "")  # Get search term from request

    if material_id:
        # Handle fetching details for a specific material
        try:
            material = Material.objects.get(pk=material_id)
            return JsonResponse({
                "mat_max_request": material.mat_max_request,
                "mat_qty_available": material.mat_quantity,
            })
        except Material.DoesNotExist:
            return JsonResponse({"error": "Material does not exist."}, status=404)

    # Handle search functionality for Select2 dropdown
    materials = Material.objects.filter(mat_name__icontains=query)  # Search by mat_name
    data = []
    for material in materials:
        data.append({
            'id': material.mat_code,  # Use mat_code as the primary key
            'text': f"Category: {material.mat_category} | Material Name: {material.mat_name} | Qnty Available: {material.mat_quantity}"
        })

    return JsonResponse({'results': data})
@login_required
def view_item_requests(request):
    item_req_date_requested = request.GET.get('item_req_date_requested', '').strip()

    # Fetch all item requests with related fields
    item_requests = Material_Requested.objects.select_related(
        'mat_code__mat_category',
        'item_req_num__bus_unit_num',
        'item_req_num__item_req_approved_by',
        'item_req_num__job_order'  # Include JobOrder relationship
    ).order_by('-item_req_num__item_req_date_requested')

    # Apply date filter if provided
    if item_req_date_requested:
        req_date = parse_date(item_req_date_requested)
        if req_date:
            start_of_day = datetime.combine(req_date, datetime.min.time())
            end_of_day = datetime.combine(req_date, datetime.max.time())
            item_requests = item_requests.filter(
                item_req_num__item_req_date_requested__range=(start_of_day, end_of_day)
            )

    # Group by item_req_num
    grouped_requests = defaultdict(lambda: {'details': None, 'items': []})
    for item in item_requests:
        item_req_num = item.item_req_num.item_req_num
        grouped_requests[item_req_num]['details'] = item
        grouped_requests[item_req_num]['items'].append(item)

    # Sort by item_req_num
    sorted_grouped_requests = dict(sorted(grouped_requests.items(), key=itemgetter(0), reverse=True))


    context = {
        'grouped_requests': sorted_grouped_requests,
        'item_req_date_requested': item_req_date_requested,
    }

    return render(request, 'mechanic/item_req/view_req.html', context)


# def create_item_req(request, job_order_id):
#     job_order = get_object_or_404(JobOrder, pk=job_order_id)
#     vehicle_maintenance_employees = Employee.objects.filter(dept_id__dept_name="Vehicle Maintenance Department")

#     if request.method == "POST":
#         form = ItemRequestForm(request.POST, job_order=job_order)
#         materials = json.loads(request.POST.get("materials", "[]"))  # Parse materials data
#         approved_by_id = request.POST.get("item_req_approved_by")

#         if form.is_valid():
#             try:
#                 # Check material quantities
#                 for material in materials:
#                     material_id = material["material_id"]
#                     quantity = int(material["quantity"])

#                     material_instance = get_object_or_404(Material, pk=material_id)

#                     if quantity > material_instance.mat_quantity:
#                         raise ValidationError(
#                             f"Requested quantity for {material_instance.mat_name} exceeds available stock ({material_instance.mat_quantity})."
#                         )
#                     if quantity > material_instance.mat_max_request:
#                         raise ValidationError(
#                             f"Requested quantity for {material_instance.mat_name} exceeds maximum requestable limit ({material_instance.mat_max_request})."
#                         )

#                 # Save item request
#                 form.instance.item_req_date_requested = timezone.now()
#                 form.instance.job_order = job_order
#                 item_request = form.save()

#                 # Save Material_Requested
#                 for material in materials:
#                     Material_Requested.objects.create(
#                         mat_code=Material.objects.get(pk=material["material_id"]),
#                         mat_req_qty=int(material["quantity"]),
#                         item_req_num=item_request,
#                     )

#                 # Update JobOrder
#                 job_order.j_o_status = "Ongoing"
#                 if approved_by_id:
#                     job_order.j_o_checked_by = Employee.objects.get(emp_id=approved_by_id)
#                 job_order.save()

#                 return redirect('mechanic:view_req')  # Redirect to view request

#             except ValidationError as e:
#                 return JsonResponse({"success": False, "errors": str(e)})

#         else:
#             return JsonResponse({"success": False, "errors": form.errors})

#     else:
#         form = ItemRequestForm(job_order=job_order)

#     return render(request, 'mechanic/item_req/create_item_req.html', {
#         'job_order': job_order,
#         'employees': vehicle_maintenance_employees,
#         'form': form,
#     })
@login_required
def create_item_req(request, job_order_id):
    job_order = get_object_or_404(JobOrder, pk=job_order_id)
    vehicle_maintenance_employees = Employee.objects.filter(dept_id__dept_name="Vehicle Maintenance Department")
    assigned_mechanic = job_order.j_o_checked_by  # Fetch the assigned mechanic

    if request.method == "POST":
        form = ItemRequestForm(request.POST, job_order=job_order)
        materials = json.loads(request.POST.get("materials", "[]"))  # Parse materials data
        approved_by_id = request.POST.get("item_req_approved_by")

        if form.is_valid():
            try:
                # Save the Item_Request instance
                item_request = form.save(commit=False)
                item_request.item_req_approved_by_id = approved_by_id  # Assign the approved_by ID
                item_request.job_order = job_order
                item_request.save()

                # Link materials to the Item_Request
                for material in materials:
                    material_id = material["material_id"]
                    requested_qty = int(material["quantity"])

                    # Validate the material exists
                    material_instance = Material.objects.get(pk=material_id)

                    # Create a Material_Requested instance
                    Material_Requested.objects.create(
                        item_req_num=item_request,
                        mat_code=material_instance,
                        mat_req_qty=requested_qty,
                        mat_req_status='Pending',  # Default status
                    )

                return redirect('mechanic:view_req')  # Redirect to view request
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = ItemRequestForm(initial={
            'bus_unit_num': job_order.j_o_bus_unit_num,
            'item_req_status': 'Waiting',
        })

    return render(request, 'mechanic/item_req/create_item_req.html', {
        'form': form,
        'job_order': job_order,
        'employees': vehicle_maintenance_employees,
        'assigned_mechanic': assigned_mechanic,  # Pass to template
    })





from django.http import JsonResponse

# def request_new_material(request):
#     bus_unit_num = request.GET.get('bus_unit_num')
#     approved_by = request.GET.get('approved_by')
#     job_order_num = request.GET.get('job_order_num')  # Retrieve the job order number

#     if request.method == 'POST':
#         materials_data = request.POST.get('materials')
#         materials = json.loads(materials_data)  # Parse JSON data

#         # Save each material to the Material_Order model
#         for material in materials:
#             mat_category = Material_Category.objects.get(mat_category_id=material["category"])
#             Material_Order.objects.create(
#                 mat_odr_name=material["name"],
#                 mat_odr_qty=material["quantity"],
#                 mat_odr_brand=material["brand"],
#                 mat_odr_measurement=material["measurement"],
#                 mat_category=mat_category,
#             )

#         return redirect("mechanic:view_req")  # Redirect to the view request page

#     categories = Material_Category.objects.all()
#     return render(
#         request,
#         "mechanic/item_req/req_new_mat.html",
#         {
#             "categories": categories, 
#             "bus_unit_num": bus_unit_num,
#             "approved_by": approved_by,
#             "job_order_num": job_order_num,
#         },
#     )
@login_required
def request_new_material(request):
    # Retrieve necessary data for the template
    bus_unit_num = request.GET.get('bus_unit_num', '')
    job_order_num = request.GET.get('job_order_num', '')
    item_req_num = request.GET.get('item_req_num', None)  # Get item_req_num if provided

    if request.method == 'POST':
        materials_data = request.POST.get('materials')
        materials = json.loads(materials_data) if materials_data else []

        # Create the item request first (if item_req_num is not provided)
        if not item_req_num:
            item_request = Item_Request.objects.create(
                bus_unit_num_id=bus_unit_num,
                job_order_id=job_order_num
            )
            item_req_num = item_request.item_req_num  # Get the newly created item_req_num

        # Create Material_Order instances
        for material in materials:
            mat_category = Material_Category.objects.get(mat_category_id=material["category_id"])
            Material_Order.objects.create(
                mat_odr_name=material["name"],
                mat_odr_qty=material["quantity"],
                mat_odr_brand=material["brand"],
                mat_odr_measurement=material["measurement"],
                mat_category=mat_category,
                item_req_num_id=item_req_num,  # Link to the created Item_Request
            )

        # Redirect to the view_mat_odr.html template
        return redirect("mechanic:view_mat_odr")  # Adjust the URL name as needed

    categories = Material_Category.objects.all()

    return render(
        request,
        "mechanic/item_req/req_new_mat.html",
        {
            "categories": categories,
            "bus_unit_num": bus_unit_num,
            "job_order_num": job_order_num,
        },
    )

@login_required
def view_mat_odr(request):
    # Get the filter value for material name if provided
    mat_odr_name_filter = request.GET.get('mat_odr_name', '')

    # Fetch the material orders along with related item requests
    material_orders = Material_Order.objects.prefetch_related(
        Prefetch('item_req_num', queryset=Item_Request.objects.select_related('job_order', 'item_req_approved_by', 'bus_unit_num'))
    )

    if mat_odr_name_filter:
        material_orders = material_orders.filter(mat_odr_name__icontains=mat_odr_name_filter)

    # Organize the data by item_req_num
    grouped_material_orders = {}
    for material_order in material_orders:
        # Get the related item request number
        item_req_num = material_order.item_req_num  # Assuming there's a reverse relationship

        if item_req_num:
            # If item_req_num is not in the dictionary, initialize the entry
            if item_req_num not in grouped_material_orders:
                grouped_material_orders[item_req_num] = {
                    'item_req_num': item_req_num,
                    'bus_unit_num': item_req_num.bus_unit_num,
                    'j_o_number': item_req_num.job_order.j_o_number if item_req_num.job_order else "No J.O.",
                    'approved_by': item_req_num.item_req_approved_by.emp_fname + ' ' + item_req_num.item_req_approved_by.emp_lname if item_req_num.item_req_approved_by else "N/A",  # Approved By
                    'description': item_req_num.item_req_description,  # Description
                    'date_requested': item_req_num.item_req_date_requested,
                    'status': item_req_num.item_req_status,
                    'materials': [],
                }

            # Append the material order to the corresponding item request
            grouped_material_orders[item_req_num]['materials'].append(material_order)

    return render(
        request,
        "mechanic/item_req/view_mat_odr.html",
        {
            "grouped_material_orders": grouped_material_orders,
            "mat_odr_name_filter": mat_odr_name_filter,
        }
    )


# ___________________________________________INVENTORY__________________________________________________________
@login_required
def inventory(request):
    search_query = request.GET.get('search', '')
    selected_category = request.GET.get('category', '')

    # Fetch all categories for the dropdown
    categories = Material_Category.objects.values('mat_category_id', 'mat_name').distinct()

    # Filter materials based on search and category
    materials = Material.objects.all()
    if search_query:
        materials = materials.filter(mat_name__icontains=search_query) 
    if selected_category:
        materials = materials.filter(mat_category_id=selected_category)

    return render(request, 'mechanic/inventory/inventory.html', {
        'materials': materials,
        'categories': categories,
        'search_query': search_query,
        'selected_category': selected_category,
    })

# ___________________________________________ACKNOWLEDGEMENT____________________________________________________
@login_required
def ack_rec(request):
    search_query = request.GET.get('search', '').strip()

    if request.method == 'POST':
        receipt_id = request.POST.get('receipt_id')
        receiver_id = request.POST.get('receiver_id')

        try:
            receipt = Acknowledgment_Receipt.objects.get(ar_num=receipt_id)
            receiver = Employee.objects.get(emp_id=receiver_id)

            receipt.ar_date_receiver = receiver
            receipt.ar_status = 'Delivered'
            receipt.ar_date_received = now()
            receipt.save()
        except (Acknowledgment_Receipt.DoesNotExist, Employee.DoesNotExist):
            pass

        return redirect('mechanic:ack_rec')

    receipts = Acknowledgment_Receipt.objects.prefetch_related(
        Prefetch(
            'item_approved_id__mat_req_id__approved_materials',
            queryset=Material_Approved.objects.select_related('mat_approved_code'),
            to_attr='materials'
        )
    ).filter(
        Q(ar_num__icontains=search_query) | Q(ar_note__icontains=search_query)
    )

    vehicle_maintenance_department = Department.objects.get(dept_name='Vehicle Maintenance Department')
    vehicle_maintenance_employees = Employee.objects.filter(dept_id=vehicle_maintenance_department)

    context = {
        'receipts': receipts,
        'vehicle_maintenance_employees': vehicle_maintenance_employees,
    }

    return render(request, "mechanic/ack_rec/ack_rec.html", context)

@login_required
def logout_view(request):
    # Clear the session (log out the user)
    logout(request)
    
    # Redirect to the login page after logout
    return redirect('login:login')  # Make sure the 'login' URL name matches the one in your URL configuration



