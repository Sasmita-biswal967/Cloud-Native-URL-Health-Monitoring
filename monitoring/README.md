# File: `prometheus-deployment.yaml`

## Purpose of This File

The `prometheus-deployment.yaml` file is responsible for:

- Deploying Prometheus inside Kubernetes
- Collecting application metrics
- Scraping FastAPI `/metrics`
- Storing time-series monitoring data
- Making observability possible

Think:

```text
FastAPI App
      ↓
/metrics endpoint
      ↓
Prometheus
      ↓
Metrics Database
```

Without Prometheus:

- No monitoring  
- No metrics collection  
- No performance visibility  
- Grafana dashboards won't work

This file creates:

```text
Prometheus Pod
```

inside Kubernetes.

---

# Complete Code

```yaml
apiVersion: apps/v1

kind: Deployment

metadata:
  name: prometheus

  namespace: monitoring

spec:
  replicas: 1

  selector:
    matchLabels:
      app: prometheus

  template:
    metadata:
      labels:
        app: prometheus

    spec:
      containers:
      - name: prometheus

        image: prom/prometheus

        ports:
        - containerPort: 9090

        volumeMounts:
        - name: prometheus-config

          mountPath:
            /etc/prometheus

      volumes:
      - name: prometheus-config

        configMap:
          name:
            prometheus-config
```

---

# Understanding the YAML Line by Line

---

# API Version

## Code

```yaml
apiVersion: apps/v1
```

---

## Purpose

Defines Kubernetes API version.

Prometheus Deployment uses:

```text
apps/v1
```

because:

```text
Deployment resource
```

belongs to:

```text
apps API
```

---

# Kind

## Code

```yaml
kind: Deployment
```

---

## Purpose

Defines:

```text
Resource Type
```

Here:

```text
Deployment
```

means:

```text
Manage Prometheus Pod
```

Benefits:

- Auto restart  
- Self-healing  
- Scaling support

---

# Metadata

## Code

```yaml
metadata:
```

---

## Purpose

Stores:

```text
Deployment identity
```

---

## Name

```yaml
name: prometheus
```

---

### Purpose

Deployment name.

Used in commands.

Example:

```bash
kubectl get deployment -n monitoring
```

Expected:

```text
prometheus
```

---

# Namespace

## Code

```yaml
namespace: monitoring
```

---

## Purpose

Deploys Prometheus in:

```text
monitoring namespace
```

instead of:

```text
default namespace
```

---

## Why Namespace?

Separates monitoring tools.

Cleaner architecture.

Example:

```text
default namespace
      ↓
Application Pods

monitoring namespace
      ↓
Prometheus
Grafana
```

---

## Verify Namespace

Command:

```bash
kubectl get ns
```

Expected:

```text
monitoring
```

---

# Spec Section

## Code

```yaml
spec:
```

---

## Purpose

Defines:

```text
Deployment behavior
```

Contains:

- replicas
- selectors
- pod template
- containers
- volumes

---

# Replicas

## Code

```yaml
replicas: 1
```

---

## Purpose

Runs:

```text
1 Prometheus pod
```

---

## Why Only 1?

Prometheus is lightweight for this project.

Enough for:

```text
Single Kubernetes Cluster
```

---

## Internal Workflow

```text
Deployment
      ↓
ReplicaSet
      ↓
1 Pod Created
```

---

# Selector

## Code

```yaml
selector:
```

---

## Purpose

Finds Prometheus pods.

Deployment needs labels.

---

# Match Labels

## Code

```yaml
matchLabels:
  app: prometheus
```

---

## Purpose

Connects deployment to pod.

Think:

```text
Pod Tag
```

Deployment searches:

```text
app=prometheus
```

---

# Template Section

## Code

```yaml
template:
```

---

## Purpose

Defines:

```text
Blueprint for Pod
```

Every Prometheus pod follows this configuration.

---

# Pod Labels

## Code

```yaml
labels:
  app: prometheus
```

