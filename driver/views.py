from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from shared.models import JobOrder  # Ensure this import points to the correct model location
from .forms import JobOrderForm
from django.contrib.auth import logout

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login:login')  # Redirect to login page if not logged in
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def driver_request(request):
    try:
        query = request.GET.get('search')  # Get search query from request parameters

        if query:
            # Filter job orders by date containing the search query
            requests = JobOrder.objects.filter(j_o_date_requested__icontains=query)
        else:
            # Retrieve all job orders if no search query
            requests = JobOrder.objects.all()

        #passes the query set and readonly flag to the template
        form = JobOrderForm(initial={'readonly':True})

        # Pass the queryset to the template
        return render(request, 'driver/driver.html', {'requests': requests, 'form': form})

    except Exception as e:
        messages.error(request, f"An error occured: {str(e)}")
        return render(request, 'driver/driver.html',{'requests': [], 'form': None})

@login_required
def add_request(request):
    if request.method == 'POST':
        form = JobOrderForm(request.POST)
        if form.is_valid():
            # Save form (status defaults to 'Pending' automatically)
            form.save()
            messages.success(request, 'Job request added successfully.')
            return redirect('driver:driver_request')
        else:
            messages.error(request, f"Error adding job request: {form.errors}")
    else:
        form = JobOrderForm()
    return render(request, 'driver/add_request.html', {'form': form})


@login_required
def logout_view(request):
    # Clear the session (log out the user)
    logout(request)
    request.session.flush()  # Extra precaution to clear all session data
    return redirect('login:login')  # Redirect to login page


