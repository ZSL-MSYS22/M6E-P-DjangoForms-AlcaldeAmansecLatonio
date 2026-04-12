# Johann Miguel S. Alcalde, 240150 ; Samantha Louise F. Amansec, 230286 ; Zale Sebastian S. Latonio, 242494
'''
We hereby attest to the truth of the following facts:

We have not discussed the Python code in our program with anyone
other than my instructor or the teaching assistants assigned to this course.

We have not used Python code obtained from another student, or
any other unauthorized source, whether modified or unmodified.

If any Python code or documentation used in our program was
obtained from another source, it has been clearly noted with citations in the
comments of our program.
'''

"""
URL configuration for MyInventorySystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('view_suppliers/', views.view_suppliers, name='view_suppliers'),
    path('view_bottles/', views.view_bottles, name='view_bottles'),
    path('add_bottle/', views.add_bottle, name='add_bottle'),
    path('view_bottle_details/<int:pk>/', views.view_bottle_details, name='view_bottle_details'),
    path('delete_bottle/<int:pk>/', views.delete_bottle, name='delete_bottle'),
    path('manage_account/<int:pk>/', views.manage_account, name='manage_account'),
    path('change_password/<int:pk>/', views.change_password, name='change_password'),
    path('delete_account/<int:pk>/', views.delete_account, name='delete_account'),
    path('logout/', views.logout_view, name='logout'),
]