from django.urls import path
from .views import signup, login_view, logout_view,generuj_opis

urlpatterns = [
    path('',generuj_opis,name='generuj-opis'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

]