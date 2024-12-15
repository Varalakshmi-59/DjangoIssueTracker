Software Project Issue Tracker

Project Documentation

Overview

The Software Project Issue Tracker is a Django-based web application designed to facilitate efficient issue tracking and management. It supports multiple user roles, including Administrator, Project Manager, Developer, and Client/User, each with specific permissions and responsibilities. The application features a robust API for integration and extensibility.

Table of Contents

Comprehensive Installation and Setup Instructions

Prerequisites

Installation Steps

Deployment Instructions

User Manual

Administrator Role

Project Manager Role

Developer Role

Client/User Role

General Features

Best Practices

API Documentation

Projects Endpoints

Tasks Endpoints

Users Endpoints

Authentication

Response Format

Installation and Setup

Prerequisites

Ensure your system meets the following requirements:

Python: Version 3.8 or higher

PostgreSQL: Version 12 or higher

Git: For cloning the repository

Virtual Environment Tool: venv or virtualenv

Node.js (Optional): For projects with custom JavaScript frontends (e.g., React or Vue.js)

Installation Steps

Step 1: Clone the Repository

# Navigate to the desired directory
cd /path/to/your/directory

# Clone the repository
git clone git@github.com:Varalakshmi-59/DjangoIssueTracker.git
cd DjangoIssueTracker

Step 2: Create a Virtual Environment

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

Step 3: Install Dependencies

pip install -r requirements.txt

Step 4: Configure the Database

Create a PostgreSQL database:

CREATE DATABASE issue_tracker_db;
CREATE USER issue_tracker_user WITH PASSWORD 'securepassword';
GRANT ALL PRIVILEGES ON DATABASE issue_tracker_db TO issue_tracker_user;

Update settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'issue_tracker_db',
        'USER': 'issue_tracker_user',
        'PASSWORD': 'securepassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

Step 5: Apply Migrations

python manage.py migrate

Step 6: Create a Superuser

python manage.py createsuperuser

Step 7: Collect Static Files

python manage.py collectstatic

Step 8: Start the Development Server

python manage.py runserver

Visit http://127.0.0.1:8000 to access the application.

Deployment Instructions

Production Setup

Use a production WSGI server such as Gunicorn or uWSGI.

Configure a reverse proxy server (e.g., Nginx or Apache).

Enable HTTPS with SSL/TLS certificates.

Set DEBUG = False in settings.py and configure ALLOWED_HOSTS.

Implement caching (e.g., Redis, Memcached) for improved performance.

Optional: Containerize the application with Docker.

User Manual

Administrator Role

Responsibilities: Manage user accounts, permissions, and system configurations.

Navigate to the admin panel at /admin.

Add users, assign roles, and monitor activity logs.

Project Manager Role

Responsibilities: Manage projects, assign tasks, and track progress.

Create projects, add team members, and assign tasks.

Monitor deadlines via the dashboard.

Developer Role

Responsibilities: Work on assigned tasks and update progress.

View assigned tasks in the "My Tasks" section.

Update task statuses and collaborate via comments.

Client/User Role

Responsibilities: Submit issues and provide feedback.

Submit issues via the "Submit Issue" form.

Track issue statuses and communicate with the team.

General Features

Dashboard: Personalized overview of tasks and projects.

Notifications: Receive updates for task assignments and status changes.

Search and Filters: Quickly locate tasks, projects, or issues.

Profile Management: Update personal details and credentials.

Best Practices

Regularly update task statuses and provide feedback.

Use built-in communication tools for collaboration.

Monitor deadlines and prioritize tasks.

API Documentation

Overview

This API provides endpoints for managing projects, tasks, and users. Authentication is required for all endpoints, with some restricted to administrators.

Projects

GET /api/projects/: List all projects.

GET /api/projects/<project_id>/: Retrieve details of a specific project.

Tasks

GET /api/tasks/: List all tasks.

GET /api/tasks/<task_id>/: Retrieve details of a specific task.

Users

GET /api/users/: List all users (admin-only).

GET /api/users/<user_id>/: Retrieve details of a specific user (admin-only).

Authentication

Token or session-based authentication is required.

Admin-only endpoints require staff privileges.

Response Format

All responses are in JSON.

Testing the API

Swagger UI: /swagger/

ReDoc: /redoc/

Postman: Import the Swagger schema for testing.

Troubleshooting

Database Connection Errors: Verify PostgreSQL credentials and status.

Missing Dependencies: Reinstall using pip install -r requirements.txt.

Static Files Issues: Ensure static files are collected and served correctly.

