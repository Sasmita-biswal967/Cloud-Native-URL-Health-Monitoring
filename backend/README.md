# File: `requirements.txt`

## Purpose of This File

The `requirements.txt` file stores all Python packages required for the project.

---

# Complete Code

```txt
fastapi
uvicorn
sqlalchemy
pydantic
requests
prometheus-fastapi-instrumentator
boto3
python-multipart
```

---

# Understanding Every Dependency

---

# 1. FastAPI

## Package

```txt
fastapi
```

---

## Purpose

Core backend framework.

Used to build:

```text
REST APIs
```

FastAPI handles:

- HTTP requests
- Routing
- Validation
- Swagger docs
- JSON responses

---

## Example Usage

In project:

```python
from fastapi import FastAPI
```

Used in:

```python
main.py
```

---

## What Happens Internally

```text
Client Request
        ↓
FastAPI
        ↓
Route Handler
        ↓
JSON Response
```

---

# 2. Uvicorn

## Package

```txt
uvicorn
```

---

## Purpose

Runs FastAPI server.

FastAPI alone cannot run.

It needs an:

```text
ASGI Server
```

Uvicorn acts as:

```text
Backend Server Engine
```

---

## Example Command

```bash
uvicorn app.main:app --reload
```

---

## Internal Working

```text
FastAPI App
       ↓
Uvicorn Server
       ↓
Browser Access
```

---

# 3. SQLAlchemy

## Package

```txt
sqlalchemy
```

---

## Purpose

Handles database operations.

Used for:

```text
ORM (Object Relational Mapping)
```

Instead of SQL:

```sql
SELECT * FROM monitors
```

we write:

```python
db.query(Monitor)
```

---

## Example Usage

```python
from sqlalchemy.orm import Session
```

Used in:

```text
database.py
models.py
routes.py
```

---

## Internal Workflow

```text
Python Class
      ↓
SQLAlchemy ORM
      ↓
SQL Query
      ↓
SQLite Database
```

---

# 4. Pydantic

## Package

```txt
pydantic
```

---

## Purpose

Used for:

```text
Data Validation
```

Prevents invalid request data.

Example:

Bad Request:

```json
{
  "url": 123
}
```

FastAPI rejects automatically.

---

## Example Usage

```python
from pydantic import BaseModel
```

Used in:

```text
schemas.py
```

---

# 5. Requests

## Package

```txt
requests
```

---

## Purpose

Checks URL availability.

Used to:

```text
Send HTTP Request
```

Example:

```python
requests.get(
    "https://google.com"
)
```

Used in:

```text
routes.py
```

for:

```http
/check/{id}
```

---

## Internal Workflow

```text
FastAPI
      ↓
requests.get()
      ↓
Website Response
      ↓
Healthy/Down
```

---

# 6. Prometheus Instrumentator

## Package

```txt
prometheus-fastapi-instrumentator
```

---

## Purpose

Adds:

```text
/metrics
```

endpoint automatically.

Needed for:

```text
Prometheus Monitoring
```

Without this:

Prometheus cannot scrape app.

---

## Example Usage

```python
Instrumentator()
```

Used in:

```text
main.py
```

---

## Metrics Example

Visit:

```text
localhost:8000/metrics
```

Output:

```text
http_requests_total
request_duration
process_cpu_seconds_total
```

---

# 7. boto3

## Package

```txt
boto3
```

---

## Purpose

AWS SDK for Python.

Allows connection to:

- S3
- Lambda
- EC2
- CloudWatch

Used here for:

```text
AWS S3 Upload
```

---

## Example Usage

```python
s3 = boto3.client("s3")
```

Used in:

```text
s3_service.py
```

---

## Internal Workflow

```text
Python App
      ↓
boto3 SDK
      ↓
AWS S3
```

---

# 8. python-multipart

## Package

```txt
python-multipart
```

---

## Purpose

Supports:

```text
Form Data Uploads
```

Especially useful for:

```text
future file upload APIs
```

FastAPI may require this.

---

## Why Included

Even if not used immediately:

Useful for scalability.

Future enhancement ready.

---

# How to Install Dependencies

## Command

```bash
pip install -r requirements.txt
```

---

## What This Command Does

Breakdown:

### `pip install`

Installs packages.

---

### `-r`

Means:

```text
Read File
```

---

### `requirements.txt`

Installs everything listed.

---

## Internal Workflow

```text
requirements.txt
        ↓
pip reads packages
        ↓
Downloads libraries
        ↓
Installs dependencies
        ↓
Environment ready
```

---

# Expected Output

Successful installation:

```text
Successfully installed
fastapi
uvicorn
sqlalchemy
requests
boto3
...
```

---

# Verify Installation

Run:

```bash
pip list
```

Expected packages:

```text
fastapi
sqlalchemy
requests
boto3
uvicorn
```

---

# Freeze Installed Packages

Generate versioned requirements:

```bash
pip freeze > requirements.txt
```

---

## Why Useful

Locks package versions.

Example:

```txt
fastapi==0.115.0
uvicorn==0.35.0
```

Useful for:

```text
Docker
Kubernetes
CI/CD
Production
```

Prevents:

