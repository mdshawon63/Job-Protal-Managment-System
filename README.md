# JobSphere

JobSphere is a modern Job Portal and Recruitment Management System built with Django and Django REST Framework.

The platform connects candidates and recruiters through a secure recruitment workflow where candidates can discover jobs, submit applications, track application status, receive notifications, and attend scheduled interviews. Recruiters can manage companies, publish jobs, review applications, update candidate status, schedule interviews, and monitor recruitment analytics.

---

## Project Overview

JobSphere provides a complete recruitment management workflow with role-based access control and JWT authentication.

The system supports three user roles:

- Candidate
- Recruiter
- Admin

Candidates can search and apply for jobs, while recruiters can manage job postings and applications.

Administrators can manage companies and verification-related operations.

---

## Features

### Authentication

- User registration
- JWT authentication
- Access token
- Refresh token
- Role-based authentication
- Candidate authentication
- Recruiter authentication
- Admin authentication
- Protected API endpoints
- Secure password hashing

### Candidate Features

- Candidate registration
- Candidate profile
- Resume upload
- Profile picture upload
- Job search
- Job filtering
- Salary filtering
- Job sorting
- Job bookmarking
- Job application
- Cover letter submission
- Application tracking
- Interview tracking
- Notification system
- Candidate dashboard

### Recruiter Features

- Recruiter registration
- Recruiter profile
- Company management
- Job creation
- Job updating
- Job publishing
- Job closing
- Application management
- Candidate status management
- Interview scheduling
- Interview management
- Recruitment analytics
- Recruiter dashboard

### Admin Features

- Admin authentication
- Company verification
- Company management
- Job management
- Application management
- Interview management
- Platform administration

### Security Features

- JWT authentication
- Role-based permissions
- Object-level ownership validation
- Resume file type validation
- Resume file size validation
- Profile picture validation
- Duplicate application prevention
- Application deadline validation
- Protected recruiter endpoints
- Protected candidate endpoints
- Environment variable configuration

### Notification System

The system automatically creates notifications for important recruitment events.

Examples:

- New job application
- Application status update
- Interview scheduled
- Interview cancelled
- System notifications

---

## Technology Stack

### Backend

- Python
- Django
- Django REST Framework
- Simple JWT
- PostgreSQL

### Frontend

- HTML5
- CSS3
- JavaScript

### API Documentation

- OpenAPI
- Swagger UI
- ReDoc

### Development Tools

- Git
- GitHub
- VS Code
- Postman

---

## Project Architecture

```text
JobSphere
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── token_serializers.py
│   ├── token_views.py
│   ├── views.py
│   └── urls.py
│
├── companies/
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views.py
│   └── urls.py
│
├── jobs/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── applications/
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views.py
│   └── urls.py
│
├── notifications/
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── views.py
│   └── urls.py
│
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   ├── auth/
│   ├── candidate/
│   ├── recruiter/
│   ├── jobs/
│   └── notifications/
│
├── static/
│   ├── css/
│   └── js/
│
├── media/
│
├── manage.py
├── requirements.txt
├── .env
└── README.md