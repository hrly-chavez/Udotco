from django.shortcuts import render, redirect, get_object_or_404
from shared.models import *
from django.contrib import messages
from django.urls import reverse
from .forms import *
from django.db.models import Q
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import logout
from datetime import datetime
# from .forms import *


# Create your views here.

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login:login')  # Redirect to login page if not logged in
        return view_func(request, *args, **kwargs)
    return wrapper

#_____________________________________DEPARTMENT_________________________________________
@login_required
def department(request):
    return render(request, 'IT/department/department.html')

@login_required
def operational(request):
    # Filter the Operational Manager department
    operational_dept = get_object_or_404(Department, dept_name__iexact="Operational Manager")
    employees = Employee.objects.filter(dept_id=operational_dept).order_by('emp_fname')  # Sort by last name A-Z

    return render(
        request,
        'IT/department/operational_manager.html',
        {'employee': employees, 'department': operational_dept}
    )

@login_required
def it_dep(request):
    it_dept = get_object_or_404(Department, dept_name__iexact="I.T. Department")
    # employees = Employee.objects.filter(dept_id=it_dept)
    employees = Employee.objects.filter(dept_id=it_dept).order_by('emp_fname')  # Sort by last name A-Z

    return render(
        request,
        'IT/department/i.t._department.html',
        {'employee': employees, 'department': it_dept}
    )

@login_required
def transportation(request):
    transportation_dept = get_object_or_404(Department, dept_name__iexact="Transportation Department")
    employees = Employee.objects.filter(dept_id=transportation_dept).order_by('emp_fname')  # Sort by last name A-Z

    return render(
        request,
        'IT/department/transportation_department.html',
        {'employee': employees, 'department': transportation_dept}
    )

@login_required
def vm(request):
    vm_dept = get_object_or_404(Department, dept_name__iexact="Vehicle Maintenance Department")
    employees = Employee.objects.filter(dept_id=vm_dept).order_by('emp_fname')  # Sort by last name A-Z

    return render(
        request,
        'IT/department/vehicle_maintenance_department.html',
        {'employee': employees, 'department': vm_dept}
    )

@login_required
def hr(request):
    hr_dept = get_object_or_404(Department, dept_name__iexact="H.R. Department")
    employees = Employee.objects.filter(dept_id=hr_dept).order_by('emp_fname')  # Sort by last name A-Z

    return render(
        request,
        'IT/department/h.r._department.html',
        {'employee': employees, 'department': hr_dept}
    )

@login_required
def finance(request):
    finance_dept = get_object_or_404(Department, dept_name__iexact="Finance Department")
    employees = Employee.objects.filter(dept_id=finance_dept).order_by('emp_fname')  # Sort by last name A-Z

    return render(
        request,
        'IT/department/finance_department.html',
        {'employee': employees, 'department': finance_dept}
    )

@login_required
def fuel(request):
    fuel_dept = get_object_or_404(Department, dept_name__iexact="Fuel Department")
    employees = Employee.objects.filter(dept_id=fuel_dept).order_by('emp_fname')  # Sort by last name A-Z

    return render(
        request,
        'IT/department/fuel_department.html',
        {'employee': employees, 'department': fuel_dept}
    )

@login_required
def safety(request):
    safety_dept = get_object_or_404(Department, dept_name__iexact="Safety Department")
    employees = Employee.objects.filter(dept_id=safety_dept).order_by('emp_fname')  # Sort by last name A-Z

    return render(
        request,
        'IT/department/safety_department.html',
        {'employee': employees, 'department': safety_dept}
    )

@login_required
def dispatch(request):
    dispatch_dept = get_object_or_404(Department, dept_name__iexact="Dispatch Department")
    employees = Employee.objects.filter(dept_id=dispatch_dept).order_by('emp_fname')  # Sort by last name A-Z

    return render(
        request,
        'IT/department/dispatch_department.html',
        {'employee': employees, 'department': dispatch_dept}
    )

@login_required
def officer(request):
    officer_dept = get_object_or_404(Department, dept_name__iexact="Officers")
    employees = Employee.objects.filter(dept_id=officer_dept).order_by('emp_fname')  # Sort by last name A-Z

    return render(
        request,
        'IT/department/officer_department.html',
        {'employee': employees, 'department': officer_dept}
    )


