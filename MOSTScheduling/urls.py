"""visitMakerWoogity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from scheduling import views

urlpatterns = [
    #### NAV BAR ####
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('admin/', admin.site.urls, name='admin'),
    path('scheduling/', include('scheduling.urls'), name='scheduling'),

    #### REQUESTS ####
    # request/entry
    path('request/entry', views.RequestCreate.as_view(), name='req_entry'),
    # request/confirm
    path('request/confirm', views.request_confirm, name='req_confirm'),

    #### Login/Logout ####
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    ]

