# Jenkins Installation & Setup Using Docker

This section explains:

```text
How Jenkins is deployed using Docker
instead of manual installation
```

including:

- Dockerized Jenkins
- Jenkins container setup
- Persistent storage
- Docker integration
- Kubernetes integration
- Minikube access
- Pipeline execution

---

# Why Dockerized Jenkins?

Instead of:

```text
Install Jenkins manually
on EC2 OS
```

we use:

```text
Jenkins Docker Container
```

Benefits:

- Cleaner setup  
- Easier maintenance  
- Better DevOps practice  
- Easy upgrades  
- Portable architecture  
- Production-like workflow

---

# Jenkins Architecture

Your CI/CD architecture:

```text
EC2 Instance
      ↓
Docker Engine
      ↓
Jenkins Container
      ↓
Docker Socket Mounted
      ↓
kubectl + Minikube Access
      ↓
Kubernetes Cluster
```

---

# Step 1 — SSH Into EC2

Command:

```bash
ssh -i "your-key.pem" ec2-user@PUBLIC_IP
```

---

## Purpose

Connects to AWS EC2 instance.

---

## Expected Output

```text
[ec2-user@ip-172-31-x-x ~]$
```

Meaning:

```text
Successfully logged in
```

---

# Step 2 — Update Server

Command:

```bash
sudo yum update -y
```

---

## Purpose

Updates packages.

Why needed?

```text
Security fixes
Dependency updates
Better compatibility
```

---

# Step 3 — Install Docker

Command:

```bash
sudo yum install docker -y
```

---

## Purpose

Installs:

```text
Docker Engine
```

needed to run Jenkins container.

---

# Start Docker

Command:

```bash
sudo systemctl start docker
```

---

## Purpose

Starts Docker service.

---

# Enable Docker

Command:

```bash
sudo systemctl enable docker
```

---

## Purpose

Starts Docker automatically after reboot.

---

# Verify Docker

Command:

```bash
docker --version
```

Expected:

```text
Docker version xx.x.x
```

---

# Step 4 — Add Docker Permission

Command:

```bash
sudo usermod -aG docker ec2-user
```

---

## Purpose

Allows:

```text
ec2-user
```

to run Docker without sudo.

---

# Apply Permission

Command:

```bash
newgrp docker
```

---

# Verify

Command:

```bash
docker ps
```

Expected:

```text
CONTAINER ID
```

No permission error.

---

# Step 5 — Create Jenkins Volume

Command:

```bash
docker volume create jenkins_home
```

---

## Purpose

Creates persistent storage.

Stores:

```text
Jenkins Jobs
Pipelines
Plugins
Credentials
Settings
```

Without volume:

```text
Container deleted
        ↓
Everything lost
```

---

# Verify Volume

Command:

```bash
docker volume ls
```

Expected:

```text
jenkins_home
```

---

# Step 6 — Pull Jenkins Image

Command:

```bash
docker pull jenkins/jenkins:lts
```

---

## Purpose

Downloads:

```text
Official Jenkins LTS Image
```

LTS means:

```text
Long Term Support
```

Most stable version.

---

# Verify Image

Command:

```bash
docker images
```

Expected:

```text
jenkins/jenkins
lts
```

---

# Step 7 — Run Jenkins Container

Command:

```bash
docker run -d \
--name jenkins \
-p 8080:8080 \
-p 50000:50000 \
-v jenkins_home:/var/jenkins_home \
-v /var/run/docker.sock:/var/run/docker.sock \
-v ~/.kube:/var/jenkins_home/.kube \
-v ~/.minikube:/var/jenkins_home/.minikube \
jenkins/jenkins:lts
```

---

# Understanding the Command

---

## Detached Mode

```bash
-d
```

Runs container in background.

---

## Container Name

```bash
--name jenkins
```

Container name:

```text
jenkins
```

---

## Port Mapping

### Jenkins UI

```bash
-p 8080:8080
```

Access:

```text
http://EC2_PUBLIC_IP:8080
```

---

### Jenkins Agents

```bash
-p 50000:50000
```

Used for:

```text
Jenkins worker communication
```

---

## Persistent Volume

```bash
-v jenkins_home:
/var/jenkins_home
```

Stores Jenkins data permanently.

Without this:

❌ Jobs lost  
❌ Plugins lost  
❌ Pipelines lost

---

## Docker Socket Mount