```text
Version mismatch issues
```

---

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

# File: `app/models.py`

## Purpose of This File

The `models.py` file is responsible for defining the **database tables**.

In SQLAlchemy ORM, tables are represented using Python classes.

Instead of writing SQL manually:

```sql
CREATE TABLE monitors (
    id INTEGER PRIMARY KEY,
    url TEXT
);
```

we define tables like this:

```python
class Monitor(Base):
```

SQLAlchemy automatically converts Python code into database tables.

Think of this file as:

```text
Python Classes
        ↓
SQLAlchemy ORM
        ↓
Database Tables
```

This file defines:

- Table names
- Columns
- Data types
- Constraints

Without this file:

- No database table exists  
- No data can be stored  
- APIs cannot save monitoring records

---

# Complete Code

```python
from sqlalchemy import Column, Integer, String
from .database import Base


class Monitor(Base):

    __tablename__ = "monitors"

    id = Column(Integer, primary_key=True, index=True)

    url = Column(String, nullable=False)

    status = Column(String, default="Unknown")
```

---

# Understanding the Code Line by Line

---

## Import 1

```python
from sqlalchemy import Column, Integer, String
```

### Purpose

Imports SQLAlchemy column types.

We use:

### `Column`

Defines a table column.

Example:

```python
id = Column(Integer)
```

means:

```text
Database Column
```

---

### `Integer`

Stores numbers.

Example:

```text
1
2
3
100
```

Used for:

```python
id
```

---

### `String`

Stores text.

Example:

```text
google.com
healthy
down
```

Used for:

```python
url
status
```

---

## Import 2

```python
from .database import Base
```

### Purpose

Imports:

```python
Base
```

from:

```python
database.py
```

Remember:

In `database.py`:

```python
Base = declarative_base()
```

This is required because:

all models must inherit from Base.

Without Base:

SQLAlchemy cannot create tables.

---

# Creating Table Class

## Code

```python
class Monitor(Base):
```

---

## Purpose

Defines a table.

Class name:

```text
Monitor
```

represents:

```text
monitor table
```

---

## Why inherit `Base`

```python
(Base)
```

This tells SQLAlchemy:

```text
This is a database table
```

Without Base:

It becomes a normal Python class.

No table gets created.

---

# Table Name

## Code

```python
__tablename__ = "monitors"
```

---

## Purpose

Defines actual database table name.

Database table becomes:

```text
monitors
```

---

## Why Needed

Without this:

SQLAlchemy may auto-generate confusing names.

Better to define explicitly.

---

## Database Output

SQLite table:

```sql
monitors
```

---

# Primary Key Column

## Code

```python
id = Column(
    Integer,
    primary_key=True,
    index=True
)
```

---

## Purpose

Creates unique identifier.

Every record gets:

```text
1
2
3
4
```

automatically.

---

## Understanding Parameters

### `Integer`

Data type:

```text
number
```

---

### `primary_key=True`

Marks column as:

```text
PRIMARY KEY
```

Meaning:

Every row must be unique.

Example:

| id | url |
|----|-----|
| 1 | google.com |
| 2 | github.com |

No duplicate IDs allowed.

---

### `index=True`

Creates database index.

Purpose:

Faster search.

Example:

Searching:

```text
id = 2
```

becomes faster.

---

## Internal Working

When row inserted:

```text
Database
      ↓
Auto Generates ID
      ↓
1,2,3,4...
```

---

# URL Column

## Code

```python
url = Column(
    String,
    nullable=False
)
```

---

## Purpose

Stores website URL.

Example:

```text
https://google.com
https://github.com
```

---

## Understanding Parameters

### `String`

Text datatype.

---

### `nullable=False`

Means:

Cannot be empty.

Example:

❌ Invalid

```json
{
    "url": ""
}
```

or

```json
{
}
```

---

✅ Valid

```json
{
    "url": "https://google.com"
}
```

---

## Database Rule

Database enforces:

```text
URL REQUIRED
```

---

# Status Column

## Code

```python
status = Column(
    String,
    default="Unknown"
)
```

---

## Purpose

Stores monitoring result.

Example values:

```text
Healthy
Down
Unknown
```

---

## Why Default Value

Before monitoring runs:

Status unknown.

Instead of NULL:

We set:

```text
Unknown
```

---

## Example Flow

User adds URL:

```json
{
    "url": "https://google.com"
}
```

Database:

| id | url | status |
|----|-----|---------|
| 1 | google.com | Unknown |

Later:

Monitoring checks health.

Status updates:

```text
Healthy
```

---

# What Happens Internally

When FastAPI starts:

```text
models.py loads
       ↓
SQLAlchemy reads classes
       ↓
Creates schema
       ↓
Creates monitors table
```

---

# Actual Database Table

Equivalent SQL:

```sql
CREATE TABLE monitors (
    id INTEGER PRIMARY KEY,
    url VARCHAR NOT NULL,
    status VARCHAR DEFAULT 'Unknown'
);
```

---

# Expected Output

After app runs:

Database table created automatically.

Verify:

Install SQLite viewer or DB Browser.

You should see:

```text
monitor.db
```

Table:

```text
monitors
```

