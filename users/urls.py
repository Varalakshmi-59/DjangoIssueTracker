from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile-update'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.user_list, name='user-list'),
    path('users/<str:username>/', views.user_detail, name='user-detail'),
    path('change-password/', views.change_password, name='change-password'),
    path('logout/', views.custom_logout, name='logout'),
]