```bash
-v /var/run/docker.sock:
/var/run/docker.sock
```

---

## Purpose

Allows Jenkins container to control:

```text
Host Docker Engine
```

Needed for:

```bash
docker build
docker images
docker ps
```

inside pipeline.

Without this:

```text
docker command fails
```

---

## Kubernetes Config Mount

```bash
-v ~/.kube:
/var/jenkins_home/.kube
```

---

## Purpose

Provides:

```text
kubectl access
```

to Kubernetes cluster.

---

## Minikube Mount

```bash
-v ~/.minikube:
/var/jenkins_home/.minikube
```

---

## Purpose

Allows Jenkins to interact with:

```text
Minikube Cluster
```

---

# Step 8 — Verify Container

Command:

```bash
docker ps
```

Expected:

```text
jenkins
Up
0.0.0.0:8080->8080
```

Meaning:

```text
Jenkins running
```

---

# Step 9 — Open Jenkins

Browser:

```text
http://EC2_PUBLIC_IP:8080
```

Expected:

```text
Unlock Jenkins
```

screen.

---

# Step 10 — Get Initial Password

Command:

```bash
docker exec jenkins cat \
/var/jenkins_home/secrets/initialAdminPassword
```

---

## Purpose

Gets admin password.

Paste into:

```text
Unlock Jenkins
```

page.

---

# Step 11 — Install Plugins

Choose:

```text
Install Suggested Plugins
```

---

## Plugins Installed

Typically:

```text
Git
Pipeline
Docker
Credentials
GitHub
Blue Ocean
```

---

# Step 12 — Create Admin User

Enter:

```text
username
password
email
```

---

# Step 13 — Install Docker CLI Inside Jenkins

Enter container:

```bash
docker exec -it jenkins bash
```

Install Docker CLI:

```bash
apt update
apt install docker.io -y
```

Verify:

```bash
docker --version
```

---

# Step 14 — Install kubectl

Command:

```bash
curl -LO \
https://dl.k8s.io/release/\
$(curl -L -s \
https://dl.k8s.io/release/stable.txt)\
/bin/linux/amd64/kubectl
```

Install:

```bash
install -o root -g root \
-m 0755 kubectl \
/usr/local/bin/kubectl
```

---

# Verify kubectl

Command:

```bash
kubectl version --client
```

---

# Step 15 — Install Minikube CLI

Download:

```bash
curl -LO \
https://storage.googleapis.com/
minikube/releases/latest/
minikube-linux-amd64
```

Install:

```bash
install \
minikube-linux-amd64 \
/usr/local/bin/minikube
```

---

# Verify Minikube

Command:

```bash
minikube version
```

---

# Step 16 — Test Kubernetes Access

Enter container:

```bash
docker exec -it jenkins bash
```

Run:

```bash
kubectl get pods
```

Expected:

```text
Running Pods
```

---

# Step 17 — Create Pipeline Job

Inside Jenkins:

```text
Dashboard
      ↓
New Item
      ↓
Pipeline
```

Name:

```text
cloud-url-monitor-pipeline
```

---

# Step 18 — Add Jenkinsfile

Pipeline:

```text
Pipeline Script
```

Paste your:

```text
Jenkinsfile
```

Save.

---

# Step 19 — Run Build

Click:

```text
Build Now
```

Expected stages:

```text
Clone Repository
      ↓
Build Docker Image
      ↓
Load Image To Minikube
      ↓
Deploy To Kubernetes
      ↓
Restart Deployment
      ↓
Verify Pods
```

---

# Complete CI/CD Flow

Real workflow:

```text
GitHub Push
      ↓
Jenkins Trigger
      ↓
Clone Repo
      ↓
Docker Build
      ↓
Load Minikube Image
      ↓
Deploy Kubernetes
      ↓
Restart Pods
      ↓
Verify Deployment
```

---

# GitHub Webhook Setup

This section explains:

```text
How GitHub automatically triggers
Jenkins pipeline after code push
```

including:

- GitHub integration
- webhook configuration
- automatic builds
- push events
- Jenkins triggers
- debugging webhook issues

---

# Why Webhooks?

Without webhook:

```text
Developer Pushes Code
         ↓
Open Jenkins
         ↓
Click Build Now
         ↓
Deployment Starts
```

Manual process.

With webhook:

```text
Developer Pushes Code
         ↓
GitHub Sends Notification
         ↓
Jenkins Triggered
         ↓
Pipeline Starts Automatically
```

This is:

```text
Real CI/CD Automation
```

---

# CI/CD Workflow

Complete automation flow:

```text
Code Change
      ↓
git add .
      ↓
git commit
      ↓
git push
      ↓
GitHub Repository
      ↓
Webhook Trigger
      ↓
Jenkins Pipeline
      ↓
Docker Build
      ↓
Minikube Load
      ↓
Kubernetes Deployment
```

---

# Step 1 — Install GitHub Plugin

Inside Jenkins:

Go:

```text
Manage Jenkins
      ↓
Plugins
```

Search:

```text
GitHub Integration
```

Install.

Restart Jenkins.

---

# Step 2 — Install Required Plugins

Ensure installed:

```text
Git
GitHub
Pipeline
Docker Pipeline
Credentials Binding
```

---

# Step 3 — Create Pipeline Job

Go:

```text
Dashboard
      ↓
New Item
      ↓
Pipeline
```

Name:

```text
cloud-url-monitor-pipeline
```

---

# Step 4 — Configure Source Code

Inside pipeline:

Go:

```text
Pipeline
```

Select:

```text
Pipeline script from SCM
```

---

## SCM

Choose:

```text
Git
```

---

## Repository URL

Use:

```text
https://github.com/
Sasmita-biswal967/
Cloud-Native-URL-Health-Monitoring.git
```

---

## Branch

Use:

```text
*/main
```

(or your branch)

---

## Script Path

Set:

```text
jenkins/Jenkinsfile
```

if inside folder.

Or:

```text
Jenkinsfile
```

if root.

---

# Step 5 — Enable Build Trigger

Inside Job:

Go:

```text
Build Triggers
```

Enable:

```text
GitHub hook trigger
for GITScm polling
```

---

## Purpose

Allows:

```text
GitHub webhook
```

to start builds.

Without this:

❌ webhook ignored

---

# Step 6 — Get Jenkins URL

Need Jenkins public URL.

Example:

```text
http://EC2_PUBLIC_IP:8080
```

Example:

```text
http://44.xx.xx.xx:8080
```

---

## Test URL

Open in browser.

Should load:

```text
Jenkins Dashboard
```

---

# Important AWS Security Group Rule

Make sure:

```text
Port 8080
```

is open.

Go:

```text
AWS EC2
      ↓
Security Groups
```

Add:

```text
8080
TCP
0.0.0.0/0
```

Otherwise:

❌ GitHub cannot reach Jenkins.

---

# Step 7 — Configure GitHub Webhook

Open repository:

```text
GitHub Repository
```

Go:

```text
Settings
      ↓
Webhooks
      ↓
Add Webhook
```

---

# Payload URL

Add:

```text
http://EC2_PUBLIC_IP:8080/
github-webhook/
```

Example:

```text
http://44.xx.xx.xx:8080/
github-webhook/
```

Important:

Must end with:

```text
/github-webhook/
```

---

# Content Type

Choose:

```text
application/json
```

---

# Secret

Leave empty.

(Optional for learning project)

---

# SSL Verification

Choose:

```text
Disable SSL verification
```

Only if HTTP used.

---

# Events

Choose:

```text
Just the push event
```

---

# Save Webhook

Click:

```text
Add Webhook
```

---

# Step 8 — Verify Webhook

GitHub should show:

```text
Recent Deliveries
```

Green tick:

```text
200 OK
```

Meaning:

```text
Jenkins received request
```

---

## If Red Cross Appears

Means:

```text
Webhook failed
```

---

# Step 9 — Test Automatic Trigger

Modify code.

Example:

```python
print("Webhook test")
```

Commit:

```bash
git add .
git commit -m "Testing webhook"
git push origin main
```

---

# Expected Workflow

After push:

```text
GitHub Push
       ↓
Webhook Sent
       ↓
Jenkins Triggered
       ↓
Build Starts
```

Open Jenkins:

Expected:

```text
Build Running Automatically
```

---

# Pipeline Execution Flow

Expected stages:

```text
Clone Repository
      ↓
Build Docker Image
      ↓
Load Image To Minikube
      ↓
Deploy To Kubernetes
      ↓
Restart Deployment
      ↓
Verify Pods
```

---

# Verify Deployment

Run:

```bash
kubectl get pods
```

Expected:

```text
New pod restarted
```

Age resets.

Meaning:

```text
New deployment successful
```

---

# How Webhook Works Internally

Real process:

```text
Git Push
      ↓
GitHub Detects Change
      ↓
HTTP POST Request
      ↓
Jenkins Endpoint
/github-webhook/
      ↓
Pipeline Triggered
      ↓
Deployment Starts
```

---

# Debugging Webhooks

---

## Check Jenkins Logs

Command:

```bash
docker logs jenkins
```

---

## Check Webhook Delivery

GitHub:

```text
Settings
      ↓
Webhooks
      ↓
Recent Deliveries
```

---

## Verify Jenkins Reachable

Open:

```text
http://EC2_IP:8080
```

If not opening:

Check SG rules.

---

# Complete CI/CD Architecture

Final automation flow:

```text
Developer Push
      ↓
GitHub
      ↓
Webhook
      ↓
Jenkins
      ↓
Docker Build
      ↓
Minikube Load
      ↓
Kubernetes Deploy
      ↓
Application Updated
```

---

# Pipeline Debugging & Common Jenkins Errors

This section explains:

```text
How to debug Jenkins pipeline failures
step-by-step
```

including:

- failed stages
- build logs
- Docker issues
- kubectl issues
- Minikube issues
- GitHub webhook failures
- Jenkins container failures
- troubleshooting workflow

---

# Why Debugging Matters

In real DevOps:

```text
Pipelines fail frequently
```

Common reasons:

```text
Docker issue
kubectl issue
GitHub issue
Kubernetes issue
Permission issue
Minikube issue
```

A DevOps engineer must know:

```text
How to debug failures quickly
```

---

# Debugging Workflow

When pipeline fails:

Always follow:

```text
Build Failed
      ↓
Identify Failed Stage
      ↓
Read Logs
      ↓
Find Root Cause
      ↓
Fix Issue
      ↓
Rebuild
```

Never randomly change things.

---

# Step 1 — Open Build Logs

Inside Jenkins:

```text
Dashboard
      ↓
Pipeline Job
      ↓
Build Number
      ↓
Console Output
```

Example:

```text
#12
```

---

## Purpose

Shows:

```text
Exact Failure Reason
```

---

## Example

Failed build:

```text
ERROR:
docker command not found
```

Meaning:

```text
Docker missing
inside Jenkins container
```

---

# Stage-by-Stage Debugging

---

# Stage 1 — Clone Repository Failed

---

## Error

```text
Failed to clone repository
```

---

## Causes

```text
Wrong GitHub URL
Private repo
Network issue
Git plugin missing
```

---

## Fix

Verify repo URL:

```text
https://github.com/
Sasmita-biswal967/
Cloud-Native-URL-Health-Monitoring.git
```

---

## Verify Git Installed

Inside Jenkins container:

```bash
docker exec -it jenkins bash
git --version
```

---

## Install Git

If missing:

```bash
apt update
apt install git -y
```

---

# Stage 2 — Docker Build Failed

---

## Error

```text
docker: command not found
```

---

## Cause

Docker CLI missing inside Jenkins container.

---

## Fix

Enter container:

```bash
docker exec -it jenkins bash
```

Install:

```bash
apt update
apt install docker.io -y
```

Verify:

```bash
docker --version
```

---

## Error

```text
permission denied
while trying to connect
docker daemon
```

---

## Cause

Docker socket permission issue.

---

## Fix

On EC2:

```bash
sudo chmod 666 \
/var/run/docker.sock
```

---

## Verify

Inside Jenkins:

```bash
docker ps
```

Should work.

---

## Error

```text
Cannot locate Dockerfile
```

---

## Cause

Wrong directory.

Your Dockerfile exists in:

```text
backend/
```

---

## Fix

Ensure:

```groovy
dir('backend')
```

exists.

---

# Stage 3 — Minikube Image Load Failed

---

## Error

```text
minikube: command not found
```

---

## Cause

Minikube missing inside container.

---

## Fix

Install Minikube CLI.

Command:

```bash
curl -LO \
https://storage.googleapis.com/
minikube/releases/latest/
minikube-linux-amd64
```

Install:

```bash
install \
minikube-linux-amd64 \
/usr/local/bin/minikube
```

Verify:

```bash
minikube version
```

---

## Error

```text
minikube not running
```

---

## Cause

Cluster stopped.

---

## Fix

