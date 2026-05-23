# File: `app/database.py`

## Purpose of This File

The `database.py` file is responsible for creating and managing the database connection for the application.

This file acts as the **bridge between FastAPI and SQLite database**.

Without this file:

- FastAPI cannot connect to database
- Models cannot create tables
- APIs cannot store data
- Monitoring records cannot be saved

In simple words:

```text
FastAPI
    ↓
database.py
    ↓
SQLite Database
```

This file initializes:

1. Database URL
2. SQLAlchemy Engine
3. Session Factory
4. Base Class for Models

---

# Complete Code

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./monitor.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()
```

---

# Understanding the Code Line by Line

---

## Line 1

```python
from sqlalchemy import create_engine
```

### Purpose

Imports:

```python
create_engine()
```

This function creates a connection between Python and the database.

Think of it like:

```text
Python App
      ↓
Connection Pipe
      ↓
Database
```

### Why We Need It

Without `create_engine()`:

FastAPI cannot talk to database.

---

## Line 2

```python
from sqlalchemy.ext.declarative import declarative_base
```

### Purpose

Creates a base class for database models.

This is needed because:

our database tables will be written as Python classes.

Example:

Instead of writing SQL manually:

```sql
CREATE TABLE monitors
```

We write:

```python
class Monitor(Base):
```

SQLAlchemy converts it automatically.

---

## Line 3

```python
from sqlalchemy.orm import sessionmaker
```

### Purpose

Used to create database sessions.

A session is a temporary connection used to:

- insert data
- update data
- delete data
- fetch data

Think of session like:

```text
Database Login Session
```

Whenever API hits database:

A session opens.

After task completes:

Session closes.

---

# Database URL

## Code

```python
SQLALCHEMY_DATABASE_URL = "sqlite:///./monitor.db"
```

---

## Purpose

Defines where database exists.

Here we are using:

```text
SQLite
```

Database file:

```text
monitor.db
```

stored locally.

---

## Breakdown

### `sqlite`

Database engine.

Tells SQLAlchemy:

```text
Use SQLite database
```

---

### `:///`

Means:

Relative path.

---

### `./monitor.db`

Means:

Create database file in current directory.

Expected file:

```text
backend/
│
├── monitor.db
```

---

## What Happens Internally

When app runs:

```text
FastAPI Starts
        ↓
Reads database URL
        ↓
Checks if monitor.db exists
        ↓
If not found:
Create database automatically
```

---

# Creating Database Engine

## Code

```python
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
```

---

## Purpose

Creates database connection engine.

This engine is responsible for:

```text
FastAPI ↔ SQLite Communication
```

---

## Why `check_same_thread=False`

SQLite normally allows:

```text
One thread only
```

But FastAPI runs multiple requests.

Example:

User 1:

```text
POST /monitor
```

User 2:

```text
GET /monitors
```

Both happen simultaneously.

Without:

```python
check_same_thread=False
```

FastAPI crashes.

---

## Internal Working

```text
FastAPI Request
        ↓
Engine Receives Query
        ↓
SQLite Executes Query
        ↓
Result Returned
```

---

# Creating Session Factory

## Code

```python
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

---

## Purpose

Creates database sessions.

Every API request gets:

its own session.

---

## Understanding Parameters

### `autocommit=False`

Means:

Changes are NOT automatically saved.

You must manually call:

```python
db.commit()
```

Why?

Safer database management.

---

### `autoflush=False`

Prevents automatic flushing.

Without this:

SQLAlchemy pushes unfinished data.

Can create inconsistent database state.

---

### `bind=engine`

Binds session with database engine.

Meaning:

```text
Session knows which database to use
```

---

## Internal Workflow

Example:

User calls:

```text
POST /monitor
```

Flow:

```text
Request Comes
      ↓
Session Created
      ↓
Insert Query Runs
      ↓
Commit Database
      ↓
Session Closed
```

---

# Base Class Creation

## Code

```python
Base = declarative_base()
```

---

## Purpose

Creates parent class for models.

All database tables inherit from this.

Example:

```python
class Monitor(Base):
```

Why?

Because SQLAlchemy needs structure.

Without Base:

Tables cannot be created.

---

## Internal Working

```text
Base
   ↓
Model Classes
   ↓
SQLAlchemy ORM
   ↓
Database Tables
```

---

# Expected Output

When app starts:

File automatically created:

```text
monitor.db
```

inside backend folder.

Example:

```text
backend/
│
├── monitor.db
```

---

# Verify Database Creation

Run:

```bash
uvicorn app.main:app --reload
```

Expected:

```text
INFO: Uvicorn running
```

Now check:

```text
backend/
```

You should see:

```text
monitor.db
```

---