Columns:

```text
id
url
status
```

---

# Example Database Records

Example:

| id | url | status |
|----|-----|---------|
| 1 | https://google.com | Healthy |
| 2 | https://github.com | Down |

---

# Internal Workflow

API Request:

```json
{
    "url": "https://google.com"
}
```

Flow:

```text
FastAPI
      ↓
routes.py
      ↓
models.py
      ↓
SQLAlchemy ORM
      ↓
SQLite Database
```

---

# File: `app/schemas.py`

## Purpose of This File

The `schemas.py` file is responsible for:

```text
Request Validation
Response Validation
Data Serialization
```

In FastAPI, schemas are created using:

```python
Pydantic
```

Pydantic ensures that incoming API data is:

✅ Correct format  
✅ Correct datatype  
✅ Validated automatically

Without schemas:

❌ Invalid data enters database  
❌ APIs become unsafe  
❌ No automatic validation

Think of schemas as:

```text
Security Gate for API Data
```

Flow:

```text
Client Request
      ↓
Schema Validation
      ↓
FastAPI
      ↓
Database
```

---

# Why Schemas Are Needed

Suppose user sends:

Bad Request:

```json
{
    "url": 12345
}
```

URL should be text.

Without schema:

Database may crash.

With schema:

FastAPI automatically rejects request.

Error:

```json
{
  "detail": [
    {
      "msg": "Input should be a valid string"
    }
  ]
}
```

This makes APIs safer.

---

# Complete Code

```python
from pydantic import BaseModel


class MonitorCreate(BaseModel):

    url: str


class MonitorResponse(BaseModel):

    id: int
    url: str
    status: str

    class Config:
        from_attributes = True
```

---

# Understanding the Code Line by Line

---

## Import

```python
from pydantic import BaseModel
```

### Purpose

Imports:

```python
BaseModel
```

from:

```text
Pydantic
```

Pydantic helps FastAPI:

- validate data
- serialize data
- enforce datatype rules

Without BaseModel:

schemas cannot exist.

---

# First Schema

## Code

```python
class MonitorCreate(BaseModel):
```

---

## Purpose

Used when:

User creates new monitor.

Example:

```http
POST /monitor
```

Incoming request:

```json
{
    "url": "https://google.com"
}
```

This schema validates:

```text
Input Data
```

---

# URL Field

## Code

```python
url: str
```

---

## Purpose

Defines:

```text
url must be string
```

Valid:

```json
{
    "url": "https://google.com"
}
```

---

Invalid:

```json
{
    "url": 123
}
```

Error:

```json
{
  "detail": [
    {
      "msg": "Input should be a valid string"
    }
  ]
}
```

---

## Internal Working

When request arrives:

```text
JSON Request
      ↓
Pydantic Schema
      ↓
Validation Check
      ↓
Accept or Reject
```

---

# Second Schema

## Code

```python
class MonitorResponse(BaseModel):
```

---

## Purpose

Used for:

```text
API Response
```

after database returns data.

Example:

Response:

```json
{
    "id": 1,
    "url": "https://google.com",
    "status": "Healthy"
}
```

This schema controls:

what response looks like.

---

# ID Field

## Code

```python
id: int
```

---

## Purpose

Defines:

```text
ID must be integer
```

Example:

```json
"id": 1
```

---

# URL Field

## Code

```python
url: str
```

---

## Purpose

Response must include:

```text
URL
```

Example:

```json
"url": "https://github.com"
```

---

# Status Field

## Code

```python
status: str
```

---

## Purpose

Returns monitoring state.

Possible values:

```text
Healthy
Down
Unknown
```

Example:

```json
"status": "Healthy"
```

---

# Config Class

## Code

```python
class Config:
```

---

## Purpose

Provides extra schema settings.

---

## Important Line

```python
from_attributes = True
```

---

## Why Needed

Database returns:

```python
SQLAlchemy Objects
```

Example:

```python
<Monitor object>
```

FastAPI cannot directly convert ORM objects to JSON.

This line tells FastAPI:

```text
Convert ORM Object → JSON
```

Without this:

Error:

```text
Validation Error
```

or

```text
Object is not JSON serializable
```

---

## Internal Workflow

Database:

```python
monitor_object
```

↓

Schema converts:

```json
{
    "id": 1,
    "url": "https://google.com",
    "status": "Healthy"
}
```

---

# What Happens Internally

Example Request:

```json
{
    "url": "https://google.com"
}
```

Flow:

```text
Client Request
      ↓
MonitorCreate Schema
      ↓
Validation
      ↓
routes.py
      ↓
Database Insert
      ↓
MonitorResponse Schema
      ↓
JSON Response
```

---

# Example API Flow

Request:

```http
POST /monitor
```

Body:

```json
{
    "url": "https://google.com"
}
```

---

Validated By:

```python
MonitorCreate
```

---

Database stores:

| id | url | status |
|----|-----|---------|
| 1 | google.com | Unknown |

---

Response:

```json
{
    "id": 1,
    "url": "https://google.com",
    "status": "Unknown"
}
```

Validated by:

```python
MonitorResponse
```

---

# Expected Outputs

Swagger automatically generates schema.

