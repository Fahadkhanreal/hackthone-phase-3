# Quickstart Guide: Neon Database Connection and Table Creation

**Feature**: 002-neon-table-creation
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
   - The format should be: `postgresql+asyncpg://username:password@host:port/database`

6. **Start the application**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

## Verification Steps

1. After starting the application, check the console logs for successful table creation messages
2. Visit `http://localhost:8000/health` to verify the health check endpoint is working
3. The response should be: `{"status": "healthy", "database": "connected"}`
4. Log into your Neon dashboard and navigate to the Tables section to confirm the "task" table exists

## API Endpoints

- `GET /health` - Health check endpoint that confirms database connectivity

## Environment Variables

- `DATABASE_URL` - Neon PostgreSQL connection string (required)

## Troubleshooting

- If you get a database connection error, verify your `DATABASE_URL` in the `.env` file
- If the task table doesn't appear in Neon, check that the startup event executed successfully
- For async operation issues, check that all dependencies are properly installed