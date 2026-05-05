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
2. Create .env
  Copy env.example into a .env file and generate a random ssl key for secrets using
```bash
  openssl rand -hex 32
 ```
Paste the key given into SECRETS=
3. Install packages
Run the following to install dependencies
```bash
uv run sync
npm install
```
4. Create a docker contianer for local database
```bash
docker run --name my-new-project-postgres -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mynewprojectdb -p 5433:5432 -d postgres:latest
```
5. Upgrade database
```bash
uv run alembic upgrade head
```
6. Connect to Database using dbeaver

   
Select host and do
Host: localhost
Database: postgres (make sure to select Show all databases)
Port: 5433

Select URL and paste: 
```bash
jdbc:postgresql://localhost:5433/postgres
```

For Authentication:
Username: myuser
Password: mypassword
7.
```bash
uv run main.py
```
Then go to 

http://127.0.0.1:3000/docs
You are done !




   