---

## Purpose

Assigns pod label.

Needed for:

```text
Selectors
Services
```

---

# Container Section

## Code

```yaml
containers:
```

---

## Purpose

Defines:

```text
Container settings
```

Includes:

- image
- ports
- volume mounts

---

# Container Name

## Code

```yaml
name: prometheus
```

---

## Purpose

Container identifier.

Used for:

```bash
kubectl logs
```

---

# Docker Image

## Code

```yaml
image: prom/prometheus
```

---

## Purpose

Official Prometheus image.

Pulled automatically from:

```text
Docker Hub
```

---

## Internal Workflow

```text
Kubernetes
      ↓
Docker Hub
      ↓
Download Image
      ↓
Create Container
```

---

# Container Port

## Code

```yaml
containerPort: 9090
```

---

## Purpose

Prometheus runs on:

```text
Port 9090
```

---

## Access Example

Browser:

```text
http://localhost:9090
```

or:

```text
minikube service
```

---

# Volume Mounts

## Code

```yaml
volumeMounts:
```

---

## Purpose

Mounts configuration files.

Prometheus needs:

```text
prometheus.yml
```

for scraping rules.

---

# Volume Name

## Code

```yaml
name: prometheus-config
```

---

## Purpose

References config volume.

---

# Mount Path

## Code

```yaml
mountPath:
  /etc/prometheus
```

---

## Purpose

Mounts configuration at:

```text
/etc/prometheus
```

inside container.

Prometheus automatically reads config here.

---

## Internal Workflow

```text
ConfigMap
      ↓
Mounted Volume
      ↓
/etc/prometheus
      ↓
Prometheus Reads Config
```

---

# Volumes Section

## Code

```yaml
volumes:
```

---

## Purpose

Creates persistent mounted config.

---

# ConfigMap

## Code

```yaml
configMap:
  name:
    prometheus-config
```

---

## Purpose

Loads:

```text
prometheus-config ConfigMap
```

which contains:

```text
prometheus.yml
```

scrape configuration.

Without this:

Prometheus cannot scrape FastAPI.

---

# Apply Deployment

## Command

```bash
kubectl apply -f prometheus-deployment.yaml
```

---

## Internal Workflow

```text
kubectl
      ↓
API Server
      ↓
Deployment Created
      ↓
ReplicaSet
      ↓
Prometheus Pod
```

---

# Verify Deployment

Command:

```bash
kubectl get deployment -n monitoring
```

Expected:

```text
prometheus
```

---

# Verify Pods

Command:

```bash
kubectl get pods -n monitoring
```

Expected:

```text
prometheus-xxxxx
Running
```

---

# Describe Pod

Command:

```bash
kubectl describe pod POD_NAME -n monitoring
```

---

# View Logs

Command:

```bash
kubectl logs POD_NAME -n monitoring
```

Expected:

```text
Server is ready to receive requests
```

---

# Access Prometheus

Command:

```bash
minikube service prometheus-service -n monitoring
```

Expected:

Prometheus UI opens.

---

# Verify Metrics Scraping

Inside Prometheus:

Open:

```text
Status → Targets
```

Expected:

```text
UP
```

for:

```text
cloud-url-monitor-service
```

---

# Behind the Scenes

When FastAPI receives traffic:

```text
FastAPI
      ↓
/metrics updated
      ↓
Prometheus scrape
      ↓
Metrics stored
      ↓
Grafana reads data
      ↓
Dashboard updated
```

---

# File: `prometheus-service.yaml`

## Purpose of This File

The `prometheus-service.yaml` file is responsible for:

- Exposing Prometheus outside Kubernetes
- Making Prometheus UI accessible
- Allowing browser access
- Enabling Grafana to query Prometheus

Without Service:

- Prometheus inaccessible  
- Cannot open Prometheus dashboard  
- Grafana cannot connect  
- Metrics invisible

Think:

```text
Prometheus Pod
        ↓
Prometheus Service
        ↓
Browser Access
```

Pods are temporary.

Service provides:

```text
Stable Network Access
```

---

# Complete Code

```yaml
apiVersion: v1

kind: Service

metadata:
  name: prometheus-service

  namespace: monitoring

spec:
  selector:
    app: prometheus

  ports:
    - protocol: TCP
      port: 9090
      targetPort: 9090

  type: NodePort
```

---

# Understanding the YAML Line by Line

---

# API Version

## Code

```yaml
apiVersion: v1
```

---

## Purpose

Defines Kubernetes API version.

For Services:

```text
v1
```

is used.

Unlike deployment:

```yaml
apps/v1
```

Service resources use:

```yaml
v1
```

---

# Kind

## Code

```yaml
kind: Service
```

---

## Purpose

Defines:

```text
Resource Type
```

Here:

```text
Service
```

means:

```text
Expose networking
```

for Prometheus.

---

## Why Needed?

Prometheus pod gets temporary IP.

Example:

Today:

```text
10.244.0.10
```

Tomorrow:

```text
10.244.0.25
```

Unstable.

Service gives:

```text
Permanent Access Point
```

---

# Metadata

## Code

```yaml
metadata:
```

---

## Purpose

Stores:

```text
Service Identity
```

---

## Name

## Code

```yaml
name: prometheus-service
```

---

## Purpose

Service identifier.

Used in commands.

Example:

```bash
kubectl get svc -n monitoring
```

Expected:

```text
prometheus-service
```

---

# Namespace

## Code

```yaml
namespace: monitoring
```

---

## Purpose

Places service in:

```text
monitoring namespace
```

instead of:

```text
default namespace
```

---

## Why Important?

Prometheus deployment exists in:

```text
monitoring
```

Service must be in same namespace.

Otherwise:

❌ Cannot connect to pod.

---

# Spec Section

## Code

```yaml
spec:
```

---

## Purpose

Contains:

```text
Networking configuration
```

Includes:

- selector
- ports
- type

---

# Selector

## Code

```yaml
selector:
  app: prometheus
```

---

## Purpose

Links service to Prometheus pod.

Service searches for:

```text
app=prometheus
```

label.

---

## Internal Workflow

```text
Service
     ↓
Find pod label
app=prometheus
     ↓
Connect pod
```

---

## Important

Must match:

### Deployment Labels

```yaml
labels:
  app: prometheus
```

If mismatch:

❌ No endpoints found.

---

# Ports Section

## Code

```yaml
ports:
```

---

## Purpose

Defines:

```text
Traffic routing
```

---

# Protocol

## Code

```yaml
protocol: TCP
```

---

## Purpose

Defines network protocol.

Prometheus uses:

```text
TCP
```

because HTTP works over TCP.

---

# Port

## Code

```yaml
port: 9090
```

---

## Purpose

Service-facing port.

Prometheus accessible through:

```text
9090
```

---

# Target Port

## Code

```yaml
targetPort: 9090
```

---

## Purpose

Maps request to container.

Prometheus internally runs on:

```text
9090
```

---

## Internal Workflow

```text
Browser Request
        ↓
Service Port 9090
        ↓
Target Port 9090
        ↓
Prometheus Container
```

---

# Service Type

## Code

```yaml
type: NodePort
```

---

## Purpose

Exposes Prometheus externally.

Without NodePort:

Prometheus only accessible inside cluster.

---

## What NodePort Does

Creates external port.

Example:

```text
31984
```

Access:

```text
http://MINIKUBE_IP:31984
```

---

## Internal Workflow

```text
Browser
    ↓
NodePort
    ↓
Service
    ↓
Prometheus Pod
```

---

# Apply Service

## Command

```bash
kubectl apply -f prometheus-service.yaml
```

---

## Internal Workflow

```text
kubectl
      ↓
API Server
      ↓
Service Created
      ↓
Traffic Routing Enabled
```

---

# Verify Service

