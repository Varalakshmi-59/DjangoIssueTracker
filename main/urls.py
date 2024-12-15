from django.urls import path
from . import views
from .api import (
    ProjectListAPIView,
    ProjectDetailAPIView,
    UserListAPIView,
    UserDetailAPIView,
)


app_name = 'main'

urlpatterns = [
    # Dashboard
    path('', views.home, name='dashboard'),
    
    # Project URLs
    path('projects/', views.project_list, name='project-list'),
    path('projects/create/', views.project_create, name='project-create'),
    path('projects/<int:pk>/', views.project_detail, name='project-detail'),
    path('projects/<int:pk>/update/', views.project_update, name='project-edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project-delete'),
    
    # Issue URLs
    path('issues/', views.issue_list, name='issue-list'),
    path('issues/create/', views.issue_create, name='issue-create'),
    path('projects/<int:project_pk>/issues/create/', 
         views.issue_create, name='project-issue-create'),
    path('issues/<int:pk>/', views.issue_detail, name='issue-detail'),
    path('issues/<int:pk>/update/', views.issue_update, name='issue-edit'),
    path('issues/<int:pk>/comment/', views.add_issue_comment, name='issue-comment'),
    path('issues/<int:pk>/delete/', views.issue_delete, name='issue-delete'),
    
    # Comment URLs
    path('comments/<int:pk>/delete/', 
         views.delete_comment, name='comment-delete'),
]


urlpatterns += [
    path('api/projects/', ProjectListAPIView.as_view(), name='project-list'),
    path('api/projects/<int:project_id>/', ProjectDetailAPIView.as_view(), name='project-detail'),
    path('api/users/', UserListAPIView.as_view(), name='user-list'),
    path('api/users/<int:user_id>/', UserDetailAPIView.as_view(), name='user-detail'),
]