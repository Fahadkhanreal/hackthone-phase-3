# Quickstart Guide: Backend Database and ORM Setup

**Feature**: 001-db-orm-setup
**Date**: 2026-01-26

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Navigate to backend directory**
   ```bash
   cd backend
   ```

3. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update `DATABASE_URL` with your Neon PostgreSQL connection string

6. **Start the application**
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

## API Endpoints

- `GET /health` - Health check endpoint that confirms database connectivity

## Environment Variables

- `DATABASE_URL` - Neon PostgreSQL connection string (required)
- `ENVIRONMENT` - Development/production mode (optional, defaults to "development")

## Verification Steps

1. After starting the application, visit `http://localhost:8000/health` to verify the health check endpoint is working
2. The response should be: `{"status": "healthy", "db_connected": true}`
3. Check the console logs for successful database connection messages
4. Verify that tables were created in your Neon database

## Troubleshooting

- If you get a database connection error, verify your `DATABASE_URL` in the `.env` file
- If tables aren't created, ensure your database user has CREATE TABLE permissions
- For async operation issues, check that all dependencies are properly installed