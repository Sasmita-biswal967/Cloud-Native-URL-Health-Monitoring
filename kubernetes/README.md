# File: `deployment.yaml`

## Purpose of This File

The `deployment.yaml` file is responsible for:

- Deploying the FastAPI application in Kubernetes
- Managing pods automatically
- Restarting failed containers
- Scaling replicas
- Pulling Docker images
- Running application containers

---

# Complete Code

```yaml
apiVersion: apps/v1

kind: Deployment

metadata:
  name: cloud-url-monitor-deployment

spec:
  replicas: 2

  selector:
    matchLabels:
      app: cloud-url-monitor

  template:
    metadata:
      labels:
        app: cloud-url-monitor

    spec:
      containers:
      - name: cloud-url-monitor

        image: cloud-url-monitor:latest

        imagePullPolicy: Never

        ports:
        - containerPort: 8000
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

Defines:

```text
Which Kubernetes API version
to use
```

Here:

```text
apps/v1
```

is used for:

```text
Deployments
ReplicaSets
```

---

## Why Needed?

Kubernetes supports many APIs.

Example:

```text
apps/v1
v1
batch/v1
autoscaling/v2
```

Each resource uses a different version.

Deployment uses:

```text
apps/v1
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
What Kubernetes resource
we are creating
```

Here:

```text
Deployment
```

means:

```text
Manage application pods
```

---

## Why Deployment?

Deployment provides:

- Pod management  
- Auto restart  
- Scaling  
- Rolling updates  
- Replica management

---

## Internal Workflow

```text
Deployment
      ↓
ReplicaSet
      ↓
Pods
```

---

# Metadata

## Code

```yaml
metadata:
  name: cloud-url-monitor-deployment
```

---

## Purpose

Provides:

```text
Resource identity
```

Deployment name:

```text
cloud-url-monitor-deployment
```

---

## Why Important?

Used for commands.

Example:

```bash
kubectl get deployment
```

Output:

```text
cloud-url-monitor-deployment
```

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
Deployment configuration
```

This includes:

- replicas
- labels
- containers
- image
- ports

Think:

```text
How deployment should behave
```

---

# Replicas

## Code

```yaml
replicas: 2
```

---

## Purpose

Defines:

```text
Number of pod copies
```

Here:

```text
2 pods
```

will run.

---

## Why Use Replicas?

Benefits:

### High Availability

If:

```text
Pod 1 crashes
```

Pod 2 still works.

---

### Load Balancing

Traffic distributed.

---

### Scalability

Easy scaling.

Example:

```yaml
replicas: 5
```

runs:

```text
5 pods
```

---

## Internal Workflow

```text
Deployment
      ↓
ReplicaSet
      ↓
Create 2 Pods
```

---

# Selector

## Code

```yaml
selector:
  matchLabels:
```

---

## Purpose

Helps deployment:

```text
Find its pods
```

Deployment must know:

```text
Which pods belong to me
```

---

# Match Labels

## Code

```yaml
app: cloud-url-monitor
```

---

## Purpose

Links deployment with pods.

Think:

```text
Tag System
```

Like:

```text
Group Identifier
```

---

## Internal Workflow

Deployment searches:

```text
app=cloud-url-monitor
```

Finds matching pods.

Controls them.

---

# Pod Template

## Code

```yaml
template:
```

---

## Purpose

Defines:

```text
Blueprint for Pod Creation
```

Every pod created follows this template.

---

## Internal Workflow

```text
Deployment
       ↓
Template
       ↓
Pod Created
```

---

# Template Metadata

## Code

```yaml
metadata:
  labels:
```

---

## Purpose

Adds labels to pods.

Example:

```yaml
app: cloud-url-monitor
```

---

## Why Needed?

Deployment selector:

```yaml
matchLabels
```

must match pod labels.

Otherwise:

Pods won't connect.

---

# Container Spec

## Code

