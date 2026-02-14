from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from .models import Student, Room, Announcement, Attendance
from .forms import (
    UserRegistrationForm, StudentProfileForm, RoomAssignmentForm,
    AnnouncementForm, AttendanceForm, BulkAttendanceForm, AdminCreateUserForm,
    RoomForm
)

def home(request):
    """Landing page view"""
    return render(request, 'hostel/home.html')

def register(request):
    """User registration view"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = StudentProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        user_form = UserRegistrationForm()
        profile_form = StudentProfileForm()
    
    return render(request, 'hostel/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def dashboard(request):
    """User dashboard view"""
    # For admin users, show admin dashboard
    if request.user.is_staff:
        # Get counts for admin dashboard
        student_count = Student.objects.count()
        room_count = Room.objects.count()
        available_rooms = Room.objects.filter(is_available=True).count()
        announcement_count = Announcement.objects.count()
        
        # Get latest announcements
        announcements = Announcement.objects.all()[:5]
        
        # Get recent attendance records
        recent_attendance = Attendance.objects.order_by('-date')[:10]
        
        return render(request, 'hostel/admin_dashboard.html', {
            'student_count': student_count,
            'room_count': room_count,
            'available_rooms': available_rooms,
            'announcement_count': announcement_count,
            'announcements': announcements,
            'recent_attendance': recent_attendance
        })
    
    # For regular users, show student dashboard
    try:
        student = request.user.student
        room = student.room
        attendance = Attendance.objects.filter(student=student).order_by('-date')[:5]
    except Student.DoesNotExist:
        student = None
        room = None
        attendance = None
        messages.warning(request, 'Please complete your student profile.')
        return redirect('profile')
    
    announcements = Announcement.objects.all()[:5]
    
    return render(request, 'hostel/dashboard.html', {
        'student': student,
        'room': room,
        'attendance': attendance,
        'announcements': announcements
    })

@login_required
def room_list(request):
    """View all rooms"""
    rooms = Room.objects.all()
    return render(request, 'hostel/room_list.html', {'rooms': rooms})

@login_required
def room_detail(request, room_id):
    """View room details"""
    room = get_object_or_404(Room, id=room_id)
    students = Student.objects.filter(room=room)
    return render(request, 'hostel/room_detail.html', {
        'room': room,
        'students': students
    })

@login_required
def room_assignment(request):
    """Assign room to student"""
    # Admin users should use the admin interface for room assignments
    if request.user.is_staff:
        messages.info(request, 'Admin users should manage room assignments through the admin panel.')
        return redirect('admin:hostel_student_changelist')
        
    # For regular users
    try:
        student = Student.objects.get(user=request.user)
        
        if request.method == 'POST':
            form = RoomAssignmentForm(request.POST, instance=student)
            if form.is_valid():
                # Update old room availability if exists
                if student.room:
                    old_room = student.room
                    old_room.is_available = True
                    old_room.save()
                
                # Save new room assignment
                new_student = form.save(commit=False)
                new_room = new_student.room
                if new_room:
                    new_room.is_available = False
                    new_room.save()
                new_student.save()
                
                messages.success(request, 'Room assigned successfully!')
                return redirect('dashboard')
        else:
            form = RoomAssignmentForm(instance=student)
        
        return render(request, 'hostel/room_assignment.html', {'form': form})
    except Student.DoesNotExist:
        messages.warning(request, 'Please complete your student profile first.')
        return redirect('profile')

@login_required
def announcement_list(request):
    """View all announcements"""
    announcements = Announcement.objects.all()
    return render(request, 'hostel/announcement_list.html', {'announcements': announcements})

@login_required
def announcement_create(request):
    """Create new announcement"""
    if not request.user.is_staff:
        messages.error(request, 'Only administrators can create announcements.')
        return redirect('announcement_list')
        
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.posted_by = request.user
            announcement.save()
            messages.success(request, 'Announcement created successfully!')
            return redirect('announcement_list')
    else:
        form = AnnouncementForm()
    
    return render(request, 'hostel/announcement_form.html', {'form': form})

@login_required
def attendance_mark(request):
    """Mark attendance for a student"""
    if not request.user.is_staff:
        messages.error(request, 'Only administrators can mark attendance.')
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save()
            messages.success(request, 'Attendance marked successfully!')
            return redirect('dashboard')
    else:
        form = AttendanceForm()
    
    return render(request, 'hostel/attendance_form.html', {'form': form})

@login_required
def attendance_bulk(request):
    """Mark attendance for multiple students"""
    if not request.user.is_staff:
        messages.error(request, 'Only administrators can mark bulk attendance.')
        return redirect('dashboard')
    
    # Get all students - moved outside the if/else block to ensure it's always defined
    students = Student.objects.all()
        
    if request.method == 'POST':
        form = BulkAttendanceForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            
            for student in students:
                student_present = request.POST.get(f'student_{student.id}') == 'on'
                attendance, created = Attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={'is_present': student_present}
                )
            
            messages.success(request, 'Bulk attendance marked successfully!')
            return redirect('dashboard')
    else:
        form = BulkAttendanceForm()
    
    return render(request, 'hostel/attendance_bulk.html', {
        'form': form,
        'students': students
    })

@login_required
def profile(request):
    """View and edit user profile"""
    # For admin users, redirect to admin profile or Django admin
    if request.user.is_staff:
        messages.info(request, 'Admin users can manage their profile in the admin panel.')
        return redirect('admin:index')
        
    # For regular users, show/edit student profile
    try:
        student = get_object_or_404(Student, user=request.user)
        
        if request.method == 'POST':
            form = StudentProfileForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('dashboard')
        else:
            form = StudentProfileForm(instance=student)
        
        return render(request, 'hostel/profile.html', {'form': form})
    except Exception as e:
        # Create a new student profile if it doesn't exist
        if request.method == 'POST':
            form = StudentProfileForm(request.POST)
            if form.is_valid():
                student = form.save(commit=False)
                student.user = request.user
                student.save()
                messages.success(request, 'Profile created successfully!')
                return redirect('dashboard')
        else:
            form = StudentProfileForm()
        
        return render(request, 'hostel/profile.html', {'form': form, 'new_profile': True})

@login_required
def admin_create_user(request):
    """Admin view to create new student users"""
    if not request.user.is_staff:
        messages.error(request, 'Only administrators can create new users.')
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = AdminCreateUserForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student {student.user.username} created successfully!')
            return redirect('admin_user_list')
    else:
        form = AdminCreateUserForm()
    
    return render(request, 'hostel/admin_create_user.html', {'form': form})

@login_required
def admin_user_list(request):
    """Admin view to list all users"""
    if not request.user.is_staff:
        messages.error(request, 'Only administrators can view user list.')
        return redirect('dashboard')
        
    students = Student.objects.all().select_related('user', 'room')
    
    return render(request, 'hostel/admin_user_list.html', {'students': students})

@login_required
def admin_room_list(request):
    """Admin view to list all rooms"""
    if not request.user.is_staff:
        messages.error(request, 'Only administrators can view room list.')
        return redirect('dashboard')
        
    rooms = Room.objects.all()
    
    return render(request, 'hostel/admin_room_list.html', {'rooms': rooms})

@login_required
def admin_room_create(request, room_id=None):
    """Admin view to create or edit a room"""
    if not request.user.is_staff:
        messages.error(request, 'Only administrators can create/edit rooms.')
        return redirect('dashboard')
    
    # If room_id is provided, we're editing an existing room
    if room_id:
        room = get_object_or_404(Room, id=room_id)
        title = "Edit Room"
    else:
        room = None
        title = "Create New Room"
        
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, f'Room {"updated" if room else "created"} successfully!')
            return redirect('admin_room_list')
    else:
        form = RoomForm(instance=room)
    
    return render(request, 'hostel/admin_room_form.html', {
        'form': form,
        'title': title,
        'is_edit': room is not None
    })

@login_required
def admin_attendance_list(request):
    """Admin view to list all attendance records"""
    if not request.user.is_staff:
        messages.error(request, 'Only administrators can view attendance records.')
        return redirect('dashboard')
        
    attendance_records = Attendance.objects.all().select_related('student', 'student__user', 'student__room').order_by('-date')
    
    return render(request, 'hostel/admin_attendance_list.html', {'attendance_records': attendance_records})

@login_required
def admin_announcement_list(request):
    """Admin view to list all announcements with management options"""
    if not request.user.is_staff:
        messages.error(request, 'Only administrators can manage announcements.')
        return redirect('dashboard')
        
    announcements = Announcement.objects.all().select_related('posted_by')
    
    return render(request, 'hostel/admin_announcement_list.html', {'announcements': announcements})