Open:

```text
/docs
```

You will see:

### Request Schema

```json
{
  "url": "string"
}
```

---

### Response Schema

```json
{
  "id": 0,
  "url": "string",
  "status": "string"
}
```

---

# File: `app/routes.py`

## Purpose of This File

The `routes.py` file contains the **API endpoints (routes)** and application business logic.

This file is responsible for:

- Creating URL monitors
- Fetching monitoring data
- Checking URL health
- Updating monitoring status
- Communicating with database

Think of this file as:

```text
Client Request
      ↓
routes.py
      ↓
Database
      ↓
Response
```

Without this file:

❌ APIs will not exist  
❌ No CRUD operations  
❌ No URL monitoring

This is the **heart of the FastAPI application**.

---

# Complete Code

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import requests

from .database import SessionLocal
from .models import Monitor
from .schemas import (
    MonitorCreate,
    MonitorResponse
)

router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post(
    "/monitor",
    response_model=MonitorResponse
)
def create_monitor(
    monitor: MonitorCreate,
    db: Session = Depends(get_db)
):

    new_monitor = Monitor(
        url=monitor.url
    )

    db.add(new_monitor)

    db.commit()

    db.refresh(new_monitor)

    return new_monitor


@router.get(
    "/monitors",
    response_model=list[MonitorResponse]
)
def get_monitors(
    db: Session = Depends(get_db)
):

    return db.query(Monitor).all()


@router.get("/check/{monitor_id}")
def check_url(
    monitor_id: int,
    db: Session = Depends(get_db)
):

    monitor = db.query(
        Monitor
    ).filter(
        Monitor.id == monitor_id
    ).first()

    if not monitor:
        return {
            "error":
            "Monitor not found"
        }

    try:

        response = requests.get(
            monitor.url,
            timeout=5
        )

        if response.status_code == 200:
            monitor.status = "Healthy"
        else:
            monitor.status = "Down"

    except:

        monitor.status = "Down"

    db.commit()

    return {
        "url": monitor.url,
        "status": monitor.status
    }
```

---

# Understanding the Code Line by Line

---

# Imports

---

## FastAPI Imports

```python
from fastapi import APIRouter, Depends
```

### Purpose

Imports FastAPI tools.

---

### `APIRouter`

Used to create API routes.

Instead of writing all APIs in:

```python
main.py
```

we separate them.

Example:

```python
router = APIRouter()
```

helps organize endpoints.

---

### `Depends`

Used for:

```text
Dependency Injection
```

Example:

Database session injection.

Instead of manually creating DB connection every time:

FastAPI injects automatically.

---

## Database Session Import

```python
from sqlalchemy.orm import Session
```

Purpose:

Creates database session type.

Used for:

```python
db: Session
```

This tells FastAPI:

```text
Database session expected
```

---

## Requests Import

```python
import requests
```

Purpose:

Checks whether URL is alive.

Example:

```python
requests.get("https://google.com")
```

This sends HTTP request.

---

## Import Database

```python
from .database import SessionLocal
```

Purpose:

Imports session creator.

Needed for:

Database connection.

---

## Import Model

```python
from .models import Monitor
```

Purpose:

Imports database table.

Used for:

```python
db.query(Monitor)
```

---

## Import Schemas

```python
from .schemas import (
    MonitorCreate,
    MonitorResponse
)
```

Purpose:

Used for:

Request validation.

Response validation.

---

# Router Creation

## Code

```python
router = APIRouter()
```

---

## Purpose

Creates route manager.

Instead of:

```python
app.post()
```

we use:

```python
router.post()
```

Later imported in:

```python
main.py
```

---

# Database Dependency

## Code

```python
def get_db():
```

---

## Purpose

Creates database session.

Every request gets:

its own database connection.

---

### Create Session

```python
db = SessionLocal()
```

Creates DB connection.

---

### Yield

```python
yield db
```

Temporarily gives session.

FastAPI uses it.

---

### Finally Block

```python
db.close()
```

Closes database.

Why?

Avoid memory leaks.

Without this:

Too many connections open.

---

## Internal Workflow

```text
Request Comes
      ↓
Session Created
      ↓
API Executes
      ↓