## Command

```bash
kubectl get svc -n monitoring
```

---

## Expected Output

```text
NAME                  TYPE
prometheus-service    NodePort
```

---

# Describe Service

## Command

```bash
kubectl describe svc prometheus-service -n monitoring
```

---

## Purpose

Shows:

- Ports
- Endpoints
- NodePort
- Labels

---

# Open Prometheus

## Command

```bash
minikube service prometheus-service -n monitoring
```

---

## Purpose

Automatically opens browser.

Expected UI:

```text
Prometheus Dashboard
```

---

# Verify Metrics Collection

Inside Prometheus:

Go:

```text
Status → Targets
```

Expected:

```text
UP
```

for:

```text
cloud-url-monitor-service
```

---

# Test Query

Inside Prometheus query box:

```text
http_requests_total
```

Click:

```text
Execute
```

Expected:

Metrics data appears.

---

# Behind the Scenes

When user opens:

```text
minikube service prometheus-service
```

Flow:

```text
Browser
      ↓
NodePort
      ↓
Service
      ↓
Prometheus Pod
      ↓
Prometheus UI
```

---

# File: `grafana-deployment.yaml`

## Purpose of This File

The `grafana-deployment.yaml` file is responsible for:

- Deploying Grafana in Kubernetes
- Creating Grafana pods
- Visualizing Prometheus metrics
- Building dashboards
- Monitoring system performance

Think:

```text
Prometheus
      ↓
Stores Metrics
      ↓
Grafana
      ↓
Beautiful Dashboards
```

Without Grafana:

- No dashboards  
- Hard to analyze metrics  
- No visualization  
- Monitoring becomes difficult

This file creates:

```text
Grafana Pod
```

inside Kubernetes.

---

# Complete Code

```yaml
apiVersion: apps/v1

kind: Deployment

metadata:
  name: grafana

  namespace: monitoring

spec:
  replicas: 1

  selector:
    matchLabels:
      app: grafana

  template:
    metadata:
      labels:
        app: grafana

    spec:
      containers:
      - name: grafana

        image: grafana/grafana

        ports:
        - containerPort: 3000
```

---

# Understanding the YAML Line by Line

---

# API Version

## Code

```yaml
apiVersion: apps/v1
```

---

## Purpose

Defines Kubernetes API version.

Grafana Deployment uses:

```text
apps/v1
```

because:

```text
Deployment resource
```

belongs to:

```text
apps API
```

---

# Kind

## Code

```yaml
kind: Deployment
```

---

## Purpose

Defines:

```text
Resource Type
```

Here:

```text
Deployment
```

means:

```text
Manage Grafana Pod
```

Benefits:

- Auto restart  
- Self-healing  
- Pod recreation  
- Easy scaling

---

# Metadata

## Code

```yaml
metadata:
```

---

## Purpose

Stores deployment identity.

---

# Name

## Code

```yaml
name: grafana
```

---

## Purpose

Deployment identifier.

Used in commands.

Example:

```bash
kubectl get deployment -n monitoring
```

Expected:

```text
grafana
```

---

# Namespace

## Code

```yaml
namespace: monitoring
```

---

## Purpose

Deploys Grafana in:

```text
monitoring namespace
```

instead of:

```text
default namespace
```

---

## Why Namespace?

Keeps monitoring stack separate.

Example:

```text
default namespace
      ↓
Application Pods

monitoring namespace
      ↓
Prometheus
Grafana
```

Cleaner architecture.

---

# Spec Section

## Code

```yaml
spec:
```

---

## Purpose

Contains deployment configuration.

Includes:

- replicas
- selectors
- pod template
- containers

---

# Replicas

## Code

```yaml
replicas: 1
```

---

## Purpose

Runs:

```text
1 Grafana Pod
```

---

## Why Only 1?

Enough for:

```text
Local Kubernetes Project
```

Simple monitoring setup.

---

## Internal Workflow

