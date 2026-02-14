from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Room(models.Model):
    ROOM_TYPES = (
        ('S', 'Single'),
        ('D', 'Double'),
        ('T', 'Triple'),
    )
    
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=1, choices=ROOM_TYPES)
    capacity = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Room {self.room_number} ({self.get_room_type_display()})"

class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.roll_number})"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date_posted']

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    is_present = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student.user.first_name} - {self.date} - {'Present' if self.is_present else 'Absent'}"
    
    class Meta:
        unique_together = ['student', 'date']
