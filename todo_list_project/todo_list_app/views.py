from django.http import request
from django.shortcuts import render

# Create your views here.

# Home Page View 
def home_view(request):
    return render(request, template_name='todo_list_app/home.html')

# Login Page View 
def login_view(request):
    return render(request, template_name='todo_list_app/login.html')

# Register Page View 
def register_view(request):
    return render(request, template_name='todo_list_app/register.html')

# Dashboard Page View 
def dashboard_view(request):
    return render(request, template_name='todo_list_app/dashboard.html')