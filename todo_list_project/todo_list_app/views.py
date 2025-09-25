from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Count
from .forms import RegisterForm, LoginForm, AddListForm, AddListItemForm
from django.contrib.auth.decorators import login_required
from .models import ListItem, ToDoList
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404

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
        register_form = RegisterForm()
        
    context = {'form': register_form}
    return render(request, template_name='todo_list_app/register.html', context=context)

# Dashboard Page View 
@login_required
def dashboard_view(request, list_id=None, task_id=None):
    """
    Brief: A view method that handles the dashboard view.

    Details: This function handles the addition of a new list to a user within the DB,
             handles the selection of a list from the side-bar, handles the deletion 
             of a selected list from the DB and handles the addition, deletion and toggeling
             of a selected list item within the list.  
             This view function is restricted to only accept HTTP request POST. 
    
    Args:
        request: The received request.
        list_id: Id of the selected/current list, initially is none.
    """ 
    # All the lists owned by the logged in user 
    lists = ToDoList.objects.filter(user=request.user).annotate(list_items_count=Count('listitem'))

    # Context for the view 
    context = {
        'lists': lists, 
        'add_list_form': None,
        'add_list_item_form': None, 
        'current_list': None,
        'task': None,
    }

    # Handle the addition and the deletion of the list items 
    if request.method == "POST": 
       form_type = request.POST.get('form_type')
       if form_type == 'add_list':
          # Create an object from the Form
          add_list_form = AddListForm(request.POST)
          if add_list_form.is_valid():
                added_list_name = add_list_form.cleaned_data.get('list_name')
                ToDoList.objects.create(name = added_list_name, user= request.user)
                context['add_list_form'] =  add_list_form
                messages.success(request, 'New list added successfully!')
                return redirect('dashboard')
       elif form_type == 'delete_list':
            if list_id: 
                current_list = get_object_or_404(ToDoList, id=list_id, user= request.user) 
                context['current_list'] = current_list
                current_list.delete()
                context['current_list'] = None
                messages.success(request, 'Selected list deleted successfully!')
                return redirect('dashboard')
       elif form_type == 'add_list_item':
            add_list_item_form = AddListItemForm(request.POST)
            if add_list_item_form.is_valid():
                    list_item_text =  add_list_item_form.cleaned_data.get('list_item_text')
                    if list_id:
                        current_list = get_object_or_404(ToDoList, id=list_id, user= request.user) 
                        context['current_list'] = current_list
                        context['add_list_item_form'] = add_list_item_form
                        ListItem.objects.create(list = current_list, text=list_item_text )
                        messages.success(request, 'New list item added successfully!')
                        return redirect('view_list_items', list_id = list_id)
       elif form_type == 'delete_task':
            if list_id and task_id: 
                current_list = get_object_or_404(ToDoList, id=list_id, user= request.user) 
                task = get_object_or_404(ListItem, id=task_id, list=current_list)
                task.delete()
                messages.success(request, 'Selected list deleted successfully!')
                return redirect('view_list_items', list_id = list_id)
       elif form_type == 'toggle_task':
            if list_id and task_id: 
                current_list = get_object_or_404(ToDoList, id=list_id, user= request.user) 
                task = get_object_or_404(ListItem, id=task_id, list=current_list)
                task.isCompleted = not task.isCompleted
                task.save()
                return redirect('view_list_items', list_id = list_id)

    else: 
        add_list_form = AddListForm()
        add_list_item_form = AddListItemForm()  

    # Handle the selection of a list from the side-bar
    # If a list_id is provided in the URL, fetch the corresponding list and its items
    if list_id:
        current_list = get_object_or_404(ToDoList, id=list_id, user=request.user)
        context['current_list'] = current_list

    # Handle the selection of a list item from the selected list view.
    # If a task_id is provided in the URL, fetch the corresponding list and its items
    if task_id and list_id: 
        task = get_object_or_404(ListItem, id=task_id, list=current_list)
        context['task'] = task

    return render(request, template_name='todo_list_app/dashboard.html', context=context)     