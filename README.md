# All-Or-Nothing

## Contributors

- Agustin Xocua Dimayuga
- Fabian Ballesteros-Limon
- Miguel Medina
- Nicolas Rosetes Beltran

## Project Overview

All-Or-Nothing is a public backend API for a sports betting simulator. Users can browse real-world games, place virtual-currency bets, and track their performance over time. The API manages user balances, bet history, outcomes, leaderboards, and comments. The project uses a persistent relational database and is designed to support live sports data.

## Tech Stack

- Python 3.12
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Alembic
- uv for Python dependency management

## Prerequisites

Before setting up the project, install:

- Python 3.12 or newer
- PostgreSQL
- uv
- Git

Install `uv` if you do not already have it:

```bash
python -m pip install uv
```

## Local Development Setup

1. Clone the repository:

```bash
git clone https://github.com/AgustinDimayuga/All-Or-Nothing.git
cd All-Or-Nothing
```

2. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

3. Install Python dependencies:

```bash
uv sync
```

If `uv sync` is unavailable, use:

```bash
python -m pip install -r requirements.txt
```

4. Create a local environment file:

```bash
cp default.env .env
```

5. Update `.env` with your local values:

```env
API_KEY=your_api_key_here
POSTGRES_URI=postgresql+psycopg://myuser:mypassword@localhost:5433/mynewprojectdb
```

The included `default.env` shows the expected variable names. Your `.env` file should not be committed.

## Database Setup

Create a PostgreSQL database that matches your `POSTGRES_URI`. For the default connection string, the database settings are:

- user: `myuser`
- password: `mypassword`
- host: `localhost`
- port: `5433`
- database: `mynewprojectdb`

If your PostgreSQL setup uses different credentials, update `POSTGRES_URI` in `.env`.

After the database exists, run the Alembic migrations:

```bash
alembic upgrade head
```

## Running the API

Start the development server:

```bash
python main.py
```

The API will run at:

```text
http://127.0.0.1:3000
```

You can also run it directly with Uvicorn:

```bash
uvicorn src.api.server:app --reload --host 127.0.0.1 --port 3000 --env-file .env
```

## Verifying the Setup

Once the server is running, open:

```text
http://127.0.0.1:3000/
```

Expected response:

```json
{"status":"ok"}
```

FastAPI's interactive API docs are available at:

```text
http://127.0.0.1:3000/docs
```

## Useful Commands

Run tests:

```bash
pytest
```

Run the linter:

```bash
ruff check .
```

Run type checking:

```bash
mypy .
```

Create a new Alembic migration after changing database models:

```bash
alembic revision -m "describe change here"
```

Apply migrations:

```bash
alembic upgrade head
```

## Notes for Graders and Teammates

- Use Python 3.12 to match the project configuration.
- Copy `default.env` to `.env` before running the app.
- Make sure PostgreSQL is running before applying migrations.
- The app loads `default.env` first, then overrides values with `.env`.
- The Render deployment uses `requirements.txt`, while local development can use `uv sync`.
