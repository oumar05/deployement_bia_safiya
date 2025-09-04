from django.urls import path
from . import views

app_name = 'admin_interface'

urlpatterns = [
    path('admin-panel/login/', views.admin_login, name='admin_login'),
    path('admin-panel/logout/', views.admin_logout, name='admin_logout'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/users/', views.users_management, name='users_management'),
    path('admin-panel/posts/', views.posts_management, name='posts_management'),
    path('admin-panel/chat-analytics/', views.chat_analytics, name='chat_analytics'),
    path('admin-panel/api/stats/', views.real_time_stats, name='real_time_stats'),
    path('admin-panel/api/toggle-user/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('admin-panel/api/post-details/<int:post_id>/', views.post_details, name='post_details'),
    path('admin-panel/api/delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
]