```yaml
containers:
```

---

## Purpose

Defines:

```text
Container configuration
```

Includes:

- image
- ports
- environment
- resources

---

# Container Name

## Code

```yaml
name: cloud-url-monitor
```

---

## Purpose

Container identifier.

Useful for:

Logs.

Example:

```bash
kubectl logs POD_NAME
```

---

# Docker Image

## Code

```yaml
image:
cloud-url-monitor:latest
```

---

## Purpose

Defines:

```text
Which Docker image to run
```

Kubernetes pulls this image.

---

## Important

Since using:

```text
Minikube local image
```

we use:

```yaml
imagePullPolicy: Never
```

Otherwise:

Kubernetes tries Docker Hub.

Fails.

---

# Image Pull Policy

## Code

```yaml
imagePullPolicy: Never
```

---

## Purpose

Tells Kubernetes:

```text
Do NOT download image
```

Use:

```text
local Docker image
```

---

## Why Needed?

Because:

You built image locally.

Example:

```bash
docker build -t cloud-url-monitor .
```

---

# Container Port

## Code

```yaml
containerPort: 8000
```

---

## Purpose

Tells Kubernetes:

FastAPI runs on:

```text
port 8000
```

---

## Internal Workflow

```text
Pod
    ↓
Container
    ↓
Port 8000 Open
```

---

# Apply Deployment

## Command

```bash
kubectl apply -f deployment.yaml
```

---

## What Happens Internally

```text
kubectl
      ↓
Kubernetes API Server
      ↓
Deployment Created
      ↓
ReplicaSet Created
      ↓
Pods Created
```

---

# Verify Deployment

Command:

```bash
kubectl get deployment
```

Expected:

```text
cloud-url-monitor-deployment
```

---

# Check Pods

Command:

```bash
kubectl get pods
```

Expected:

```text
cloud-url-monitor-deployment-xxxxx
Running
```

2 pods running.

---

# Describe Deployment

Command:

```bash
kubectl describe deployment cloud-url-monitor-deployment
```

Purpose:

Detailed deployment info.

---

# Logs

Command:

```bash
kubectl logs POD_NAME
```

Expected:

```text
Uvicorn running
```

---

# Behind the Scenes

When running:

```bash
kubectl apply -f deployment.yaml
```

Flow:

```text
YAML File
      ↓
API Server
      ↓
Deployment Created
      ↓
ReplicaSet Created
      ↓
Pods Created
      ↓
FastAPI Running
```

---

# File: `service.yaml`

## Purpose of This File

The `service.yaml` file is responsible for:

- Exposing pods to the network
- Providing stable communication
- Load balancing traffic
- Making FastAPI accessible

Without Service:

- Pods inaccessible  
- No external access  
- Pod IP changes break app  
- Cannot open FastAPI in browser

Think:

```text
Pods
   ↓
Service
   ↓
Browser Access
```

Pods are temporary.

A service gives:

```text
Permanent Access Point
```

---

# Complete Code

```yaml
apiVersion: v1

kind: Service

metadata:
  name: cloud-url-monitor-service

spec:
  selector:
    app: cloud-url-monitor

  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000

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

Defines:

```text
Kubernetes API version
```

For Service resources:

```text
v1
```

is used.

Unlike deployment:

```yaml
apps/v1
```

Service uses:

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
Expose application networking
```

---

## Why Service?

Pods are temporary.

Pod IP changes frequently.

Example:

Today:

```text
10.244.0.2
```

Tomorrow:

```text
10.244.0.5
```

Bad for applications.

Service creates:

```text
Stable IP + DNS
```

---

# Metadata

## Code

```yaml
metadata:
  name:
    cloud-url-monitor-service
```

---

## Purpose

Defines:

```text
Service Name
```

Used in commands.

Example:

```bash
kubectl get svc
```

Output:

```text
cloud-url-monitor-service
```

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
Service configuration
```

Includes:

- selector
- ports
- service type

---

# Selector

## Code

```yaml
selector:
  app: cloud-url-monitor
```

---

## Purpose

Links service with pods.

Service searches for pods having:

```yaml
app: cloud-url-monitor
```

label.

---

## Why Important?

Must match:

### deployment.yaml

```yaml
labels:
  app: cloud-url-monitor
```

If labels mismatch:

❌ No connection

App breaks.

---

## Internal Workflow

```text
Service
     ↓
Find label
app=cloud-url-monitor
     ↓
Connect pods
```

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
Traffic Mapping
```

How request flows.

---

# Protocol

## Code

```yaml
protocol: TCP
```

---

## Purpose

Defines communication type.

Web applications use:

```text
TCP
```

---

## Why TCP?

HTTP works over TCP.

FastAPI uses:

```text
TCP
```

---

# Service Port

## Code

```yaml
port: 80
```

---

## Purpose

External service port.

User accesses:

```text
Port 80
```

Think:

```text
Public Entry Port
```

---

# Target Port

## Code

```yaml
targetPort: 8000
```

---

## Purpose

Maps traffic to container.

FastAPI runs internally on:

```text
8000
```

---

## Internal Flow

```text
Browser Request
       ↓
Port 80
       ↓
Service
       ↓
Container Port 8000
       ↓
FastAPI
```

---

# Service Type

## Code

```yaml
type: NodePort
```

---

## Purpose

Exposes application outside cluster.

Without NodePort:

Only internal access possible.

---

## What NodePort Does

Creates:

```text
Random External Port
```

Usually:

```text
30000–32767
```

Example:

```text
31542
```

Access app:

```text
http://MINIKUBE_IP:31542
```

---

# Internal Workflow

```text
Browser
     ↓
NodePort
     ↓
Service
     ↓
Pods
     ↓
FastAPI
```

---

# Apply Service

## Command

```bash
kubectl apply -f service.yaml
```

---

## Internal Working

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

Command:

```bash
kubectl get svc
```

Expected:

```text
cloud-url-monitor-service
```

---

## Example Output

```text
NAME                          TYPE
cloud-url-monitor-service     NodePort
```

---

# Get Service Details

Command:

```bash
kubectl describe svc cloud-url-monitor-service
```

Shows:

- Ports
- NodePort
- Endpoints
- Labels

---

# Get Minikube URL

Command:

```bash
minikube service cloud-url-monitor-service
```

Expected:

Browser opens automatically.

Example:

```text
http://192.168.49.2:31542
```

---

# Test FastAPI

## Home Route

```text
http://MINIKUBE_IP:NODEPORT
```

Expected:

```json
{
  "message":
  "Cloud URL Monitor Running"
}
```

---

## Swagger UI

```text
/docs
```

Expected:

Interactive FastAPI docs.

---

## Metrics Endpoint

```text
/metrics
```

Expected:

Prometheus metrics.

---

# Service Types in Kubernetes

---

## ClusterIP

Default.

Internal communication only.

```text
Pod ↔ Pod
```

No external access.

---

## NodePort

Used in this project.

External access.

```text
Browser ↔ App
```

---

## LoadBalancer

Used in cloud:

```text
AWS
Azure
GCP
```

Creates:

```text
Cloud Load Balancer
```

Mostly production.

---

# Behind The Scenes

When user opens:

```text
http://minikube-ip:nodeport
```

Flow:

```text
Browser
     ↓
NodePort
     ↓
Service
     ↓
Load Balancing
     ↓
Pod 1 / Pod 2
     ↓
FastAPI
```

Because replicas = 2:

Kubernetes automatically load-balances requests.

---

# Kubernetes Commands & Workflow

This section explains:

```text
How Kubernetes actually works
in this project
```

including:

- Deploying application
- Viewing pods
- Debugging failures
- Logs
- Scaling
- Service access
- Self-healing
- Pod lifecycle

