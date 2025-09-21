from django.shortcuts import render

# Create your views here.

# Home Page View 
def home_view(request):
    return render(request, template_name='todo_list_app/home.html')