# Drug Spot Backend

REST API for the Drug Spot mobile application, built with **Django REST Framework** and **PostgreSQL**

## Project Structure

```
drug_spot_backend/
├── manage.py
├── requirements.txt
├── .env.example
├── drug_spot/              # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── users/                  # User auth & profiles
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── pharmacies/             # Pharmacy locations
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── medicines/              # Medicine inventory
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   └── admin.py
└── medicine_requests/      # Medicine requests
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── admin.py
```

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (for admin panel)
python manage.py createsuperuser

# Run development server
python manage.py runserver 3001
```

## API Endpoints

| Method | Endpoint                         | Auth | Description                |
|--------|----------------------------------|------|----------------------------|
| POST   | `/api/register`                  | No   | Register a new user        |
| POST   | `/api/login`                     | No   | Login, returns JWT token   |
| GET    | `/api/profile`                   | Yes  | Get current user profile   |
| PUT    | `/api/profile`                   | Yes  | Update current user profile|
| GET    | `/api/pharmacies/`               | No   | List all pharmacies        |
| GET    | `/api/pharmacies/<id>`           | No   | Get pharmacy by ID         |
| GET    | `/api/medicines/`                | No   | List all medicines         |
| GET    | `/api/medicines/<id>`            | No   | Get medicine by ID         |
| GET    | `/api/medicines/pharmacy/<id>`   | No   | Get medicines by pharmacy  |
| POST   | `/api/medicines/`                | Yes  | Add medicine (pharmacy)    |
| PUT    | `/api/medicines/<id>`            | Yes  | Update medicine (owner)    |
| DELETE | `/api/medicines/<id>`            | Yes  | Delete medicine (owner)    |
| GET    | `/api/medicine_requests/`        | No   | List all requests          |
| POST   | `/api/medicine_requests/`        | No   | Create a medicine request  |

Auth uses JWT Bearer tokens via `Authorization: Bearer <token>` header.