#_______________________________EMPLOYEE_______________________________________
@login_required
def add_employee(request):
    errors = {}  # Dictionary to store custom error messages
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)

        # Custom validation for Middle Initial
        emp_initial = request.POST.get('emp_initial', '').strip()
        if emp_initial and not emp_initial.isalpha():
            errors['emp_initial'] = "Middle Initial should contain only letters."

        # Custom validation for Contact Number
        emp_contact_num = request.POST.get('emp_contact_num', '').strip()
        if emp_contact_num and not emp_contact_num.isdigit():
            errors['emp_contact_num'] = "Contact Number should contain only numbers."

        # If the form is valid and there are no custom errors, save the form
        if form.is_valid() and not errors:
            form.save()
            messages.success(request, 'Employee successfully added!')
            return redirect('it:department')
        else:
            # Add errors from the form to the error dictionary
            errors.update(form.errors)

    else:
        form = EmployeeForm()

    return render(request, 'IT/department/add_employee.html', {
        'form': form,
        'errors': errors  # Pass errors to the template
    })

@login_required
def edit_employee(request, emp_id):
    employee = get_object_or_404(Employee, pk=emp_id)  # Fetch employee by ID or return 404

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)  # Bind data to form

        # Initialize a flag to track custom validation errors
        custom_error_flag = False

        # Custom validation for Middle Initial
        emp_initial = request.POST.get('emp_initial', '').strip()
        if emp_initial and not emp_initial.isalpha():
            form.add_error('emp_initial', "Middle Initial should contain only letters.")
            custom_error_flag = True

        # Custom validation for Contact Number
        emp_contact_num = request.POST.get('emp_contact_num', '').strip()
        if emp_contact_num and not emp_contact_num.isdigit():
            form.add_error('emp_contact_num', "Contact Number should contain only numbers.")
            custom_error_flag = True

        # Validate form and check for custom validation errors
        if form.is_valid() and not custom_error_flag:
            form.save()  # Save changes to the employee instance
            messages.success(request, "Employee details updated successfully!")
            return redirect('it:department')  # Redirect to the operational manager page
        else:
            # Instead of a generic message, show specific field errors
            for errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = EmployeeForm(instance=employee)  # Populate form with existing employee data

    return render(request, 'IT/department/edit_employee.html', {
        'form': form,
        'edit_mode': True,  # Pass a flag to indicate edit mode
        'employee': employee,
        'hide_messages': True
    })


@login_required
def delete_employee(request, emp_id):
    employee = get_object_or_404(Employee, pk=emp_id)

    # Delete the associated image file
    if employee.emp_image:  # Ensure the employee has an image path
        image_path = os.path.join(settings.MEDIA_ROOT, employee.emp_image.name)  # Get full file path
        if os.path.exists(image_path):  # Check if the file exists
            os.remove(image_path)  # Delete the file from the filesystem

    # Delete the employee record from the database
    employee.delete()
    messages.success(request, f"Employee {employee.emp_fname} {employee.emp_lname} and associated image have been deleted successfully.")
    return redirect('it:department')  # Adjust this to redirect to the appropriate page


#___________________________________BUS______________________________________________
@login_required
def bus(request):
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '')

    buses = Bus.objects.all()

    # Apply search filter
    if search_query:
        buses = buses.filter(
            Q(bus_unit_num__icontains=search_query) |
            Q(bus_license_plate_number__icontains=search_query) |
            Q(bus_chassis_num__icontains=search_query) |
            Q(bus_engine_num__icontains=search_query) |
            Q(bus_year_model__icontains=search_query) |
            Q(bus_tag_num__icontains=search_query)
        )

    # Apply sorting
    if sort_by in ['bus_unit_num', 'bus_license_plate_number', 'bus_chassis_num', 'bus_engine_num', 'bus_year_model', 'bus_tag_num']:
        buses = buses.order_by(sort_by)

    context = {'buses': buses}
    return render(request, 'IT/Bus/bus.html', context)

