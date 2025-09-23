from django.contrib.auth import login
from django.db.models import Count
from django.http import request
from .forms import RegisterForm, LoginForm, AddListForm
from .models import ListItem, ToDoList
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

# Create your views here.

# Home Page View 
def home_view(request):
    return render(request, template_name='todo_list_app/home.html')

# Login Page View 
def login_view(request):
    """
    Brief: A view method that handles the login form.

    Details: If the form from the POST request is valid the user is logged in and
             re-directed to his dashboard. 
    
    Args:
        request: The received request.
    """   
    if request.method == "POST":
         login_form = LoginForm(request.POST)
         if login_form.is_valid():

            login_user = login_form.user
            login(request, login_user)

            return redirect('dashboard')
    else:
        login_form = LoginForm()

    context = {'form': login_form}
    return render(request, template_name='todo_list_app/login.html', context=context)

# Register Page View 
def register_view(request):
    """
    Brief: A view method that handles the register form.

    Details: If the form from the POST request is valid it is registered in the 
             DB and the user is re-directed to his dashboard. 
    
    Args:
        request: The received request.
    """    
    if request.method == "POST": 
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():

            # After the form has been validated we can use the cleaned data 
            registered_user_name = register_form.cleaned_data.get('username') 
            registered_email = register_form.cleaned_data.get('email') 
            registered_password = register_form.cleaned_data.get('password')

            # Create a new user in the DB 
            registered_user = User.objects.create_user(registered_user_name, registered_email, registered_password)
            
            # Login the created user 
            login(request, user=registered_user)

            # Redirect to the dashboard view to start creating To-Do Lists.
            return redirect('dashboard')
    else: 
        form = RegisterForm()
        
    context = {'form': register_form}
    return render(request, template_name='todo_list_app/register.html', context=context)

# Dashboard Page View 
def dashboard_view(request):
    """
    Brief: A view method that handles the dashboard view.

    Details: This function handles the addition of a new list to a user within the DB,

    
    Args:
        request: The received request.
    """ 
    # Handle the Add new List form 
    if request.method == "POST": 
        add_list_form = AddListForm(request.POST)
        if add_list_form.is_valid():
            if request.user.is_authenticated: 
                added_list_name = add_list_form.cleaned_data.get("list_name")
                ToDoList.objects.create(name= added_list_name, user=request.user)
                return redirect('dashboard')
            else:
                return redirect('login') 
    else:
        add_list_form = AddListForm() 

    # Viewing all the current lists of a user 
    lists = ToDoList.objects.filter(user= request.user).annotate(list_items_count=Count('listitem'))

    context= {
        'add_list_form': add_list_form, 
        'lists': lists
        }
    return render(request, template_name='todo_list_app/dashboard.html', context=context)