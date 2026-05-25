# AWS Lambda for URL Health Monitoring

This section explains:

```text
How AWS Lambda automatically
checks application health
```

including:

- Lambda function
- URL monitoring
- health checks
- S3 report storage
- EventBridge scheduling
- CloudWatch logs
- debugging
- common errors

---

# Why Use Lambda?

Without Lambda:

```text
Manual Monitoring
        ↓
Open Browser
        ↓
Check API Status
```

Manual work.

With Lambda:

```text
Automatic Health Check
          ↓
Runs Every Few Minutes
          ↓
Checks API Status
          ↓
Stores Monitoring Report
```

Benefits:

- Serverless  
- Automatic monitoring  
- AWS-native architecture  
- Cost efficient  
- No server management

---

# Lambda Architecture

Your monitoring flow:

```text
EventBridge Scheduler
          ↓
Lambda Function
          ↓
Health API Check
          ↓
Response Analysis
          ↓
S3 Storage
          ↓
Logs Generated
```

---

# Project Structure

```text
lambda/
│
├── lambda_function.py
└── README.md
```

---

# File: `lambda_function.py`

## Purpose

This function:

```text
Checks FastAPI health endpoint
and stores monitoring report
```

---

# Complete Code

```python
import json
import boto3
import requests
from datetime import datetime

s3 = boto3.client("s3")

BUCKET_NAME = "cloud-url-monitor-reports-12345"

URL_TO_CHECK = "http://YOUR_EC2_IP:8000/health"


def lambda_handler(event, context):

    try:
        response = requests.get(URL_TO_CHECK)

        status_code = response.status_code

        if status_code == 200:
            health_status = "UP"
        else:
            health_status = "DOWN"

    except Exception as e:
        health_status = "ERROR"
        status_code = str(e)

    report = {
        "timestamp":
        str(datetime.utcnow()),

        "url":
        URL_TO_CHECK,

        "status":
        health_status,

        "response":
        status_code
    }

    file_name = (
        f"reports/"
        f"health_report_"
        f"{datetime.utcnow()}.json"
    )

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=file_name,
        Body=json.dumps(report)
    )

    return {
        "statusCode": 200,
        "body": json.dumps(report)
    }
```

---

# Understanding the Code Line by Line

---

# Import Libraries

## Code

```python
import json
```

Purpose:

```text
Converts Python data
to JSON format
```

---

## Code

```python
import boto3
```

Purpose:

```text
AWS SDK for Python
```

Used for:

```text
S3 interaction
```

---

## Code

```python
import requests
```

Purpose:

```text
HTTP request library
```

Used to check:

```text
FastAPI health endpoint
```

---

## Code

```python
from datetime import datetime
```

Purpose:

```text
Generate timestamps
```

for monitoring reports.

---

# Create S3 Client

## Code

```python
s3 =
boto3.client("s3")
```

Purpose:

Connects Lambda to:

```text
AWS S3
```

---

# Bucket Name

## Code

```python
BUCKET_NAME =
"cloud-url-monitor-reports-12345"
```

Purpose:

Defines:

```text
Where reports are stored
```

---

# URL To Monitor

## Code

```python
URL_TO_CHECK =
"http://YOUR_EC2_IP:8000/health"
```

Replace:

```text
YOUR_EC2_IP
```

with:

```text
Terraform output IP
```

Example:

```text
http://44.xx.xx.xx:8000/health
```

---

# Lambda Entry Function

## Code

```python
def lambda_handler(
event,
context
):
```

Purpose:

Main function executed by AWS Lambda.

Think:

```text
main()
```

for Lambda.

---

# API Health Check

## Code

```python
requests.get()
```

Purpose:

Checks if API is:

```text
reachable
```

---

# Status Code

## Code

```python
response.status_code
```

Purpose:

Checks:

```text
200 OK
```

means:

```text
Application healthy
```

---

# Health Status Logic

If:

```text
200
```

Then:

```text
UP
```

Else:

```text
DOWN
```

---

# Exception Handling

If API unreachable:

Example:

```text
timeout
server down
DNS failure
```

Lambda records:

```text
ERROR
```

instead of crashing.

---

# Monitoring Report

Example report:

```json
{
  "timestamp":
  "2026-05-24",

  "url":
  "http://44.xx.xx.xx:8000/health",

  "status":
  "UP",

  "response":
  200
}
```

---

# File Naming

Example:

```text
reports/
health_report_
2026-05-24.json
```

Stored in:

```text
S3 bucket
```

---

# Upload To S3

## Code

```python
s3.put_object()
```

Purpose:

Uploads report to S3.

---

# Internal Workflow

```text
Health Check
      ↓
Generate Report
      ↓
Create JSON
      ↓
Upload To S3
```

---

# Deploy Lambda

Go:

```text
AWS Console
      ↓
Lambda
      ↓
Create Function
```

Choose:

```text
Author from scratch
```

---

## Function Name

```text
url-health-monitor
```

---

## Runtime

Choose:

```text
Python 3.12
```

---

# Add Code

Paste:

```text
lambda_function.py
```

Deploy.

---

# Add Dependency Layer

Because:

```python
requests
```

is external.

Need Lambda layer.

Create zip:

```bash
pip install requests -t python/
zip -r requests-layer.zip python
```

Upload as:

```text
Lambda Layer
```

Attach to function.

---

# IAM Permission

Lambda needs:

```text
S3 Write Access
```

Attach policy:

```text
AmazonS3FullAccess
```

(learning project)

---

# Create EventBridge Trigger

Go:

```text
EventBridge
      ↓
Create Rule
```

Schedule:

```text
Rate Expression
```

Example:

```text
every 5 minutes
```

Equivalent:

```text
rate(5 minutes)
```

---

# Workflow

Real monitoring flow:

```text
Every 5 Minutes
        ↓
EventBridge Trigger
        ↓
Lambda Starts
        ↓
Checks FastAPI Health
        ↓
Stores Report In S3
```

---

# Testing Lambda

Click:

```text
Test
```

Expected output:

```json
{
  "statusCode": 200
}
```

---

# Verify S3

Go:

```text
S3 Bucket
      ↓
reports/
```

Expected:

```text
health_report_xxx.json
```

---

# CloudWatch Logs

Go:

```text
CloudWatch
      ↓
Log Groups
```

Expected:

```text
Lambda Logs
```

---

