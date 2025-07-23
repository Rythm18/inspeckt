# Vehicle Damage Inspection API
A Flask-based REST API for vehicle damage inspection workflow with MySQL database.


## Local Setup

### Prerequisites
- Python 3.11+
- MySQL Server

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
CREATE DATABASE inspeck;
```

5. Run the application
```bash
python run.py
```

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