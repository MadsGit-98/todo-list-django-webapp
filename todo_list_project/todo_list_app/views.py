from django.contrib.auth import authenticate, login
from django.http import request
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

# Create your views here.

# Home Page View 
def home_view(request):
    return render(request, template_name='todo_list_app/home.html')

# Login Page View 
def login_view(request):
    return render(request, template_name='todo_list_app/login.html')

# Register Page View 
def register_view(request):
    """
    Brief: A view method that handles the register form.

    Details: If the form from the POST request is valid it is registered in the 
             DB and the user is directed to his dashboard. 
    
    Args:
        request: The received request.
    """    
    if request.method == "POST": 
        form = RegisterForm(request.POST)
        if form.is_valid():

            # After the form has been validated we can use the cleaned data 
            registered_user_name = form.cleaned_data.get('username') 
            registered_email = form.cleaned_data.get('email') 
            registered_password = form.cleaned_data.get('password')

            # Create a new user in the DB 
            registered_user = User.objects.create_user(registered_user_name, registered_email, registered_password)
            
            # Login the created user 
            login(request, user=registered_user)

            # Redirect to the dashboard view to start creating To-Do Lists.
            return redirect('dashboard')
    else: 
        form = RegisterForm()
        
    context = {'form': form}
    return render(request, template_name='todo_list_app/register.html', context=context)

# Dashboard Page View 
def dashboard_view(request):
    return render(request, template_name='todo_list_app/dashboard.html')