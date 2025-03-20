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

This application requires a **PostgreSQL** database as **SQLite is not supported** due to the use of **Enum fields** in the models.

#### Install PostgreSQL

If you don't have PostgreSQL installed, follow the official installation guide:

- [PostgreSQL Installation Guide](https://www.postgresql.org/download/)

#### Create a PostgreSQL Database

Once PostgreSQL is installed, create a new database with the following command:

```sh
psql -U your_user -d postgres -c "CREATE DATABASE database_name;"
```

Modify `.env` with your PostgreSQL database settings:

```env
DATABASE_URL=postgresql://
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Initialize the database:

```sh
python scripts/create_tables.py
```

### Database Management Scripts

To manage the database, use the following scripts:

| Script                  | Description |
|-------------------------|-------------|
| `test_connection.py`    | Tests the connection to the database. |
| `delete_db.py`         | Deletes all database tables. |
| `reset_db.py`          | Resets the database by deleting and recreating tables. |
| `create_admin.py`      | Creates an admin user if it does not exist. |
| `populate_database.py` | Populates the database with test data. |

### Running Database Scripts

#### Test the Database Connection
```sh
python scripts/test_connection.py
```

## Usage

### Sentry Configuration

This application uses **Sentry** for error tracking and performance monitoring.

#### Configure Sentry

Modify `.env` with your Sentry DSN:

```env
SENTRY_DSN=https://your_sentry_dsn@sentry.io/project_id
```

For more details on Sentry, visit [Sentry Documentation](https://docs.sentry.io/).

### Launch the application

```sh
python main.py
```

The application starts with a main menu allowing navigation between different sections.

### Authentication

On startup, the user must authenticate using their email and password.

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