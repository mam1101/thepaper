"""thepaper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from paper import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'new/$', views.create_new_paper, name='create-new-paper'),
    path(r'paper/<slug:slug>/', views.view_paper, name='view-paper'),
    path(r'new/submit/', views.submit_paper, name='submit-paper'),
    path(r'api/random/', views.get_random_paper, name='random-paper'),
    path(r'api/frontpage/', views.get_front_page, name='frontpage-paper'),
    path(r'api/frontpage/page/', views.get_page, name='frontpage-page-paper'),
]
