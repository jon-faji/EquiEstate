# EquiEstate - Real Estate Management System

A comprehensive Django-based web application for managing residential, commercial, and industrial properties, tenants, and financial transactions.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [Admin Panel](#admin-panel)
- [Security Features](#security-features)

## Features

- **Property Management**: Add, edit, and manage multiple properties (residential, commercial, industrial)
- **Tenant Registry**: Complete tenant information management with lease details
- **Transaction Tracking**: Monitor rent payments, track payment status (Paid, Pending, Overdue)
- **Advanced Search**: Filter and search properties and tenants by various criteria
- **Sorting Options**: Sort properties and tenants by multiple fields
- **User Authentication**: Secure login system using django-allauth
- **Dashboard**: Comprehensive property and tenant dashboards with statistics
- **Role-Based Access**: Admin and staff-level access control
- **Profile Management**: User profile management with avatar support
- **PWA Support**: Progressive Web App capabilities for offline access
- **Responsive Design**: Mobile-friendly interface with bootstrap styling
- **Pagination**: Efficient data display with pagination support

## Technology Stack

### Backend
- **Django 6.0.5** - Web framework
- **Python** - Programming language
- **PostgreSQL** - Database (psycopg2-binary support)
- **SQLite** - Development database

### Frontend
- **HTML/CSS/JavaScript** - Frontend technologies
- **Bootstrap** - CSS framework (via static files)
- **Django Templates** - Server-side templating

### Key Dependencies
- **django-allauth 65.17.0** - User authentication and social auth
- **django-pwa 2.0.1** - Progressive Web App support
- **django-ratelimit 4.1.0** - API rate limiting
- **django-widget-tweaks 1.5.1** - Form widget customization
- **Pillow 12.2.0** - Image processing
- **Faker 40.18.0** - Test data generation
- **PyJWT 2.13.0** - JWT token handling
- **python-dotenv 1.2.2** - Environment variable management
- **requests 2.34.2** - HTTP client library

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL (optional, for production)

### Setup Steps

1. **Clone/Access the Project**
   ```bash
   cd c:\Personal\Computer\Projects\myenv\EquiEstate
   ```

2. **Activate Virtual Environment** (Windows)
   ```bash
   ..\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r realestateproject/requirements.txt
   ```

4. **Navigate to Project Directory**
   ```bash
   cd realestateproject
   ```

5. **Apply Database Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect Static Files** (for production)
   ```bash
   python manage.py collectstatic
   ```

8. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

The application will be available at `http://127.0.0.1:8000/`

## Configuration

### Environment Variables
Create a `.env` file in the project root with the following variables:

```env
DJANGO_SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost,your-domain.com
DATABASE_URL=postgresql://user:password@localhost/equiestate
DEBUG=True  # Set to False in production
```

### Allowed Hosts (settings.py)
Default allowed hosts are configured for:
- `127.0.0.1`
- `localhost`
- `production.pythonanywhere.com`

Modify `realestateproject/settings.py` to add your deployment domain.

## Usage

### Admin Panel
Access the Django admin panel at `/admin/` with your superuser credentials to:
- Manage properties, tenants, and transactions
- View system logs and activity
- Manage user accounts and permissions

### Main Features

#### Properties Dashboard
- View all properties with pagination (5 per page)
- Search properties by name, address, or type
- Sort by name, address, or number of units
- Add/Edit/Delete properties

#### Tenants Registry
- View all registered tenants
- Search tenants by first name, last name, or email
- Sort by name or creation date
- Manage lease information and rent amounts

#### Transactions
- Track rent payments
- View payment status (Paid, Pending, Overdue)
- Monitor tenant payment history
- Generate financial reports and statistics

## Project Structure

```
EquiEstate/
├── README.md                          # This file
├── realestateproject/
│   ├── manage.py                      # Django management script
│   ├── db.sqlite3                     # SQLite database
│   ├── requirements.txt               # Project dependencies
│   │
│   ├── estateapp/                     # Main application
│   │   ├── models.py                  # Database models
│   │   ├── views.py                   # View logic
│   │   ├── admin.py                   # Admin configuration
│   │   ├── urls.py                    # URL routing
│   │   ├── tests.py                   # Unit tests
│   │   ├── management/                # Custom management commands
│   │   └── migrations/                # Database migrations
│   │
│   ├── realestateproject/             # Project configuration
│   │   ├── settings.py                # Django settings
│   │   ├── urls.py                    # URL configuration
│   │   ├── wsgi.py                    # WSGI configuration
│   │   └── asgi.py                    # ASGI configuration
│   │
│   ├── templates/                     # HTML templates
│   │   ├── base.html                  # Base template
│   │   ├── home.html                  # Home page
│   │   ├── property.html              # Properties dashboard
│   │   ├── tenant.html                # Tenants registry
│   │   ├── transactions.html          # Transactions view
│   │   ├── statistics.html            # Statistics/Reports
│   │   ├── profile.html               # User profile
│   │   ├── crud_form.html             # Generic CRUD form
│   │   ├── crud_delete.html           # Delete confirmation
│   │   ├── account/                   # Account-related templates
│   │   ├── includes/                  # Template includes
│   │   └── socialaccount/             # Social auth templates
│   │
│   ├── static/                        # Static files (development)
│   │   ├── css/                       # Stylesheets
│   │   ├── js/                        # JavaScript files
│   │   ├── img/                       # Images
│   │   └── fonts/                     # Font files
│   │
│   ├── staticfiles/                   # Collected static files (production)
│   ├── profile_photos/                # User profile photo storage
│   └── .env                           # Environment variables (not in repo)
│
└── Scripts/                           # Virtual environment scripts
    ├── activate                       # Activation script
    ├── activate.bat                   # Windows batch activation
    ├── Activate.ps1                   # PowerShell activation
    └── deactivate.bat                 # Deactivation script
```

## Database Models

### BaseModel
Abstract base model with common fields:
- `created_at` - Timestamp when record was created
- `updated_at` - Timestamp when record was last updated

### Property
Represents real estate properties:
- **name** - Property name
- **address** - Property address
- **property_type** - Type: Residential, Commercial, or Industrial
- **units** - Number of units/rooms

### Tenant
Represents tenants renting properties:
- **first_name** - Tenant's first name
- **last_name** - Tenant's last name
- **email** - Email address (unique)
- **phone** - Contact phone number
- **property** - Associated property (OneToOne)
- **lease_start** - Lease start date
- **lease_end** - Lease end date
- **rent_amount** - Monthly rent amount

### Transaction
Tracks financial transactions:
- **property** - Related property
- **tenant** - Related tenant
- **amount** - Transaction amount
- **date** - Transaction date
- **status** - Payment status (Paid, Pending, Overdue)

### SystemProfile
System administration profile:
- **profile_name** - Profile display name
- **email** - Profile email
- **avatar** - Profile photo (optional)

## Security Features

- **CSRF Protection** - Cross-Site Request Forgery protection enabled
- **Login Required** - All main views require authentication
- **Role-Based Access** - Staff/Superuser required for administrative actions
- **Rate Limiting** - django-ratelimit prevents abuse
- **Secure Passwords** - Django's password hashing system
- **Environment Variables** - Sensitive data via .env configuration
- **SQL Injection Prevention** - ORM usage prevents SQL injection

## URL Routing

Configure URL patterns in `estateapp/urls.py` and include in `realestateproject/urls.py`:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # Add app-specific URLs
]
```

## Management Commands

Run custom management commands:
```bash
python manage.py <command_name>
```

Place custom commands in `estateapp/management/commands/`

## Testing

Run tests with:
```bash
python manage.py test
```

Add tests to `estateapp/tests.py`

## Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Update `ALLOWED_HOSTS` with your domain
3. Configure a production database (PostgreSQL recommended)
4. Use a production WSGI server (Gunicorn, uWSGI)
5. Collect static files: `python manage.py collectstatic`
6. Set up HTTPS/SSL certificates
7. Configure environment variables securely

## License

This project is provided as-is for educational purpose.

## Support

For issues or questions, please refer to:
- Django Documentation: https://docs.djangoproject.com/
- Django-allauth: https://django-allauth.readthedocs.io/
- PostgreSQL: https://www.postgresql.org/docs/

---

**Last Updated:** May 2026
**Django Version:** 6.0.5
**Python Version:** 3.8+