@login_required
def add_bus(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Bus added successfully!")
            return redirect('it:bus')  # Redirect to the bus list or relevant page
        else:
            # Display form errors using Django's form error handling mechanism
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = BusForm()

    return render(request, 'IT/Bus/add_bus.html', {'form': form})


@login_required
def edit_bus(request, bus_unit_num):
    bus = get_object_or_404(Bus, pk=bus_unit_num)
    if request.method == 'POST':
        # Pass the hidden field's value to retain the bus_unit_num
        form = BusForm(request.POST, instance=bus, edit_mode=True)
        if form.is_valid():
            form.save()
            messages.success(request, "Bus details updated successfully!")
            return redirect('it:bus')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BusForm(instance=bus, edit_mode=True)

    return render(request, 'IT/Bus/edit_bus.html', {
        'form': form,
        'edit_mode': True,
        'bus': bus
    })



@login_required
def delete_bus(request, bus_unit_num):
    bus = get_object_or_404(Bus, pk=bus_unit_num)
    bus.delete()
    messages.success(request, f"Bus {bus.bus_license_plate_number} has been deleted successfully.")
    return redirect('it:bus')  # Adjust this to redirect to the appropriate page

#_______________________________JOBORDER________________________________________
@login_required
def JO(request):
    # Get search query from request parameters
    query = request.GET.get('search')
    status_filter = request.GET.get('status')
    checked_by_filter = request.GET.get('checked_by')
    approved_by_filter = request.GET.get('approved_by')
    date_filter = request.GET.get('date')

    filters = Q()

    # Apply search filter if query exists
    if query:
        filters &= (
            Q(j_o_number__icontains=query) |  # Search by job order number
            Q(j_o_date_requested__icontains=query) |  # Search by date requested
            Q(j_o_work_description__icontains=query) |  # Search by work description
            Q(j_o_checked_by__emp_fname__icontains=query) |  # Search by checked by employee first name
            Q(j_o_checked_by__emp_lname__icontains=query) |  # Search by checked by employee last name
            Q(j_o_approved_by__emp_fname__icontains=query) |  # Search by approved by employee first name
            Q(j_o_approved_by__emp_lname__icontains=query) |  # Search by approved by employee last name
            Q(j_o_status__icontains=query) |  # Search by job order status
            Q(j_o_bus_unit_num__bus_unit_num__icontains=query)  # Search by bus unit number
        )
    
    # Apply filter by status
    if status_filter:
        filters &= Q(j_o_status=status_filter)

    # Apply filter by checked by
    if checked_by_filter:
        filters &= Q(j_o_checked_by__emp_id=checked_by_filter)

    # Apply filter by approved by
    if approved_by_filter:
        filters &= Q(j_o_approved_by__emp_id=approved_by_filter)

    # Apply filter by date
    if date_filter:
        filters &= Q(j_o_date_requested=date_filter)

    # Retrieve the filtered job orders
    requests = JobOrder.objects.filter(filters)

    # Get all employees for dropdown options
    employees = Employee.objects.all()

    # Pass the queryset and employees to the template
    return render(request, 'IT/JO/JO.html', {'requests': requests, 'employees': employees})

#____________________________________ACK_REQ______________________________________
@login_required
def AR(request):
    ar_query = Acknowledgment_Receipt.objects.all()

    # Filtering by status
    status_filter = request.GET.get('status', None)
    if status_filter:
        ar_query = ar_query.filter(ar_status__icontains=status_filter)

    # Filtering by receiver
    receiver_filter = request.GET.get('receiver', None)
    if receiver_filter:
        ar_query = ar_query.filter(ar_date_receiver_id=receiver_filter)  # Using `id` for foreign key lookup

    # Filtering by date made
    date_made_filter = request.GET.get('date_made', None)
    if date_made_filter:
        try:
            date_made = datetime.strptime(date_made_filter, '%Y-%m-%d')
            ar_query = ar_query.filter(ar_date_made=date_made)
        except ValueError:
            pass  # If invalid date, ignore filter

    # Filtering by date received
    date_received_filter = request.GET.get('date_received', None)
    if date_received_filter:
        try:
            date_received = datetime.strptime(date_received_filter, '%Y-%m-%d')
            ar_query = ar_query.filter(ar_date_received=date_received)
        except ValueError:
            pass  # If invalid date, ignore filter

    # Fetching employees from Vehicle Maintenance Department
    employees = Employee.objects.filter(dept_id__dept_name__iexact="Vehicle Maintenance Department")

    return render(request, 'IT/AR/AR.html', {'ack_req': ar_query, 'employees': employees})

#_________________________________PURCHASE_ORDER____________________________________
@login_required
def PO(request):
    return render(request, 'IT/PO/PO.html')

@login_required
def it_purchase_odr(request, po_num=None):
    if po_num:
        # View a specific purchase order
        purchase_order = get_object_or_404(Purchase_Order, po_num=po_num)
        material_orders = Material_Order.objects.filter(purchase_order=purchase_order)
        context = {
            'purchase_order': purchase_order,
            'material_orders': material_orders,
        }
        return render(request, 'IT/PO/view_purchase_odr.html', context)
    else:
        # Display all purchase orders
        purchase_orders = Purchase_Order.objects.all()
        statuses = Purchase_Order_Status.STATUS_CHOICES  # Get the status choices
        context = {
            'purchase_orders': purchase_orders,
            'statuses': statuses,  # Add statuses to context
            'selected_status': '',  # Default value for selected status
        }
        return render(request, 'IT/PO/PO.html', context)


@login_required
def filter_purchase_orders(request):
    # Get query parameters
    start_date = request.GET.get('start_date', '')  # Retrieve the date filter
    selected_status = request.GET.get('status', '')  # Retrieve the status filter

    # Base queryset for purchase orders
    purchase_orders = Purchase_Order.objects.all()

    # Apply date filter if a valid date is provided
    if start_date:
        try:
            # Try filtering by the exact date
            exact_date_orders = purchase_orders.filter(po_datemade=start_date)

            if exact_date_orders.exists():
                purchase_orders = exact_date_orders
            else:
                # Fallback: Filter by the same month and year
                date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                purchase_orders = purchase_orders.filter(
                    po_datemade__year=date_obj.year,
                    po_datemade__month=date_obj.month
                )
        except ValueError:
            pass  # Ignore invalid dates

    # Apply status filter if a valid status is provided
    if selected_status:
        purchase_orders = purchase_orders.filter(postat_id__postat_status=selected_status)

    # Prepare context for rendering
    context = {
        'purchase_orders': purchase_orders,
        'statuses': Purchase_Order_Status.STATUS_CHOICES,
        'selected_status': selected_status,
        'form': DateFilterForm(initial={'start_date': start_date}),
    }

    return render(request, 'IT/PO/PO.html', context)

#____________________________________MATERIAL______________________________________
@login_required
def materials_it(request):
    search_query = request.GET.get('search', '')  # Get the search query from the URL
    category_query = request.GET.get('category', '')  # Get the selected category from the URL

    # Start with all materials
    materials = Material.objects.all()

    # Filter by search query (material name, type, or brand)
    if search_query:
        materials = materials.filter(
            mat_name__icontains=search_query
        ) | materials.filter(
            mat_brand__icontains=search_query
        )

    # Filter by category if provided
    if category_query:
        materials = materials.filter(mat_category__mat_name=category_query)

    # Get all categories for the dropdown
    categories = Material_Category.objects.all()

    return render(
        request,
        'IT/material/material.html',  # Update this to match your app's templates
        {
            'materials': materials,
            'categories': categories,
            'selected_category': category_query,
        }
    )

#__________________________________________ACCOUNTS___________________________________
@login_required
def account(request):
    # Get the search query from the GET request
    search_query = request.GET.get('search', '')

    # Filter accounts based on the search query (case-insensitive)
    if search_query:
        accounts = Accounts.objects.filter(username__icontains=search_query)
    else:
        accounts = Accounts.objects.all()

    return render(request, 'IT/Accounts/Accounts.html', {'accounts': accounts, 'search': search_query})

@login_required
def add_account(request):
    if request.method == 'POST':
        form = AccountsForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new account (password will be hashed automatically)
            # Redirect to the same page with a success message or to a different success page
            return render(request, 'IT/Accounts/add_account.html', {
                'form': AccountsForm(),  # Reset the form for the next input
                'success': True  # Flag to indicate successful submission
            })
        else:
            return render(request, 'IT/Accounts/add_account.html', {
                'form': form,  # Return the form with validation errors
                'success': False  # Flag to indicate failure
            })
    else:
        form = AccountsForm()  # Create a blank form for GET requests

    return render(request, 'IT/Accounts/add_account.html', {
        'form': form  # Pass the form to the template
    })


@login_required
def delete_account(request, username):
    # Fetch the account using the username
    account = get_object_or_404(Accounts, username=username)

    if request.method == "POST":
        # Delete the account
        account.delete()
        # Add a success message
        messages.success(request, f'Account for {username} has been deleted successfully.')
        # Redirect to the list of accounts page
        return redirect('it:Accounts')  # Replace 'account_list' with your actual URL name for the accounts list
    
    # If the request method is GET, display the confirmation page
    return render(request, 'IT/Accounts/Accounts.html', {'account': account})

@login_required
def edit_account(request, username):
    account = get_object_or_404(Accounts, username=username)  # Get the account using the username
    
    if request.method == 'POST':
        form = AccountsForm(request.POST, instance=account, current_user_id=account.user_id_id)  # Pass the current user_id
        if form.is_valid():
            form.save()  # Save the changes
            messages.success(request, f"Account '{username}' updated successfully!")
            return redirect('it:Accounts')  # Redirect back to the accounts list
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AccountsForm(instance=account, current_user_id=account.user_id_id)  # Prepopulate the form with the account's data

    # Fetch the employee name for display
    employee_name = account.user_id.emp_fname if account.user_id else "Unknown Employee"

    return render(request, 'IT/Accounts/edit_account.html', {
        'form': form,
        'account': account,
        'employee_name': employee_name,
    })

#________________________________LOGOUT__________________________________________________
@login_required
def logout_view(request):
    # Clear the session (log out the user)
    logout(request)
    request.session.flush()  # Extra precaution to clear all session data
    return redirect('login:login')  # Redirect to login page