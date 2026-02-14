# Hostel Management System

A comprehensive Django application for managing hostel operations including user authentication, room assignments, announcements, and attendance tracking.

## Features

- User registration and authentication
- Student profile management
- Room assignment and management
- Announcements system
- Attendance tracking
- Responsive UI with Bootstrap 5

## Installation

1. Clone the repository:
```
git clone https://github.com/hajrahk/hostel-management.git
cd hostel-management
```

2. Install dependencies:
```
pip install django django-bootstrap5
```

3. Run migrations:
```
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser:
```
python manage.py createsuperuser
```

5. Run the development server:
```
python manage.py runserver
```

6. Access the application at `http://127.0.0.1:8000/`

## Default Admin Credentials

- Username: hajra
- Password: msa123

## Usage

### Admin Tasks

1. Log in as admin at `/admin`
2. Create rooms for the hostel
3. Manage student accounts
4. Post announcements
5. View and manage attendance records

### Student Tasks

1. Register for an account
2. Request room assignment
3. View announcements
4. Check attendance records
5. Update profile information

## Project Structure

- `hostel/` - Main application directory
  - `models.py` - Database models
  - `views.py` - View functions
  - `urls.py` - URL routing
  - `forms.py` - Form definitions
  - `admin.py` - Admin interface configuration
- `templates/` - HTML templates
  - `base.html` - Base template with common structure
  - `hostel/` - App-specific templates
- `static/` - Static files (CSS, JS)

## License

This project is licensed under the MIT License. 