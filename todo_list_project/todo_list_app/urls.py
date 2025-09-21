from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('', views.login_view, name="login"),
    path('', views.register_view, name="register"),
    path('', views.dashboard_view, name="dashboard"),
]