```text
Deployment
      ↓
ReplicaSet
      ↓
1 Grafana Pod
```

---

# Selector

## Code

```yaml
selector:
```

---

## Purpose

Helps deployment identify pods.

Uses labels.

---

# Match Labels

## Code

```yaml
matchLabels:
  app: grafana
```

---

## Purpose

Links deployment to Grafana pod.

Deployment searches:

```text
app=grafana
```

---

# Template Section

## Code

```yaml
template:
```

---

## Purpose

Defines:

```text
Pod Blueprint
```

Every Grafana pod follows this template.

---

# Pod Labels

## Code

```yaml
labels:
  app: grafana
```

---

## Purpose

Assigns labels to pods.

Needed for:

- services
- selectors
- networking

---

# Container Section

## Code

```yaml
containers:
```

---

## Purpose

Defines:

```text
Container Configuration
```

Includes:

- image
- ports

---

# Container Name

## Code

```yaml
name: grafana
```

---

## Purpose

Container identifier.

Useful for:

```bash
kubectl logs
```

---

# Docker Image

## Code

```yaml
image: grafana/grafana
```

---

## Purpose

Official Grafana image.

Automatically downloaded from:

```text
Docker Hub
```

---

## Internal Workflow

```text
Kubernetes
      ↓
Docker Hub
      ↓
Download Grafana Image
      ↓
Create Container
```

---

# Container Port

## Code

```yaml
containerPort: 3000
```

---

## Purpose

Grafana runs on:

```text
Port 3000
```

---

## Browser Access

Example:

```text
http://localhost:3000
```

or via:

```text
minikube service
```

---

# Apply Deployment

## Command

```bash
kubectl apply -f grafana-deployment.yaml
```

---

## Internal Workflow

```text
kubectl
      ↓
API Server
      ↓
Deployment Created
      ↓
ReplicaSet Created
      ↓
Grafana Pod Running
```

---

# Verify Deployment

## Command

```bash
kubectl get deployment -n monitoring
```

Expected:

```text
grafana
```

---

# Verify Pods

## Command

```bash
kubectl get pods -n monitoring
```

Expected:

```text
grafana-xxxxx
Running
```

---

# Describe Pod

## Command

```bash
kubectl describe pod POD_NAME -n monitoring
```

---

# View Logs

## Command

```bash
kubectl logs POD_NAME -n monitoring
```

Expected:

```text
HTTP Server Listen
```

meaning Grafana started successfully.

---

# Default Login Credentials

When Grafana opens:

### Username

```text
admin
```

### Password

```text
admin
```

Grafana asks password reset after first login.

---

# Why Grafana?

Prometheus stores data.

But raw metrics are hard to read.

Grafana converts:

```text
Raw Numbers
```

into:

```text
Charts
Graphs
Dashboards
Monitoring Panels
```

---

# Monitoring Workflow

```text
FastAPI
      ↓
/metrics endpoint
      ↓
Prometheus scrapes data
      ↓
Prometheus stores metrics
      ↓
Grafana queries Prometheus
      ↓
Dashboard visualization
```

---

# Behind the Scenes

When Grafana loads:

```text
Grafana UI
      ↓
Query Prometheus
      ↓
Fetch Metrics
      ↓
Generate Graphs
      ↓
Display Dashboard
```

---

# File: `grafana-service.yaml`

## Purpose of This File

The `grafana-service.yaml` file is responsible for:

- Exposing Grafana outside Kubernetes
- Enabling browser access
- Providing dashboard access
- Connecting users to monitoring UI

Without Service:

- Grafana inaccessible  
- No browser access  
- No dashboards visible  
- Monitoring impossible

Think:

```text
Grafana Pod
       ↓
Grafana Service
       ↓
Browser Access
```

Pods are temporary.

Service provides:

```text
Stable Networking Layer
```

---

# Complete Code