Database Closes
```

---

# API 1 — Create Monitor

## Code

```python
@router.post(
    "/monitor"
)
```

---

## Purpose

Creates URL monitor.

Endpoint:

```http
POST /monitor
```

---

## Request Body

Example:

```json
{
    "url":
    "https://google.com"
}
```

---

## Response Model

```python
response_model=MonitorResponse
```

Ensures clean JSON response.

---

## Create Monitor Function

```python
def create_monitor()
```

---

### Request Validation

```python
monitor: MonitorCreate
```

Uses schema.

Validates request.

---

### Database Injection

```python
db: Session = Depends(get_db)
```

Injects database automatically.

---

### Create Object

```python
new_monitor = Monitor(
    url=monitor.url
)
```

Creates database object.

---

### Add Record

```python
db.add(new_monitor)
```

Adds object.

But NOT saved yet.

---

### Commit

```python
db.commit()
```

Saves permanently.

---

### Refresh

```python
db.refresh(new_monitor)
```

Fetches latest DB values.

Especially:

```text
id
```

---

### Return

```python
return new_monitor
```

Returns response.

---

## Example Response

```json
{
    "id": 1,
    "url":
    "https://google.com",
    "status":
    "Unknown"
}
```

---

# API 2 — Get All Monitors

## Endpoint

```http
GET /monitors
```

---

## Purpose

Fetches all URLs.

---

## Query

```python
db.query(Monitor).all()
```

Equivalent SQL:

```sql
SELECT * FROM monitors;
```

---

## Response Example

```json
[
  {
    "id": 1,
    "url":
    "https://google.com",
    "status":
    "Healthy"
  }
]
```

---

# API 3 — Check URL Health

## Endpoint

```http
GET /check/{monitor_id}
```

Example:

```http
/check/1
```

---

## Purpose

Checks URL health.

---

## Fetch Record

```python
db.query(
    Monitor
)
```

Gets monitor.

---

## Filter

```python
Monitor.id == monitor_id
```

Equivalent SQL:

```sql
WHERE id = 1
```

---

## First Record

```python
.first()
```

Returns first match.

---

## URL Request

```python
requests.get()
```

Makes HTTP request.

---

## Healthy Case

```python
status_code == 200
```

Means:

Website alive.

Status:

```text
Healthy
```

---

## Failure Case

Status:

```text
Down
```

---

## Commit Status

```python
db.commit()
```

Saves latest status.

---

## Example Response

Healthy:

```json
{
    "url":
    "https://google.com",
    "status":
    "Healthy"
}
```

Down:

```json
{
    "url":
    "https://badsite.com",
    "status":
    "Down"
}
```

---

# Internal Workflow

```text
Client Request
      ↓
Route Hit
      ↓
Schema Validation
      ↓
Database Query
      ↓
HTTP Health Check
      ↓
Status Update
      ↓
Response Returned
```

---

# Expected Swagger Output

Open:

```text
/docs
```

You should see:

### POST

```text
/monitor
```

---

### GET

```text
/monitors
```

---

### GET

```text
/check/{monitor_id}
```

---

# File: `app/routes.py`

## Purpose of This File

The `routes.py` file contains the **API endpoints (routes)** and application business logic.

This file is responsible for:

- Creating URL monitors
- Fetching monitoring data
- Checking URL health
- Updating monitoring status
- Communicating with database

Think of this file as:

```text
Client Request
      ↓
routes.py
      ↓
Database
      ↓
Response
```

Without this file:

❌ APIs will not exist  
❌ No CRUD operations  
❌ No URL monitoring

This is the **heart of the FastAPI application**.

---

# Complete Code

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import requests

from .database import SessionLocal
from .models import Monitor
from .schemas import (
    MonitorCreate,
    MonitorResponse
)

router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post(
    "/monitor",
    response_model=MonitorResponse
)
def create_monitor(
    monitor: MonitorCreate,
    db: Session = Depends(get_db)
):

    new_monitor = Monitor(
        url=monitor.url
    )

    db.add(new_monitor)

    db.commit()

    db.refresh(new_monitor)

    return new_monitor


@router.get(
    "/monitors",
    response_model=list[MonitorResponse]
)
def get_monitors(
    db: Session = Depends(get_db)
):

    return db.query(Monitor).all()


@router.get("/check/{monitor_id}")
def check_url(
    monitor_id: int,
    db: Session = Depends(get_db)
):

    monitor = db.query(
        Monitor
    ).filter(
        Monitor.id == monitor_id
    ).first()

    if not monitor:
        return {
            "error":
            "Monitor not found"
        }

    try:

        response = requests.get(
            monitor.url,
            timeout=5
        )

        if response.status_code == 200:
            monitor.status = "Healthy"
        else:
            monitor.status = "Down"

    except:

        monitor.status = "Down"

    db.commit()

    return {
        "url": monitor.url,
        "status": monitor.status
    }
```

---

# Understanding the Code Line by Line

---

# Imports

---

## FastAPI Imports

```python
from fastapi import APIRouter, Depends
```

### Purpose

Imports FastAPI tools.

---

### `APIRouter`

Used to create API routes.

Instead of writing all APIs in:

```python
main.py
```

we separate them.

Example:

```python
router = APIRouter()
```

helps organize endpoints.

---

### `Depends`

Used for:

```text
Dependency Injection
```

Example:

Database session injection.

Instead of manually creating DB connection every time:

FastAPI injects automatically.

---

## Database Session Import

```python
from sqlalchemy.orm import Session
```

Purpose:

Creates database session type.

Used for:

```python
db: Session
```

This tells FastAPI:

```text
Database session expected
```

---

## Requests Import

```python
import requests
```

Purpose:

Checks whether URL is alive.

Example:

```python
requests.get("https://google.com")
```

This sends HTTP request.

---

## Import Database

```python
from .database import SessionLocal
```

Purpose:

Imports session creator.

Needed for:

Database connection.

---

## Import Model

```python
from .models import Monitor
```

Purpose:

Imports database table.

Used for:

```python
db.query(Monitor)
```

---

## Import Schemas

```python
from .schemas import (
    MonitorCreate,
    MonitorResponse
)
```

