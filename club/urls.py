from django.urls import path
from club import views

app_name = 'club'
LOGIN_URL = 'club:login'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('search/', views.search, name='search'),
    path('logout/', views.user_logout, name='logout'),
    path('create_club/', views.createClub, name='create_club'),
    path('view_club/<int:club_id>/', views.viewClub, name='view_club'),
    path('contact/', views.contact, name='contact'),
    path('evaluate_club/<int:club_id>/', views.evaluateClub, name='evaluate_club'),
    path('like_or_dislike_club/', views.likeordislikeClub, name='like_or_dislike_club'),
    path('manage_club/<int:club_id>/', views.manageClub, name='manage_club'),
    path('deal_approval/', views.dealApproval, name='deal_approval'),
    path('myclublist/', views.myclublist, name='myclublist'),
    path('join_club/', views.joinClub, name='join_club'),
    path('remove_member/', views.removeMember, name='remove_member'),
]