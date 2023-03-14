from django.urls import path
from club import views

app_name = 'club'
LOGIN_URL = 'club:login'

urlpatterns = [
    path('', views.index, name='index'),
    path('myclub/', views.myClub, name='myclub'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('search/', views.search, name='search'),
    path('logout/',views.user_logout, name='logout'),
]