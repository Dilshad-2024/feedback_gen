from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("", views.register, name="register"),
    path("login/", views.login_page,name="login"),
    path("logout/", views.logout_page,name="logout"),
    path('dashboard/', views.dashboard, name='dashboard')
]