"""worktracker URL Configuration

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
from django.contrib import admin
from django.urls import path

from tracker import views

urlpatterns = [

    path('explain', views.explain, name='explain'),

    path('all_task_data', views.all_task_data, name='all_task_data'),
    path('all_people_data', views.all_people_data, name='all_people_data'),
    path('all_fund_data', views.all_fund_data, name='all_fund_data'),
    path('all_project_data', views.all_project_data, name='all_project_data'),

    path('admin/', admin.site.urls),
]