Think of workflow like:

```text
Docker Image
       ↓
Deployment
       ↓
Pods Created
       ↓
Service Exposure
       ↓
Application Running
```

---

# Step 1 — Start Minikube

## Command

```bash
minikube start
```

---

## Purpose

Starts:

```text
Local Kubernetes Cluster
```

Without Minikube:

- Kubernetes unavailable  
- Pods cannot run

---

## What Happens Internally

```text
Minikube VM Starts
        ↓
Control Plane Starts
        ↓
API Server Starts
        ↓
Scheduler Starts
        ↓
Kubernetes Ready
```

---

## Expected Output

```text
Done! kubectl is now configured
to use "minikube"
```

---

# Step 2 — Verify Cluster

## Command

```bash
kubectl cluster-info
```

---

## Purpose

Checks:

```text
Cluster status
```

---

## Expected Output

```text
Kubernetes control plane
running at https://...
```

---

## Why Important?

Confirms:

✅ Cluster active  
✅ kubectl connected

---

# Step 3 — Verify Nodes

## Command

```bash
kubectl get nodes
```

---

## Purpose

Shows:

```text
Available machines
```

In Minikube:

Usually:

```text
1 node
```

---

## Example Output

```text
NAME        STATUS
minikube    Ready
```

---

## Meaning

### Ready

Kubernetes node healthy.

---

# Step 4 — Build Docker Image

Before deployment:

Build app image.

## Command

```bash
docker build -t cloud-url-monitor .
```

---

## Purpose

Creates:

```text
Docker image
```

used by Kubernetes.

---

## Verify Image

Command:

```bash
docker images
```

Expected:

```text
cloud-url-monitor
```

visible.

---

# Step 5 — Apply Deployment

## Command

```bash
kubectl apply -f deployment.yaml
```

---

## Purpose

Creates deployment.

Kubernetes automatically:

- Creates ReplicaSet
- Creates Pods
- Starts Containers

---

## Internal Workflow

```text
deployment.yaml
         ↓
API Server
         ↓
Deployment Created
         ↓
ReplicaSet Created
         ↓
Pods Created
```

---

## Expected Output

```text
deployment.apps/
cloud-url-monitor-deployment created
```

---

# Step 6 — Check Deployments

## Command

```bash
kubectl get deployments
```

---

## Purpose

Shows:

```text
Running deployments
```

---

## Example Output

```text
NAME
cloud-url-monitor-deployment
```

---

## Important Columns

### READY

Example:

```text
2/2
```

Means:

```text
2 pods running
```

---

### AVAILABLE

Pods healthy.

---

# Step 7 — Check Pods

## Command

```bash
kubectl get pods
```

---

## Purpose

Shows:

```text
Running containers
```

---

## Example Output

```text
NAME                                READY
cloud-url-monitor-xxxx             1/1
cloud-url-monitor-yyyy             1/1
```

---

## Meaning

### READY

```text
1/1
```

Means:

Container healthy.

---

### STATUS

#### Running

Application healthy.

#### Pending

Waiting resources.

#### CrashLoopBackOff

App crashing repeatedly.

#### ContainerCreating

Image downloading.

---

# Step 8 — Describe Pod

## Command

```bash
kubectl describe pod POD_NAME
```

Example:

```bash
kubectl describe pod cloud-url-monitor-abc123
```

---

## Purpose

Detailed troubleshooting.

Shows:

- Events
- Errors
- Restarts
- Container state
- Networking

---

## Useful For

Fixing:

```text
CrashLoopBackOff
ImagePullBackOff
```

---

## Example Output

```text
Events:
Pulled image
Started container
```

---

# Step 9 — View Logs

## Command

```bash
kubectl logs POD_NAME
```

---

## Purpose

Shows application logs.

Equivalent to:

```text
Terminal output
```

inside pod.

---

## Example

