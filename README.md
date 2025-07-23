# Vehicle Damage Inspection API

A Flask-based REST API for vehicle damage inspection workflow with MySQL database.

## Features

- 🔐 JWT Authentication
- 📦 CRUD Operations for Inspections
- 🖼️ Image URL Validation
- 🛡️ SQL Injection Protection
- 📊 Comprehensive Logging
- 👥 User Authorization

## Local Development

### Prerequisites
- Python 3.11+
- MySQL Server
- Virtual Environment

### Setup
1. Clone the repository
```bash
git clone <your-repo-url>
cd inspectk-assignment
```

2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure MySQL database
```bash
# Create database in MySQL
CREATE DATABASE inspeck;
```

5. Run the application
```bash
python run.py
```

## Deployment to Free Services (MySQL)

### Option 1: Railway 🚂

1. **Create Railway account**: https://railway.app/
2. **Add MySQL service** in Railway dashboard
3. **Connect GitHub repo** to Railway
4. **Set environment variables**:
   ```
   DATABASE_URL=mysql://username:password@host:port/database
   JWT_SECRET_KEY=your-super-secret-key
   ```

### Option 2: PlanetScale + Render

1. **Database**: Create free MySQL database on PlanetScale
2. **App**: Deploy on Render using this repo
3. **Environment variables**:
   ```
   DATABASE_URL=mysql://username:password@host:port/database
   JWT_SECRET_KEY=your-random-secret-key
   ```

### Option 3: Aiven MySQL + Any Host

1. **Database**: Get free trial MySQL from Aiven
2. **Host**: Deploy on Render/Railway/Heroku
3. **Connect**: Use Aiven MySQL connection string

## API Endpoints

### Authentication
- `POST /api/v1/signup` - Register new user
- `POST /api/v1/login` - Login and get JWT token

### Inspections (Protected)
- `POST /api/v1/inspection` - Create inspection
- `GET /api/v1/inspection/<id>` - Get single inspection
- `PATCH /api/v1/inspection/<id>` - Update inspection
- `GET /api/v1/inspection?status=pending` - List inspections

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
DATABASE_URL=mysql://username:password@host:3306/database
JWT_SECRET_KEY=your-secret-key
FLASK_ENV=development
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE,
  password_hash VARCHAR(255)
);
```

### Inspections Table
```sql
CREATE TABLE inspections (
  id INT AUTO_INCREMENT PRIMARY KEY,
  vehicle_number VARCHAR(20),
  inspected_by INT,
  damage_report TEXT,
  status ENUM('pending', 'reviewed', 'completed') DEFAULT 'pending',
  image_url TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (inspected_by) REFERENCES users(id)
);
```

## Security Features

- ✅ SQL Injection Protection (SQLAlchemy ORM)
- ✅ Password Hashing (Werkzeug Security)
- ✅ JWT Token Authentication
- ✅ User Authorization
- ✅ Input Validation
- ✅ Image URL Validation

## Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Database**: MySQL
- **Authentication**: JWT (Flask-JWT-Extended)
- **Security**: Werkzeug Security
- **Deployment**: Docker, Railway/Render compatible 