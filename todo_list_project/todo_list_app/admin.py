from django.contrib import admin
from .models import ToDoList, ListItem, User

# Register your models here.
admin.site.register(ToDoList)
admin.site.register(ListItem)
