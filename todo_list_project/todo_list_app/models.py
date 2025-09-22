from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# To-Do List Model
class ToDoList(models.Model): 
    """ Represents a To-Do list with name, and user
    
    Attributes: 
        user(ForeignKey): The user that owns the To-Do List.  [1:* Relationship, a user can have multiple To-Do Lists]
        name(CharField): The name of the To-Do List that the user has specified, with a maximum length of 64 characters.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)

# List Items Class
class ListItem(models.Model):
    """ Represents a List Item with a containing list, text and status
    
    Attributes: 
        list(ForeignKey): The ToDo list that this item lies in.  [1:* Relationship, a ToDo List can have multiple ListItems]
        text(CharField): Description of a task or a To-Do list item, with a maximum length of 100 characters.
        isCompleted(BooleanField): Whether the task is completed or not.
    """
    list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    isCompleted = models.BooleanField(default=False)

