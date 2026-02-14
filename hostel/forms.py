from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Room, Announcement, Attendance

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_number', 'phone_number', 'gender']

class RoomAssignmentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['room']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show available rooms
        self.fields['room'].queryset = Room.objects.filter(is_available=True)

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'is_present']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class BulkAttendanceForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class AdminCreateUserForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    roll_number = forms.CharField(max_length=20, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    gender = forms.ChoiceField(choices=Student.GENDER_CHOICES, required=True)
    room = forms.ModelChoiceField(queryset=Room.objects.filter(is_available=True), required=False)
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username
    
    def clean_roll_number(self):
        roll_number = self.cleaned_data.get('roll_number')
        if Student.objects.filter(roll_number=roll_number).exists():
            raise forms.ValidationError("Roll number already exists")
        return roll_number
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords don't match")
        
        return cleaned_data
    
    def save(self):
        data = self.cleaned_data
        # Create the user
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_staff=False,
        )
        
        # Create the student profile
        student = Student.objects.create(
            user=user,
            roll_number=data['roll_number'],
            phone_number=data['phone_number'],
            gender=data['gender'],
            room=data.get('room')  # May be None
        )
        
        # Update room availability if assigned
        if data.get('room'):
            room = data['room']
            room.is_available = False
            room.save()
            
        return student 

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'capacity', 'is_available']
        
    def clean_room_number(self):
        room_number = self.cleaned_data.get('room_number')
        # Check if room number already exists when creating a new room
        if not self.instance.pk and Room.objects.filter(room_number=room_number).exists():
            raise forms.ValidationError("Room with this number already exists.")
        return room_number 