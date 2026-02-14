from django.contrib import admin
from .models import Student, Room, Announcement, Attendance

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'user', 'gender', 'phone_number', 'room')
    search_fields = ('roll_number', 'user__username', 'user__first_name', 'user__last_name')
    list_filter = ('gender', 'room')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'capacity', 'is_available')
    search_fields = ('room_number',)
    list_filter = ('room_type', 'is_available')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'posted_by')
    search_fields = ('title', 'content')
    list_filter = ('date_posted',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'is_present')
    search_fields = ('student__roll_number', 'student__user__username')
    list_filter = ('date', 'is_present')