```yaml
apiVersion: v1

kind: Service

metadata:
  name: grafana-service

  namespace: monitoring

spec:
  selector:
    app: grafana

  ports:
    - protocol: TCP
      port: 3000
      targetPort: 3000

  type: NodePort
```

---

# Understanding the YAML Line by Line

---

# API Version

## Code

```yaml
apiVersion: v1
```

---

## Purpose

Defines Kubernetes API version.

Services use:

```text
v1
```

Unlike deployments:

```yaml
apps/v1
```

---

# Kind

## Code

```yaml
kind: Service
```

---

## Purpose

Defines:

```text
Resource Type
```

Here:

```text
Service
```

means:

```text
Expose Network Access
```

for Grafana.

---

# Why Service Needed?

Pods get temporary IPs.

Example:

Today:

```text
10.244.0.20
```

Tomorrow:

```text
10.244.0.45
```

Bad for access.

Service gives:

```text
Permanent Entry Point
```

---

# Metadata

## Code

```yaml
metadata:
```

---

## Purpose

Stores:

```text
Service Identity
```

---

# Name

## Code

```yaml
name: grafana-service
```

---

## Purpose

Service name.

Used in commands.

Example:

```bash
kubectl get svc -n monitoring
```

Expected:

```text
grafana-service
```

---

# Namespace

## Code

```yaml
namespace: monitoring
```

---

## Purpose

Places Grafana service inside:

```text
monitoring namespace
```

---

## Why Important?

Grafana deployment exists in:

```text
monitoring
```

Service must exist there too.

Otherwise:

❌ Cannot connect to pod.

---

# Spec Section

## Code

```yaml
spec:
```

---

## Purpose

Contains:

```text
Networking Configuration
```

Includes:

- selector
- ports
- type

---

# Selector

## Code

```yaml
selector:
  app: grafana
```

---

## Purpose

Links service to Grafana pod.

Service searches:

```text
app=grafana
```

label.

---

## Internal Workflow

```text
Service
     ↓
Find pod
app=grafana
     ↓
Connect pod
```

---

## Important

Must match:

### deployment.yaml labels

```yaml
labels:
  app: grafana
```

If mismatch:

❌ Service fails.

---

# Ports Section

## Code

```yaml
ports:
```

---

## Purpose

Defines:

```text
Traffic Routing
```

---

# Protocol

## Code

```yaml
protocol: TCP
```

---

## Purpose

Grafana uses:

```text
TCP
```

because web traffic runs over TCP.

---

# Port

## Code

```yaml
port: 3000
```

---

## Purpose

Service-facing port.

Grafana accessible through:

```text
3000
```

---

# Target Port

## Code

```yaml
targetPort: 3000
```

---

## Purpose

Maps request to container.

Grafana internally runs on:

```text
3000
```

---

## Internal Workflow

```text
Browser Request
        ↓
Service Port 3000
        ↓
Target Port 3000
        ↓
Grafana Container
```

---

# Service Type

## Code

```yaml
type: NodePort
```

---

## Purpose

Exposes Grafana externally.

Without NodePort:

Only internal cluster access.

---

## What NodePort Does

Creates random external port.

Example:

```text
32451
```

Access:

```text
http://MINIKUBE_IP:32451
```

---

## Internal Workflow

```text
Browser
     ↓
NodePort
     ↓
Service
     ↓
Grafana Pod
```

---

# Apply Service

## Command

```bash
kubectl apply -f grafana-service.yaml
```

---

## Internal Workflow

```text
kubectl
      ↓
API Server
      ↓
Service Created
      ↓
Traffic Enabled
```

---

# Verify Service

## Command

```bash
kubectl get svc -n monitoring
```

---

## Expected Output

```text
NAME                TYPE
grafana-service     NodePort
```

---

# Describe Service

## Command

```bash
kubectl describe svc grafana-service -n monitoring
```

---

## Purpose

Shows:

- Ports
- NodePort
- Endpoints
- Labels

---

# Open Grafana

## Command

```bash
minikube service grafana-service -n monitoring
```

---

