# SOT Info Backend

A Django-based REST API backend for the School of Technology information portal. This backend provides authentication, user management, and form submission functionality for various categories including achievements, research, and projects.

## Features

### Authentication
- Custom user model with multiple user types (Student, Faculty, Admin)
- JWT-based authentication
- Email OTP verification for secure registration
- Comprehensive user profile management

### Content Management
- CRUD operations for various content forms
- Categories for achievements, research, and projects
- Support for team projects with multiple members
- Tracking of ongoing projects and achievements
- Featured content highlighting (top 6 items)

### API
- RESTful API design
- Comprehensive API documentation using Swagger/ReDoc
- Permission-based access control

## Tech Stack

- **Django**: Core web framework
- **Django REST Framework**: API functionality
- **PostgreSQL**: Database
- **JWT**: Authentication
- **Swagger/ReDoc**: API documentation
- **CORS**: Cross-origin resource sharing
- **WhiteNoise**: Static file serving
- **Gunicorn**: WSGI HTTP server

## API Endpoints

### Authentication Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/verify_otp/` - OTP verification
- `POST /api/auth/login/` - User login
- `GET /api/auth/me/` - Get current user profile
- `POST /api/auth/resend_otp/` - Resend OTP for registration

### Form Endpoints
- `GET /api/forms/` - List all forms
- `POST /api/forms/` - Create a new form (authenticated)
- `GET /api/forms/:id/` - Retrieve a specific form
- `PUT/PATCH /api/forms/:id/` - Update a form (owner only)
- `DELETE /api/forms/:id/` - Delete a form (owner only)
###More details on www.prod.sost.in/redoc

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8+
- PostgreSQL
- pip (Python package manager)
- virtualenv (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-organization/sot-info-backend.git
   cd sot-info-backend
   ```

2. Set up a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your_secret_key
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   DEFAULT_FROM_EMAIL=your_email@gmail.com
   ```

5. Configure the database in `settings.py` or use environment variables

6. Apply migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

## Running the Application

### Development Mode

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`.

### Production Deployment

For production, use Gunicorn:

```bash
gunicorn sotinfo.wsgi:application
```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

These provide interactive documentation for all API endpoints.

## Admin Interface

The Django admin interface is available at `/admin/`. This provides a comprehensive backend for managing users, forms, and other data.

## Project Structure

```
sotinfo/              # Project directory
├── authentication/   # Authentication app
│   ├── models.py     # User and OTP models
│   ├── serializers.py# Authentication serializers
│   ├── views.py      # Authentication endpoints
│   └── utils.py      # Utility functions for auth
├── catogories/       # Form categories app
│   ├── models.py     # Form model
│   ├── serializers.py# Form serializers
│   └── views.py      # Form endpoints
└── sotinfo/          # Project settings
    ├── settings.py   # Django settings
    ├── urls.py       # URL configuration
    └── routing.py    # DRF router configuration
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| SECRET_KEY | Django secret key |
| EMAIL_HOST_USER | Email for sending OTPs |
| EMAIL_HOST_PASSWORD | Password/app password for email |
| DEFAULT_FROM_EMAIL | Default sender email |


## Contributing

1. No Contributions are allowed as of now

## Contact

For questions or support, please contact: kshitijmoghe10@gmail.com
