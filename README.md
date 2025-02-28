# CRM Management System

## Description

This project is a command-line application developed in Python for managing clients, contracts, and events for a service-based company. It follows an MVC architecture and implements the Repository Pattern for clear separation of responsibilities.

## Features

- User management with JWT authentication and roles (Sales, Management, Support).
- Management of clients, contracts, and events with specific permissions.
- Separation of responsibilities via Repository Pattern:
  - **Repository**: Data access.
  - **Service**: Business logic.
  - **Controller**: User interaction.
- Application security with role-based permissions.
- Intuitive command-line interface.

## Installation

### 1. Clone the repository

```sh
git clone https://github.com/FabL-B/OC_Projet12.git
cd OC_Projet12
```

### 2. Create and activate the virtual environment

```sh
python -m venv env
source env/bin/activate  # For Linux and Mac
env\Scripts\activate     # For Windows
```

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

### 4. Database configuration

Modify `.env` with your database settings:

```env
DATABASE_URL=sqlite:///db.sqlite3
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Initialize the database:

```sh
python setup_database.py
```

## Usage

### Launch the application

```sh
python main.py
```

The application starts with a main menu allowing navigation between different sections.

### Authentication

On startup, the user must authenticate using their email and password.

## Main Features

| Feature                  | Required Role       | CLI Command |
|--------------------------|--------------------|--------------|
| List users               | Management        | `1 -> 1`     |
| Create user              | Management        | `1 -> 2`     |
| List clients             | Sales, Management | `2 -> 1`     |
| Create client            | Sales             | `2 -> 3`     |
| List contracts           | Management        | `3 -> 1`     |
| Create contract          | Management        | `3 -> 4`     |
| List events              | Support, Management | `4 -> 1` |
| Create event             | Sales             | `4 -> 3`     |

## Testing

### Run all tests

```sh
pytest
```

### Check test coverage

```sh
pytest --cov=app tests/
```

### Generate a detailed HTML report

```sh
pytest --cov=app --cov-report=html tests/
```

The report is available in the `htmlcov/` directory.

## Project Structure

```
📂 app/
 ├─📂 controllers/        # Handles user interactions
 ├─📂 models/             # Defines SQLAlchemy models
 ├─📂 repository/         # Manages data access
 ├─📂 services/           # Business logic
 ├─📂 views/              # Command-line interfaces
 ├─📂 auth/               # Authentication and permission handling
 ├─📂 permissions/        # Role and permission management
 ├─ config/                # Application configuration
 ├─ main.py                # Application entry point
 ├─ setup_database.py      # Database initialization
 ├─ requirements.txt       # Python dependencies
```

Developed with Python, SQLAlchemy, and JWT Authentication.