## Purpose

Automatically opens browser.

Expected:

```text
Grafana Login Page
```

---

# Login Credentials

### Username

```text
admin
```

### Password

```text
admin
```

After login:

Grafana asks password reset.

---

# Add Prometheus Data Source

Inside Grafana:

### Go To

```text
Connections
      ↓
Data Sources
      ↓
Add Data Source
```

Choose:

```text
Prometheus
```

---

## URL

Use:

```text
http://prometheus-service:9090
```

Click:

```text
Save & Test
```

Expected:

```text
Data source is working
```

---

# Create Dashboard

### Go To

```text
Dashboards
     ↓
New Dashboard
```

---

## Example Query

```text
http_requests_total
```

Expected:

Graph visible.

---

# Monitoring Flow

```text
FastAPI App
      ↓
/metrics endpoint
      ↓
Prometheus Scrapes
      ↓
Stores Metrics
      ↓
Grafana Queries
      ↓
Dashboard Display
```

---

# Behind the Scenes

When user opens Grafana:

```text
Browser
      ↓
NodePort
      ↓
Grafana Service
      ↓
Grafana Pod
      ↓
Prometheus Query
      ↓
Metrics Visualization
```

---

# Monitoring Workflow & Setup Guide

This section explains:

```text
How monitoring works end-to-end
inside this project
```

including:

- Metrics generation
- Prometheus scraping
- Grafana dashboards
- Data flow
- Monitoring lifecycle
- Troubleshooting

Think of monitoring like this:

```text
User Request
      ↓
FastAPI App
      ↓
Metrics Generated
      ↓
/metrics endpoint
      ↓
Prometheus Scrapes
      ↓
Stores Time-Series Data
      ↓
Grafana Queries
      ↓
Dashboard Visualization
```

---

# Monitoring Architecture

Complete monitoring architecture:

```text
                 Kubernetes Cluster
┌────────────────────────────────────────┐

      FastAPI Application
              ↓
       /metrics endpoint
              ↓
      Prometheus Scrapes
              ↓
       Metrics Database
              ↓
        Grafana Queries
              ↓
      Dashboard Visualization

└────────────────────────────────────────┘
```

---

# Step 1 — FastAPI Generates Metrics

Inside your FastAPI app:

We added:

```python
Instrumentator().instrument(app).expose(app)
```

---

## Purpose

Automatically creates:

```text
Prometheus Metrics Endpoint
```

at:

```text
/metrics
```

---

## Why Needed?

Without this:

- No metrics available  
- Prometheus cannot scrape

---

## Test Metrics

Open:

```text
http://localhost:8000/metrics
```

or in Kubernetes:

```text
http://MINIKUBE_IP:NODEPORT/metrics
```

Expected output:

```text
http_requests_total
process_cpu_seconds_total
python_gc_objects_collected_total
```

---

# Common Metrics Generated

Prometheus automatically exposes:

---

## HTTP Requests

Metric:

```text
http_requests_total
```

Purpose:

Tracks:

```text
Total API requests
```

---

## Request Duration

Metric:

```text
http_request_duration_seconds
```

Purpose:

Measures:

```text
API response time
```

---

## CPU Usage

Metric:

```text
process_cpu_seconds_total
```

Purpose:

Measures CPU consumption.

---

## Memory Usage

Metric:

```text
process_resident_memory_bytes
```

Purpose:

Tracks RAM usage.

---

# Step 2 — Prometheus Scrapes Metrics

Prometheus periodically checks:

```text
/metrics
```

endpoint.

Think:

```text
Prometheus asks:

"Give me latest stats"
```

every few seconds.

---

# Scraping Configuration

Configured inside:

```text
prometheus.yml
```

Example:

```yaml
scrape_configs:
  - job_name: "fastapi"

    static_configs:
      - targets:
        - cloud-url-monitor-service:80
```

---

## Meaning

Prometheus scrapes:

```text
cloud-url-monitor-service
```