Purpose:

Used for:

Request validation.

Response validation.

---

# Router Creation

## Code

```python
router = APIRouter()
```

---

## Purpose

Creates route manager.

Instead of:

```python
app.post()
```

we use:

```python
router.post()
```

Later imported in:

```python
main.py
```

---

# Database Dependency

## Code

```python
def get_db():
```

---

## Purpose

Creates database session.

Every request gets:

its own database connection.

---

### Create Session

```python
db = SessionLocal()
```

Creates DB connection.

---

### Yield

```python
yield db
```

Temporarily gives session.

FastAPI uses it.

---

### Finally Block

```python
db.close()
```

Closes database.

Why?

Avoid memory leaks.

Without this:

Too many connections open.

---

## Internal Workflow

```text
Request Comes
      ↓
Session Created
      ↓
API Executes
      ↓
Database Closes
```

---

# API 1 — Create Monitor

## Code

```python
@router.post(
    "/monitor"
)
```

---

## Purpose

Creates URL monitor.

Endpoint:

```http
POST /monitor
```

---

## Request Body

Example:

```json
{
    "url":
    "https://google.com"
}
```

---

## Response Model

```python
response_model=MonitorResponse
```

Ensures clean JSON response.

---

## Create Monitor Function

```python
def create_monitor()
```

---

### Request Validation

```python
monitor: MonitorCreate
```

Uses schema.

Validates request.

---

### Database Injection

```python
db: Session = Depends(get_db)
```

Injects database automatically.

---

### Create Object

```python
new_monitor = Monitor(
    url=monitor.url
)
```

Creates database object.

---

### Add Record

```python
db.add(new_monitor)
```

Adds object.

But NOT saved yet.

---

### Commit

```python
db.commit()
```

Saves permanently.

---

### Refresh

```python
db.refresh(new_monitor)
```

Fetches latest DB values.

Especially:

```text
id
```

---

### Return

```python
return new_monitor
```

Returns response.

---

## Example Response

```json
{
    "id": 1,
    "url":
    "https://google.com",
    "status":
    "Unknown"
}
```

---

# API 2 — Get All Monitors

## Endpoint

```http
GET /monitors
```

---

## Purpose

Fetches all URLs.

---

## Query

```python
db.query(Monitor).all()
```

Equivalent SQL:

```sql
SELECT * FROM monitors;
```

---

## Response Example

```json
[
  {
    "id": 1,
    "url":
    "https://google.com",
    "status":
    "Healthy"
  }
]
```

---

# API 3 — Check URL Health

## Endpoint

```http
GET /check/{monitor_id}
```

Example:

```http
/check/1
```

---

## Purpose

Checks URL health.

---

## Fetch Record

```python
db.query(
    Monitor
)
```

Gets monitor.

---

## Filter

```python
Monitor.id == monitor_id
```

Equivalent SQL:

```sql
WHERE id = 1
```

---

## First Record

```python
.first()
```

Returns first match.

---

## URL Request

```python
requests.get()
```

Makes HTTP request.

---

## Healthy Case

```python
status_code == 200
```

Means:

Website alive.

Status:

```text
Healthy
```

---

## Failure Case

Status:

```text
Down
```

---

## Commit Status

```python
db.commit()
```

Saves latest status.

---

## Example Response

Healthy:

```json
{
    "url":
    "https://google.com",
    "status":
    "Healthy"
}
```

Down:

```json
{
    "url":
    "https://badsite.com",
    "status":
    "Down"
}
```

---

# Internal Workflow

```text
Client Request
      ↓
Route Hit
      ↓
Schema Validation
      ↓
Database Query
      ↓
HTTP Health Check
      ↓
Status Update
      ↓
Response Returned
```

---

# Expected Swagger Output

Open:

```text
/docs
```

You should see:

### POST

```text
/monitor
```

---

### GET

```text
/monitors
```

---

### GET

```text
/check/{monitor_id}
```

---

# File: `app/s3_service.py`

## Purpose of This File

The `s3_service.py` file is responsible for:

- Uploading monitoring reports to AWS S3
- Generating backup JSON files
- Connecting FastAPI with cloud storage
- Triggering AWS Lambda automatically

This file enables:

```text
FastAPI
     ↓
Generate Report
     ↓
Upload to S3
     ↓
Lambda Trigger
     ↓
CloudWatch Logs
```

Without this file:

❌ No cloud backups  
❌ No S3 integration  
❌ No Lambda automation  
❌ Monitoring data remains local only

This introduces:

```text
Serverless + Cloud Storage
```

concepts into the project.

---

# Complete Code

```python
import boto3
import json

from datetime import datetime


s3 = boto3.client("s3")


BUCKET_NAME = (
    "your-bucket-name"
)


def upload_monitor_report(data):

    filename = (
        f"report_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        ".json"
    )

    with open(
        filename,
        "w"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )

    s3.upload_file(
        filename,
        BUCKET_NAME,
        filename
    )

    return {
        "message":
        "Uploaded successfully",

        "file":
        filename
    }
```

---

# Understanding the Code Line by Line

---

# Import 1 — boto3

## Code

```python
import boto3
```

