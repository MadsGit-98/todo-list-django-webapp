from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('dashboard/<int:list_id>/', views.dashboard_view, name="view_list_items"),
    path('dashboard/<int:list_id>/', views.dashboard_view, name="delete_list"),
]