On EC2:

```bash
minikube start
```

Verify:

```bash
minikube status
```

Expected:

```text
Running
```

---

# Stage 4 — Kubernetes Deploy Failed

---

## Error

```text
kubectl: command not found
```

---

## Cause

kubectl missing.

---

## Fix

Install kubectl.

Verify:

```bash
kubectl version --client
```

---

## Error

```text
Unable to connect
to server
```

---

## Cause

Kubernetes config not mounted.

---

## Fix

Ensure container mounts:

```bash
-v ~/.kube:
/var/jenkins_home/.kube

-v ~/.minikube:
/var/jenkins_home/.minikube
```

---

## Verify

Inside Jenkins:

```bash
kubectl get pods
```

Should work.

---

## Error

```text
deployment not found
```

---

## Cause

Wrong deployment name.

Verify:

```bash
kubectl get deployment
```

Expected:

```text
url-monitor-deployment
```

---

# Stage 5 — Restart Deployment Failed

---

## Error

```text
deployment
"url-monitor-deployment"
not found
```

---

## Cause

Deployment name mismatch.

---

## Fix

Check:

```bash
kubectl get deployment
```

Update Jenkinsfile.

---

# Stage 6 — Verify Pods Failed

---

## Error

```text
CrashLoopBackOff
```

---

## Cause

Container crash.

---

## Fix

Check pod logs:

```bash
kubectl logs POD_NAME
```

---

## Example

```text
ModuleNotFoundError
```

Fix:

```text
requirements.txt missing package
```

Rebuild Docker image.

---

# Kubernetes Debugging Commands

---

## View Pods

```bash
kubectl get pods
```

---

## View Services

```bash
kubectl get svc
```

---

## Describe Pod

```bash
kubectl describe pod POD_NAME
```

Useful for:

```text
ImagePullBackOff
Pending
CrashLoopBackOff
```

---

## View Logs

```bash
kubectl logs POD_NAME
```

---

## Restart Deployment

```bash
kubectl rollout restart deployment \
url-monitor-deployment
```

---

# GitHub Webhook Debugging

---

## Error

```text
Build not triggered
```

---

## Fix

Check:

```text
GitHub Webhook
```

Go:

```text
Repository
      ↓
Settings
      ↓
Webhooks
      ↓
Recent Deliveries
```

Expected:

```text
200 OK
```

---

## Error

```text
404
```

---

## Cause

Wrong webhook URL.

Correct:

```text
http://EC2_IP:8080/
github-webhook/
```

---

## Error

```text
403
```

---

## Cause

Trigger disabled.

Fix:

Enable:

```text
GitHub hook trigger
for GITScm polling
```

---

# Jenkins Container Debugging

---

## Check Container Running

Command:

```bash
docker ps
```

Expected:

```text
jenkins
```

---

## View Jenkins Logs

Command:

```bash
docker logs jenkins
```

---

## Restart Jenkins

Command:

```bash
docker restart jenkins
```

---

## Enter Container

Command:

```bash
docker exec -it jenkins bash
```

---

# Pipeline Best Practices

---

## 1. Read Console Output First

Never guess.

Always check:

```text
Console Output
```

---

## 2. Test Commands Manually

Example:

Pipeline failing:

```bash
kubectl apply
```

Run manually on EC2.

---

## 3. Verify Kubernetes First

Check:

```bash
kubectl get pods
```

---

## 4. Verify Docker Image

Check:

```bash
docker images
```

---

## 5. Restart Deployment

Sometimes image cache issue.

Run:

```bash
kubectl rollout restart deployment \
url-monitor-deployment
```

---

# Real Debugging Workflow

Example:

```text
Pipeline Failed
      ↓
Console Output
      ↓
kubectl error
      ↓
Enter Jenkins Container
      ↓
Test kubectl manually
      ↓
Fix kubeconfig issue
      ↓
Rebuild pipeline
```

---

# Common CI/CD Errors Summary

| Error | Cause | Fix |
|--------|--------|-----|
| docker not found | Docker CLI missing | install docker.io |
| kubectl not found | kubectl missing | install kubectl |
| minikube not found | missing CLI | install minikube |
| webhook not triggering | bad URL | fix webhook |
| permission denied | docker socket | chmod 666 |
| deployment not found | wrong name | verify kubectl get deployment |
| CrashLoopBackOff | app crash | kubectl logs |

---