---

## Purpose

`boto3` is:

```text
AWS SDK for Python
```

It allows Python applications to communicate with:

- EC2
- S3
- Lambda
- CloudWatch
- DynamoDB
- IAM

In this project:

We use it for:

```text
AWS S3
```

---

## Why Needed

Without boto3:

Python cannot talk to AWS.

No upload possible.

---

## Installation

Install:

```bash
pip install boto3
```

---

# Import 2 — json

## Code

```python
import json
```

---

## Purpose

Used to create:

```text
JSON report files
```

Example:

Generated file:

```json
{
    "status": "healthy",
    "cpu": 22.4
}
```

---

# Import 3 — datetime

## Code

```python
from datetime import datetime
```

---

## Purpose

Used to create:

```text
unique timestamped filenames
```

Example:

```text
report_20260824_154512.json
```

This prevents:

❌ File overwriting

---

# Create S3 Client

## Code

```python
s3 = boto3.client("s3")
```

---

## Purpose

Creates:

```text
AWS S3 connection client
```

Think:

```text
Python App
       ↓
boto3 Client
       ↓
AWS S3
```

---

## What Happens Internally

boto3 automatically checks:

```text
AWS Credentials
```

from:

```text
~/.aws/credentials
```

or:

```text
IAM Role
```

on EC2.

---

# Bucket Name

## Code

```python
BUCKET_NAME =
"your-bucket-name"
```

---

## Purpose

Defines target S3 bucket.

Example:

```python
BUCKET_NAME =
"cloud-url-monitor-sasmita-2026"
```

---

## Important Rule

S3 bucket names must be:

```text
Globally Unique
```

Bad:

```text
cloud-url-monitor
```

Good:

```text
cloud-url-monitor-sasmita-2026
```

---

# Upload Function

## Code

```python
def upload_monitor_report(data):
```

---

## Purpose

Handles:

```text
Backup Creation
+
S3 Upload
```

Input:

```python
data
```

Example:

```python
{
    "status": "healthy",
    "cpu": 22
}
```

---

# Generate Filename

## Code

```python
filename = (
    f"report_"
    f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    ".json"
)
```

---

## Purpose

Creates unique file name.

Example:

```text
report_20260824_121314.json
```

---

## Why Timestamp?

Without timestamp:

Every upload:

```text
report.json
```

would overwrite previous file.

Timestamp solves this.

---

# Create Local JSON File

## Code

```python
with open(
    filename,
    "w"
) as file:
```

---

## Purpose

Creates local file.

Example:

```text
report_20260824.json
```

---

### `"w"`

Means:

```text
Write mode
```

Creates new file.

---

# Write JSON Data

## Code

```python
json.dump(
    data,
    file,
    indent=4
)
```

---

## Purpose

Converts Python dictionary:

```python
{
    "cpu": 20
}
```

into JSON file.

---

## `indent=4`

Makes JSON readable.

Example:

Bad:

```json
{"cpu":20}
```

Good:

```json
{
    "cpu": 20
}
```

---

# Upload to S3

## Code

```python
s3.upload_file(
    filename,
    BUCKET_NAME,
    filename
)
```

---

## Purpose

Uploads file.

---

## Parameters

### First Parameter

```python
filename
```

Local file path.

Example:

```text
report.json
```

---

### Second Parameter

```python
BUCKET_NAME
```

Target bucket.

Example:

```text
cloud-url-monitor-sasmita
```

---

### Third Parameter

```python
filename
```

Object name in S3.

File appears as:

```text
report_20260824.json
```

---

## Internal Workflow

```text
FastAPI
      ↓
Create JSON
      ↓
boto3 Upload
      ↓
AWS S3
      ↓
Object Stored
```

---

# Return Response

## Code

```python
return {
```

---

## Purpose

Returns upload confirmation.

Example:

```json
{
    "message":
    "Uploaded successfully",

    "file":
    "report_20260824.json"
}
```

---

# Example API Flow

Endpoint:

```http
POST /backup
```

---

Request:

```text
Trigger backup
```

---

Flow:

```text
main.py
      ↓
s3_service.py
      ↓
Create JSON Report
      ↓
Upload To S3
      ↓
Lambda Triggered
      ↓
CloudWatch Logs
```

---

# Expected Output

API response:

```json
{
  "message":
  "Uploaded successfully",

  "file":
  "report_20260824.json"
}
```

---

## Verify in AWS

Go:

```text
S3 Bucket
```

Expected:

```text
report_20260824.json
```

uploaded.

---

# Lambda Trigger

If Lambda configured:

Upload automatically triggers:

```text
AWS Lambda
```

Event:

```text
Object Created
```

Lambda executes automatically.

---

# File: `Dockerfile`

## Purpose of This File

The `Dockerfile` is responsible for:

```text
Packaging the entire application
inside a container
```

It defines:

- Base operating system
- Python environment
- Dependencies installation
- Project copy
- Exposed port
- Startup command

Architecture:

```text
Source Code
      ↓
Dockerfile
      ↓
Docker Image
      ↓
Docker Container
      ↓
Kubernetes Deployment
```

---

