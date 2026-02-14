from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='hostel/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Room URLs
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/assign/', views.room_assignment, name='room_assignment'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    
    # Announcement URLs
    path('announcements/', views.announcement_list, name='announcement_list'),
    path('announcements/create/', views.announcement_create, name='announcement_create'),
    
    # Attendance URLs
    path('attendance/mark/', views.attendance_mark, name='attendance_mark'),
    path('attendance/bulk/', views.attendance_bulk, name='attendance_bulk'),
    
    # Admin User Management URLs - changed to avoid conflict with Django admin
    path('manage/users/', views.admin_user_list, name='admin_user_list'),
    path('manage/users/create/', views.admin_create_user, name='admin_create_user'),

    # Admin Room Management URLs
    path('manage/rooms/', views.admin_room_list, name='admin_room_list'),
    path('manage/rooms/create/', views.admin_room_create, name='admin_room_create'),
    path('manage/rooms/edit/<int:room_id>/', views.admin_room_create, name='admin_room_edit'),

    # Admin Attendance Management URL
    path('manage/attendance/', views.admin_attendance_list, name='admin_attendance_list'),

    # Admin Announcement Management URL
    path('manage/announcements/', views.admin_announcement_list, name='admin_announcement_list'),
] 