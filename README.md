# Cloud-Native URL Health Monitoring System

A cloud-native monitoring system built using **FastAPI, Docker, Kubernetes, Terraform, Jenkins, AWS, Prometheus, and Grafana**.

This project monitors URLs, stores monitoring data, exposes API metrics, deploys services using Kubernetes, provisions AWS infrastructure using Terraform, automates deployment through Jenkins CI/CD, and visualizes monitoring metrics using Prometheus and Grafana.

---

# Project Overview

The **Cloud-Native URL Health Monitoring System** is a DevOps-oriented backend application designed to monitor URLs and demonstrate modern cloud-native deployment practices.

The project focuses on:

- Backend API development using FastAPI
- Containerization using Docker
- Kubernetes orchestration
- Infrastructure as Code (IaC) using Terraform
- AWS Cloud deployment
- CI/CD automation using Jenkins
- Monitoring and observability using Prometheus & Grafana
- Cloud storage and serverless integration using S3 and AWS Lambda

---

# Project Objectives

The major objectives of this project are:

### 1. Build a FastAPI Monitoring API

Create a lightweight monitoring backend capable of:

- Adding URLs
- Monitoring health
- Viewing analytics
- Exposing metrics

---

### 2. Containerize the Application

Use Docker to:

- Package dependencies
- Ensure consistency
- Enable portability

---

### 3. Deploy using Kubernetes

Use Kubernetes for:

- Container orchestration
- Replica scaling
- Self-healing
- Service exposure

---

### 4. Provision AWS Infrastructure

Use Terraform to automate:

- EC2 creation
- Security groups
- EBS storage
- S3 buckets

---

### 5. Implement CI/CD

Use Jenkins to automate:

```text
Code Push
    ↓
Build
    ↓
Deploy
    ↓
Restart Services
```

---

### 6. Implement Monitoring

Use:

- Prometheus → Metrics Collection
- Grafana → Visualization

---

### 7. Use AWS Native Services

Integrate:

- AWS Lambda
- S3 Storage
- CloudWatch Logs

---

# Key Features

## FastAPI Backend

- URL monitoring
- REST APIs
- Health endpoints
- Metrics endpoint

---

## Docker

- Containerized deployment
- Consistent runtime
- Environment portability

---

## Kubernetes

- Deployment
- Scaling
- Services
- Self-healing containers

---

## Monitoring

### Prometheus

Collects:

- Request count
- Response times
- CPU usage
- Application metrics

### Grafana

Visualizes:

- API metrics
- Kubernetes metrics
- CPU and memory
- Monitoring dashboards

---

## AWS Infrastructure

### EC2

Hosts application infrastructure.

### EBS

Persistent storage.

### S3

Stores monitoring reports.

### Lambda

Handles serverless automation.

---

## Jenkins CI/CD

Automates deployment pipeline.

---

# High-Level Architecture

```text
                    Developer
                        │
                        ▼
                    GitHub Repo
                        │
                        ▼
                     Jenkins
                        │
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
 Docker Build     Kubernetes Deploy   Restart Pods
       │
       ▼
     AWS EC2
       │
       ▼
 Kubernetes Cluster
       │
 ┌─────┴─────────┐
 ▼               ▼
FastAPI       Monitoring Stack
Backend       (Prometheus + Grafana)
     │
     ▼
 AWS S3 Bucket
     │
     ▼
 AWS Lambda Trigger
```

---

# Project Workflow

## Phase 1 — Backend Development

Build FastAPI backend.

Features:

- Add URL
- Monitor URL
- Analytics
- Health check

---

## Phase 2 — Dockerization

Containerize application.

Workflow:

```text
Source Code
     ↓
Dockerfile
     ↓
Docker Image
     ↓
Docker Container
```

---

## Phase 3 — Kubernetes Deployment

Deploy application using:

- Deployment
- Service
- Replica scaling

Workflow:

```text
Docker Image
      ↓
Kubernetes Deployment
      ↓
Pods
      ↓
Kubernetes Service
```

---

## Phase 4 — Monitoring

Prometheus scrapes metrics.

Grafana visualizes metrics.

Workflow:

```text
FastAPI Metrics
        ↓
Prometheus
        ↓
Grafana Dashboard
```

---

## Phase 5 — Terraform Infrastructure

Provision AWS resources automatically.

Workflow:

```text
Terraform Code
        ↓
AWS API
        ↓
EC2 + Security Group + EBS
```

---

## Phase 6 — AWS Deployment

Deploy Kubernetes setup on AWS EC2.

---

## Phase 7 — Jenkins CI/CD

Automated deployment.

Workflow:

```text
Git Push
    ↓
Jenkins Trigger
    ↓
Build Docker Image
    ↓
Deploy to Kubernetes
```

---

## Phase 8 — S3 + Lambda Automation

Monitoring reports uploaded to S3.

Lambda triggers automatically.

Workflow:

```text
FastAPI
    ↓
Generate Report
    ↓
Upload to S3
    ↓
Lambda Trigger
```

---

# Technology Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | Backend API |
| SQLite | Database |
| Docker | Containerization |
| Kubernetes | Orchestration |
| Terraform | Infrastructure as Code |
| Jenkins | CI/CD |
| AWS EC2 | Compute |
| AWS EBS | Storage |
| AWS S3 | Object Storage |
| AWS Lambda | Serverless |
| Prometheus | Monitoring |
| Grafana | Visualization |

---

# Project Structure

```text
cloud-url-monitor-project/
│
├── backend/
│   ├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── kubernetes/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── README.md
│
├── monitoring/
│   ├── prometheus-config.yaml
│   ├── grafana-deployment.yaml
│   └── README.md
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── README.md
│
├── Jenkinsfile
│
└── README.md
```

---
