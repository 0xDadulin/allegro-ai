# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('opisy/', views.opis_list, name='opis_list'),
    path('opisy/<int:opis_id>/', views.opis_detail, name='opis_detail'),
    path('opisy/update/<int:opis_id>/', views.opis_update, name='opis_update'),
]