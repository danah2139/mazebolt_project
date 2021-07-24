"""mazebolt_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("", views.instance, name='instance'),
    path('admin/', admin.site.urls),
    path('create_test/', views.create_test, name='create_test'),
    path('terminate_instance/',views.terminate_instance, name='terminate_instance'),
    path('tests/', views.test, name='test'),
    path('stop_test_checked/',views.stop_test_checked, name='stop_test_checked'),

]