# Complete Code

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD [
    "uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
]
```

---

# Understanding the Code Line by Line

---

# Step 1 — Base Image

## Code

```dockerfile
FROM python:3.11-slim
```

---

## Purpose

Defines:

```text
Base Operating Environment
```

This image already contains:

```text
Python 3.11
```

installed.

Docker downloads this image automatically.

---

## Why Python Slim?

We use:

```text
slim
```

because:

✅ Lightweight  
✅ Faster build  
✅ Smaller image size  
✅ Better for production

---

## What Happens Internally

Docker checks:

```text
Do I already have image?
```

If no:

Downloads from:

```text
Docker Hub
```

---

## Internal Workflow

```text
Dockerfile Starts
        ↓
Pull python:3.11-slim
        ↓
Create container environment
```

---

# Step 2 — Working Directory

## Code

```dockerfile
WORKDIR /app
```

---

## Purpose

Sets:

```text
Default folder
inside container
```

Everything runs from:

```text
/app
```

Think:

Inside container:

```text
/app
```

becomes:

project root.

---

## Why Needed

Without this:

Docker commands execute randomly.

Can break project paths.

---

## Internal Workflow

```text
Container Starts
        ↓
Move to /app
        ↓
Execute remaining commands
```

---

# Step 3 — Copy Requirements File

## Code

```dockerfile
COPY requirements.txt .
```

---

## Purpose

Copies:

```text
requirements.txt
```

into container.

---

## Why First?

This is an optimization trick.

Docker caching improves speed.

If requirements don't change:

Docker skips reinstalling packages.

Faster builds.

---

## Internal Workflow

```text
Local Machine
        ↓
requirements.txt
        ↓
Docker Container
```

---

# Step 4 — Install Dependencies

## Code

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

---

## Purpose

Installs project dependencies.

Same as running:

```bash
pip install -r requirements.txt
```

locally.

---

## Understanding Parameters

### `RUN`

Executes command inside image.

---

### `pip install`

Installs Python packages.

---

### `--no-cache-dir`

Prevents cache storage.

Benefits:

✅ Smaller image size  
✅ Less memory usage

---

### `-r requirements.txt`

Reads dependency file.

Installs all packages.

---

## Internal Workflow

```text
requirements.txt
        ↓
pip install
        ↓
Packages Downloaded
        ↓
Environment Ready
```

---

# Step 5 — Copy Project Files

## Code

```dockerfile
COPY . .
```

---

## Purpose

Copies:

```text
Entire backend folder
```

into container.

Includes:

- app/
- Dockerfile
- requirements.txt

---

## Internal Workflow

```text
Local Project
       ↓
Docker Build
       ↓
Copied to /app
```

---

# Step 6 — Expose Port

## Code

```dockerfile
EXPOSE 8000
```

---

## Purpose

Tells Docker:

```text
Application uses port 8000
```

FastAPI runs here.

---

## Why Needed

Helps:

- Docker networking
- Kubernetes service mapping
- Documentation clarity

---

## Internal Workflow

```text
Container
      ↓
Port 8000 Open
      ↓
Traffic Allowed
```

---

# Step 7 — Start Command

## Code

```dockerfile
CMD [
    "uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
]
```

---

## Purpose

Defines:

```text
How container starts
```

Equivalent local command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Understanding Parameters

### `uvicorn`

ASGI server.

Runs FastAPI.

---

### `app.main:app`

Meaning:

```text
folder.file:object
```

Location:

```text
app/main.py
```

Object:

```python
app = FastAPI()
```

---

### `--host 0.0.0.0`

Very important.

Allows:

```text
External access
```

Without this:

App inaccessible outside container.

Bad:

```text
localhost only
```

Good:

```text
accessible everywhere
```

---

### `--port 8000`

Runs FastAPI on:

```text
8000
```

---

# What Happens Internally

Docker startup:

```text
Container Starts
       ↓
Move to /app
       ↓
Run Uvicorn
       ↓
FastAPI Starts
       ↓
Port 8000 Active
```

---

# Build Docker Image

## Command

```bash
docker build -t cloud-url-monitor .
```

---

## Breakdown

### `docker build`

Build image.

---

### `-t`

Tag image.

---

### `cloud-url-monitor`

Image name.

---

### `.`

Current folder.

---

# Expected Output

Successful build:

```text
Successfully tagged
cloud-url-monitor:latest
```

---

# Verify Image

Run:

```bash
docker images
```

Expected:

```text
cloud-url-monitor
```

visible.

---

# Run Container

## Command

```bash
docker run -d -p 8000:8000 cloud-url-monitor
```

---

## Breakdown

### `-d`

Detached mode.

Runs background.

---

### `-p 8000:8000`

Port mapping.

Meaning:

```text
Local 8000 → Container 8000
```

---

# Verify Running Container

Command:

```bash
docker ps
```

Expected:

```text
cloud-url-monitor
```

running.

---

# Test Application

Browser:

## Home

```text
http://localhost:8000
```

Expected:

```json
{
  "message":
  "Cloud URL Monitor Running"
}
```

---

## Swagger

```text
http://localhost:8000/docs
```

---

## Metrics

```text
http://localhost:8000/metrics
```

---