using:

```text
Port 80
```

---

## Internal Workflow

```text
Prometheus
      ↓
Request /metrics
      ↓
FastAPI responds
      ↓
Metrics Collected
      ↓
Stored in TSDB
```

---

# Step 3 — Verify Prometheus Target

Open Prometheus.

Command:

```bash
minikube service prometheus-service -n monitoring
```

---

## Navigate

```text
Status
   ↓
Targets
```

Expected:

```text
UP
```

for:

```text
cloud-url-monitor-service
```

---

## Meaning

### UP

Prometheus connected successfully.

---

### DOWN

Connection failed.

Possible causes:

- wrong service name
- wrong port
- pod failure
- metrics unavailable

---

# Step 4 — Test Prometheus Queries

Inside Prometheus:

Search bar:

---

## Total Requests

```text
http_requests_total
```

Click:

```text
Execute
```

Expected:

Metrics displayed.

---

## Request Latency

```text
http_request_duration_seconds
```

---

## CPU Usage

```text
process_cpu_seconds_total
```

---

## Memory

```text
process_resident_memory_bytes
```

---

# Step 5 — Open Grafana

Command:

```bash
minikube service grafana-service -n monitoring
```

---

## Login

### Username

```text
admin
```

### Password

```text
admin
```

---

# Step 6 — Configure Prometheus Data Source

Inside Grafana:

Go:

```text
Connections
      ↓
Data Sources
      ↓
Add Data Source
```

Choose:

```text
Prometheus
```

---

## URL

Use:

```text
http://prometheus-service:9090
```

---

## Save Connection

Click:

```text
Save & Test
```

Expected:

```text
Data source is working
```

---

# Why This URL?

Because Kubernetes service discovery works internally.

Grafana accesses:

```text
prometheus-service
```

using Kubernetes DNS.

---

## Internal Workflow

```text
Grafana
      ↓
prometheus-service
      ↓
Prometheus API
      ↓
Metrics Returned
```

---

# Step 7 — Create Dashboard

Inside Grafana:

```text
Dashboards
      ↓
New Dashboard
```

Click:

```text
Add Visualization
```

Select:

```text
Prometheus
```

---

# Example Dashboard Queries

---

## Total Requests

Query:

```text
http_requests_total
```

Shows:

```text
API Traffic
```

---

## Request Latency

Query:

```text
http_request_duration_seconds
```

Shows:

```text
API Performance
```

---

## CPU Usage

Query:

```text
process_cpu_seconds_total
```

Shows:

```text
CPU Consumption
```

---

## Memory Usage

Query:

```text
process_resident_memory_bytes
```

Shows:

```text
RAM Usage
```

---

# Monitoring Lifecycle

Complete lifecycle:

```text
User Request
      ↓
FastAPI API Hit
      ↓
Metric Updated
      ↓
/metrics Endpoint
      ↓
Prometheus Scrape
      ↓
Metrics Stored
      ↓
Grafana Query
      ↓
Dashboard Updated
```

---

# Kubernetes Monitoring Commands

---

## View Monitoring Pods

```bash
kubectl get pods -n monitoring
```

Expected:

```text
prometheus-xxxxx
grafana-xxxxx
```

Running.

---

## View Services

```bash
kubectl get svc -n monitoring
```

Expected:

```text
prometheus-service
grafana-service
```

---

## View Logs

### Prometheus

```bash
kubectl logs POD_NAME -n monitoring
```

---

### Grafana

```bash
kubectl logs POD_NAME -n monitoring
```

---

## Describe Pod

```bash
kubectl describe pod POD_NAME -n monitoring
```

Useful for:

```text
CrashLoopBackOff
Pending
```

---

# Behind the Scenes

Real monitoring flow:

```text
FastAPI Request
       ↓
Metric Counter Updated
       ↓
Prometheus Scrape
       ↓
Time-Series Storage
       ↓
Grafana Query
       ↓
Dashboard Graph
```

---