```bash
kubectl logs cloud-url-monitor-abc123
```

Expected:

```text
Uvicorn running on:
0.0.0.0:8000
```

---

## Why Important?

Helps debug:

- FastAPI errors
- Missing modules
- Database issues

---

# Step 10 — Execute Inside Pod

## Command

```bash
kubectl exec -it POD_NAME -- sh
```

Example:

```bash
kubectl exec -it cloud-url-monitor-abc123 -- sh
```

---

## Purpose

Enter container shell.

Like:

```text
SSH into container
```

---

## Example Usage

Inside pod:

```bash
ls
```

View files.

---

Check Python:

```bash
python --version
```

---

Check app folder:

```bash
cd /app
```

---

# Step 11 — Apply Service

## Command

```bash
kubectl apply -f service.yaml
```

---

## Purpose

Exposes application.

Without service:

No browser access.

---

## Expected Output

```text
service/
cloud-url-monitor-service created
```

---

# Step 12 — View Services

## Command

```bash
kubectl get svc
```

---

## Purpose

Shows networking services.

---

## Example Output

```text
NAME                          TYPE
cloud-url-monitor-service     NodePort
```

---

## Important Columns

### TYPE

```text
NodePort
```

Means:

External access enabled.

---

### PORT

Example:

```text
80:31542/TCP
```

Meaning:

```text
80 → service
31542 → external nodeport
```

---

# Step 13 — Open Application

## Command

```bash
minikube service cloud-url-monitor-service
```

---

## Purpose

Opens app automatically.

Browser launches.

---

## Example URL

```text
http://192.168.49.2:31542
```

---

# Test URLs

---

## Home Route

```text
/
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
/docs
```

---

## Metrics

```text
/metrics
```

---

# Step 14 — Scale Pods

## Command

```bash
kubectl scale deployment \
cloud-url-monitor-deployment \
--replicas=5
```

---

## Purpose

Increase app capacity.

---

## Internal Workflow

```text
Deployment
      ↓
ReplicaSet Updated
      ↓
3 New Pods Created
```

---

## Verify

```bash
kubectl get pods
```

Expected:

```text
5 pods
```

running.

---

# Step 15 — Delete Pod (Self-Healing Demo)

## Command

```bash
kubectl delete pod POD_NAME
```

---

## Purpose

Demonstrates:

```text
Self-Healing
```

---

## Internal Workflow

```text
Pod Deleted
      ↓
Deployment notices
      ↓
ReplicaSet recreates pod
      ↓
App restored
```

---

## Verify

Run:

```bash
kubectl get pods
```

New pod appears automatically.

---

# Step 16 — Delete Deployment

## Command

```bash
kubectl delete deployment \
cloud-url-monitor-deployment
```

---

## Purpose

Removes deployment.

Pods deleted automatically.

---

# Step 17 — Delete Service

## Command

```bash
kubectl delete service \
cloud-url-monitor-service
```

---

## Purpose

Removes external access.

---

# Pod Lifecycle

Pods go through stages:

```text
Pending
   ↓
ContainerCreating
   ↓
Running
   ↓
Succeeded / Failed
```

---

## Pending

Waiting resources.

---

## ContainerCreating

Image pulling.

---

## Running

Healthy state.

---

## Failed

Application crashed.

---

# Kubernetes Self-Healing

One major feature:

```text
Automatic Recovery
```

Example:

```text
Pod crashes
```

Kubernetes:

```text
Automatically recreates it
```

No manual work.

---

# Internal Kubernetes Architecture

```text
kubectl
    ↓
API Server
    ↓
Scheduler
    ↓
Node
    ↓
Pod
    ↓
Container
```

---

# Behind the Scenes

When user runs:

```bash
kubectl apply -f deployment.yaml
```

Flow:

```text
YAML File
      ↓
API Server
      ↓
Deployment
      ↓
ReplicaSet
      ↓
Pods
      ↓
Running Application
```