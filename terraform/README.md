# Terraform Workflow & AWS Infrastructure Setup

This section explains:

```text
How Terraform creates AWS infrastructure
from start to finish
```

including:

- terraform init
- terraform validate
- terraform plan
- terraform apply
- terraform destroy
- terraform state
- SSH access
- EC2 provisioning lifecycle
- S3 provisioning
- debugging
- common errors

---

# Terraform Architecture

Your Terraform infrastructure flow:

```text
Terraform Code
       ↓
Terraform CLI
       ↓
AWS Provider
       ↓
AWS API
       ↓
Resources Created
       ↓
EC2 + Security Group + EBS + S3
```

---

# Infrastructure Created

When Terraform runs, it creates:

```text
EC2 Instance
Security Group
EBS Storage
S3 Bucket
Networking Rules
```

---

# Terraform File Flow

Terraform reads files in this order:

```text
variables.tf
       ↓
main.tf
       ↓
outputs.tf
```

Meaning:

```text
Variables Loaded
       ↓
Resources Created
       ↓
Outputs Displayed
```

---

# Step 1 — Terraform Initialization

## Command

```bash
terraform init
```

---

## Purpose

Initializes Terraform project.

Downloads:

```text
AWS Provider
Required Plugins
Dependencies
```

---

## Internal Workflow

```text
terraform init
        ↓
Check Configuration
        ↓
Download AWS Provider
        ↓
Create .terraform Folder
        ↓
Ready to Deploy
```

---

## Expected Output

```text
Terraform has been successfully initialized!
```

---

## What Gets Created?

Terraform creates:

```text
.terraform/
```

folder.

Contains:

```text
Downloaded providers
Plugin files
Dependencies
```

---

## Verify

Command:

```bash
dir
```

or:

```bash
ls
```

Expected:

```text
.terraform
```

folder exists.

---

# Step 2 — Validate Configuration

## Command

```bash
terraform validate
```

---

## Purpose

Checks:

```text
Terraform syntax correctness
```

before deployment.

Like:

```text
Code Error Checking
```

---

## Internal Workflow

```text
Terraform Files
        ↓
Syntax Validation
        ↓
Error Check
        ↓
Pass/Fail
```

---

## Expected Output

```text
Success! The configuration is valid.
```

---

## Why Important?

Prevents deployment failure.

Without validate:

- Syntax mistakes  
- Resource reference errors

---

## Example Error

Bad code:

```terraform
instance_type =
var.instance_typ
```

Expected error:

```text
Reference to undeclared variable
```

---

# Step 3 — Execution Plan

## Command

```bash
terraform plan
```

---

## Purpose

Shows:

```text
What Terraform WILL create
```

before creating resources.

Safe preview mode.

---

## Internal Workflow

```text
Current AWS State
         ↓
Terraform Config
         ↓
Compare Difference
         ↓
Show Execution Plan
```

---

## Expected Output

Example:

```text
Plan:
3 to add,
0 to change,
0 to destroy
```

---

## What Will Be Created?

Expected:

```text
aws_security_group
aws_instance
aws_s3_bucket
```

---

## Why Important?

Prevents mistakes.

Example:

Before accidental deletion:

```text
1 to destroy
```

You stop immediately.

---

# Step 4 — Infrastructure Deployment

## Command

```bash
terraform apply
```

---

## Purpose

Actually creates AWS resources.

---

## Terraform Prompt

Terraform asks:

```text
var.key_name
Enter a value:
```

Type:

```text
cloud-url-monitor-key
```

(Your EC2 key pair name)

---

## Confirmation

Terraform asks:

```text
Do you want to perform these actions?
```

Type:

```text
yes
```

---

## Internal Workflow

```text
Terraform
       ↓
AWS Provider
       ↓
AWS API
       ↓
Security Group Created
       ↓
EC2 Created
       ↓
EBS Attached
       ↓
S3 Bucket Created
       ↓
Outputs Displayed
```

---

## Expected Output

```text
Apply complete!
```

Then:

```text
Outputs:

ec2_public_ip =
44.xx.xx.xx

ec2_public_dns =
ec2-xx-xx.compute.amazonaws.com

s3_bucket_name =
cloud-url-monitor-reports-12345
```

---

# Step 5 — Verify Resources in AWS

Open:

```text
AWS Console
```

---

## EC2

Go:

```text
EC2
   ↓
Instances
```

Expected:

```text
cloud-url-monitor
```

State:

```text
Running
```

---

## Security Group

Go:

```text
EC2
   ↓
Security Groups
```

Expected:

```text
url-monitor-sg
```

---

## S3

Go:

```text
S3
```

Expected bucket:

```text
cloud-url-monitor-reports-12345
```

---

# Step 6 — SSH into EC2

## Command

Windows PowerShell:

```powershell
ssh -i "cloud-url-monitor-key.pem" ec2-user@PUBLIC_IP
```

Example:

```powershell
ssh -i "cloud-url-monitor-key.pem" ec2-user@44.xx.xx.xx
```

---

## Purpose

Connects to server.

---

## Internal Workflow

```text
SSH Key
      ↓
EC2 Authentication
      ↓
Secure Access
      ↓
Terminal Opened
```

---

## Expected Output

```text
[ec2-user@ip-172-31-x-x ~]$
```

Meaning:

✅ Login successful

---

# Step 7 — Verify Storage (EBS)

Go:

```text
EC2
   ↓
Volumes
```

Expected:

```text
20 GB
gp3
```

---

## Why EBS?

Stores:

```text
Docker Images
Containers
Kubernetes Files
Monitoring Data
```

Without storage:

Server unusable

---

# Step 8 — View Terraform State

## Command

```bash
terraform state list
```

---

## Purpose

Shows:

```text
Managed Resources
```

Expected:

```text
aws_instance.url_monitor_ec2
aws_security_group.url_monitor_sg
aws_s3_bucket.monitor_reports
```

---

# Step 9 — View Outputs Again

## Command

```bash
terraform output
```

---

## Purpose

Displays infrastructure info again.

Expected:

```text
ec2_public_ip
ec2_public_dns
s3_bucket_name
```

---

# Step 10 — Destroy Infrastructure

## Command

```bash
terraform destroy
```

---

## Purpose

Deletes:

```text
EC2
Security Group
S3
EBS
```

Avoids AWS charges.

---

## Confirmation

Terraform asks:

```text
Do you really want to destroy?
```

Type:

```text
yes
```

---

## Internal Workflow

```text
Terraform State
       ↓
AWS API
       ↓
Delete Resources
       ↓
Clean Infrastructure
```

---

# Terraform State File

Terraform automatically creates:

```text
terraform.tfstate
```

---

## Purpose

Stores:

```text
Infrastructure Metadata
```

Terraform remembers:

```text
What resources exist
```

---

## Why Important?

Without state:

Terraform loses tracking.

---

# Behind the Scenes

Real infrastructure flow:

```text
terraform apply
        ↓
AWS Authentication
        ↓
Security Group Created
        ↓
EC2 Launch
        ↓
EBS Attach
        ↓
S3 Create
        ↓
Outputs Displayed
```

---

# File: `main.tf`

## Purpose of This File

The `main.tf` file is the most important Terraform file.

It is responsible for:

- Creating AWS infrastructure
- Launching EC2 instance
- Creating Security Groups
- Opening ports
- Configuring EBS storage
- Creating S3 bucket
- Connecting resources together

Think:

```text
Terraform Code
        ↓
AWS API
        ↓
Infrastructure Created
```

Without `main.tf`:

- No EC2 instance  
- No AWS infrastructure  
- No security rules  
- No storage

This file acts as:

```text
Infrastructure Blueprint
```

---

# Complete Code

```terraform
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_security_group" "url_monitor_sg" {
  name        = "url-monitor-sg"
  description = "Security Group for URL Monitor"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "FastAPI"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Grafana"
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Prometheus"
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Kubernetes NodePort"
    from_port   = 30000
    to_port     = 32767
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "url-monitor-security-group"
  }
}

resource "aws_instance" "url_monitor_ec2" {

  ami           = "ami-0236922087fa98b6e"
  instance_type = var.instance_type

  key_name = var.key_name

  vpc_security_group_ids = [
    aws_security_group.url_monitor_sg.id
  ]

  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }

  tags = {
    Name = "cloud-url-monitor"
  }
}

resource "aws_s3_bucket" "monitor_reports" {
  bucket = "cloud-url-monitor-reports-12345"

  tags = {
    Name = "Cloud URL Monitor Reports"
  }
}
```

---

# Understanding the Code Line by Line

---

# Terraform Block

## Code

```terraform
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

---

## Purpose

Defines:

```text
Terraform Requirements
```

Specifies:

- provider source
- provider version

---

# Required Provider

## Code

```terraform
aws = {
  source  = "hashicorp/aws"
  version = "~> 5.0"
}
```

---

## Purpose

Tells Terraform:

```text
Use AWS Provider
```

from:

```text
HashiCorp Registry
```

---

## Why Needed?

Terraform itself cannot talk to AWS.

AWS provider acts like:

```text
Translator
```

between:

```text
Terraform ↔ AWS API
```

---

## Version

### Code

```terraform
~> 5.0
```

---

## Meaning

Use:

```text
Version 5.x
```

but not breaking upgrades.

Example:

Allowed:

```text
5.1
5.3
5.9
```

Not allowed:

```text
6.0
```

---

# Provider Block

## Code

```terraform
provider "aws" {
  region = var.aws_region
}
```

---

## Purpose

Configures AWS connection.

Defines:

```text
Which AWS region
to deploy resources
```

---

## Region Variable

### Code

```terraform
var.aws_region
```

Comes from:

```text
variables.tf
```

Value:

```text
us-east-1
```

---

## Why Important?

Resources deploy in:

```text
Virginia Region
(us-east-1)
```

---

## Internal Workflow

```text
Terraform
      ↓
AWS Provider
      ↓
Connect us-east-1
      ↓
Create Resources
```

---

# Security Group Resource

## Code

```terraform
resource "aws_security_group"
"url_monitor_sg"
```

---

## Purpose

Creates:

```text
Firewall Rules
```

for EC2.

Think:

```text
Security Gate
```

Controls:

```text
Allowed Traffic
Blocked Traffic
```

Without SG:

- Cannot SSH  
- FastAPI inaccessible  
- Grafana inaccessible  
- Kubernetes broken

---

# Security Group Name

## Code

```terraform
name = "url-monitor-sg"
```

---

## Purpose

Visible in AWS console.

Used for identification.

---

# SSH Ingress Rule

## Code

```terraform
ingress {
  description = "SSH"

  from_port = 22
  to_port   = 22
}
```

---

## Purpose

Allows:

```text
SSH Login
```

to EC2.

---

## Port 22

Used for:

```text
Remote Server Access
```

Example:

```bash
ssh -i key.pem ec2-user@PUBLIC_IP
```

---

## Protocol

```terraform
tcp
```

SSH works over TCP.

---

## CIDR

```terraform
0.0.0.0/0
```

Means:

```text
Anyone can access
```

---

# FastAPI Port

## Code

```terraform
8000
```

---

## Purpose

Allows:

```text
FastAPI Access
```

Example:

```text
http://EC2_IP:8000
```

---

# Grafana Port

## Code

```terraform
3000
```

---

## Purpose

Allows:

```text
Grafana Dashboard Access
```

Example:

```text
http://EC2_IP:3000
```

---

# Prometheus Port

## Code

```terraform
9090
```

---

## Purpose

Allows:

```text
Prometheus UI Access
```

Example:

```text
http://EC2_IP:9090
```

---

# Kubernetes NodePort Range

## Code

```terraform
30000–32767
```

---

## Purpose

Allows:

```text
Kubernetes Services
```

through NodePort.

Example:

```text
http://EC2_IP:31245
```

---

## Why Needed?

Minikube/Kubernetes exposes services using:

```text
NodePort
```

---

# Egress Rule

## Code

```terraform
egress
```

---

## Purpose

Controls:

```text
Outgoing Traffic
```

---

## Code

```terraform
protocol = "-1"
```

Meaning:

```text
Allow All Protocols
```

---

## CIDR

```terraform
0.0.0.0/0
```

Meaning:

```text
Anywhere Internet
```

EC2 can:

- download Docker images  
- install packages  
- access AWS APIs

---

# Tags

## Code

```terraform
tags = {
  Name =
}
```

---

## Purpose

Adds labels in AWS.

Helpful for:

```text
Organization
Billing
Identification
```

---

# EC2 Instance Resource

## Code

```terraform
resource "aws_instance"
"url_monitor_ec2"
```

---

## Purpose

Creates:

```text
EC2 Virtual Machine
```

where project runs.

---

# AMI

## Code

```terraform
ami =
"ami-0236922087fa98b6e"
```

---

## Purpose

Defines:

```text
Operating System Image
```

This is:

```text
Amazon Linux
```

---

## Why AMI Needed?

EC2 needs OS to boot.

Like:

```text
Windows ISO
Linux ISO
```

for VM.

---

# Instance Type

## Code

```terraform
instance_type =
var.instance_type
```

---

## Value

```text
t3.micro
```

---

## Purpose

Defines:

```text
CPU + RAM
```

for EC2.

---

## t3.micro Specs

Approx:

```text
2 vCPU
1 GB RAM
```

Good for:

- Small DevOps project  
- Kubernetes practice

---

# Key Pair

## Code

```terraform
key_name =
var.key_name
```

---

## Purpose

Allows:

```text
SSH Authentication
```

without password.

---

## Example

Key:

```text
cloud-url-monitor-key.pem
```

Connect:

```bash
ssh -i cloud-url-monitor-key.pem ec2-user@IP
```

---

# Security Group Attachment

## Code

```terraform
vpc_security_group_ids
```

---

## Purpose

Attaches firewall to EC2.

Without this:

❌ No network access

---

## Reference

```terraform
aws_security_group
.url_monitor_sg.id
```

Meaning:

Attach created SG.

---

# Root Block Device

## Code

```terraform
root_block_device
```

---

## Purpose

Configures:

```text
EBS Storage
```

for EC2.

---

# Volume Size

## Code

```terraform
volume_size = 20
```

---

## Meaning

Creates:

```text
20GB Storage
```

Enough for:

- Docker
- Kubernetes
- Images
- Monitoring stack

---

# Volume Type

## Code

```terraform
gp3
```

---

## Purpose

Modern AWS SSD storage.

Benefits:

- Faster  
- Cheaper  
- Better performance

---

# S3 Bucket Resource

## Code

```terraform
resource "aws_s3_bucket"
"monitor_reports"
```

---

## Purpose

Creates:

```text
S3 Storage Bucket
```

for:

```text
Monitoring Reports
Logs
Exports
Backups
```

---

# Bucket Name

## Code

```terraform
bucket =
"cloud-url-monitor-reports-12345"
```

---

## Important

Must be:

```text
Globally Unique
```

If exists already:

Terraform fails.

Example fix:

```text
cloud-url-monitor-reports-yourname-2026
```

---

# Apply Infrastructure

## Commands

```bash
terraform init
terraform validate
terraform plan
terraform apply
```

---

## Internal Workflow

```text
Terraform Code
        ↓
AWS Provider
        ↓
AWS API
        ↓
Security Group
        ↓
EC2 Created
        ↓
EBS Attached
        ↓
S3 Created
```

---

# File: `variables.tf`

## Purpose of This File

The `variables.tf` file is responsible for:

- Making Terraform reusable
- Avoiding hardcoded values
- Improving maintainability
- Making infrastructure configurable

Think:

Instead of writing:

```terraform
region = "us-east-1"
```

everywhere,

we create:

```terraform
var.aws_region
```

and define it once.

This makes the project:

- Flexible  
- Cleaner  
- Easier to modify  
- Production-friendly

Without variables:

- Hardcoded configuration  
- Difficult updates  
- Repeated values

---

# Complete Code

```terraform
variable "aws_region" {
  default = "us-east-1"
}

variable "instance_type" {
  default = "t3.micro"
}

variable "key_name" {
  description = "EC2 Key Pair Name"
}
```

---

# Understanding the Code Line by Line

---

# Variable Block

## Code

```terraform
variable
```

---

## Purpose

Defines:

```text
Reusable Configuration Value
```

Think like:

```text
Python Variables
```

Example:

Python:

```python
name = "AWS"
```

Terraform:

```terraform
variable "aws_region"
```

---

# AWS Region Variable

## Code

```terraform
variable "aws_region" {
  default = "us-east-1"
}
```

---

## Purpose

Stores:

```text
AWS Deployment Region
```

Used in:

```terraform
provider "aws"
```

Example:

```terraform
provider "aws" {
  region = var.aws_region
}
```

---

## Default Value

### Code

```terraform
default = "us-east-1"
```

---

## Meaning

Terraform automatically uses:

```text
US East (N. Virginia)
```

unless changed manually.

---

## Why us-east-1?

Benefits:

- Cheapest region often  
- Maximum AWS support  
- Fast provisioning  
- Most tutorials/examples

---

## AWS Console View

You will see resources inside:

```text
N. Virginia
(us-east-1)
```

---

## Internal Workflow

```text
variables.tf
        ↓
aws_region variable
        ↓
provider block
        ↓
Terraform deploys in us-east-1
```

---

# Instance Type Variable

## Code

```terraform
variable "instance_type" {
  default = "t3.micro"
}
```

---

## Purpose

Defines:

```text
EC2 Machine Size
```

Used in:

```terraform
resource "aws_instance"
```

Example:

```terraform
instance_type =
var.instance_type
```

---

## Current Value

```text
t3.micro
```

---

## Why Variable?

Instead of changing:

```terraform
main.tf
```

every time,

you only change:

```terraform
variables.tf
```

Example:

Small Project:

```text
t3.micro
```

Bigger Project:

```text
t3.medium
```

Production:

```text
t3.large
```

---

# EC2 Size Meaning

## Current:

```text
t3.micro
```

Approx resources:

```text
2 vCPU
1 GB RAM
```

Good for:

- Terraform learning  
- Small FastAPI apps  
- DevOps practice

---

## If Kubernetes becomes heavy

Upgrade to:

```text
t3.medium
```

Approx:

```text
2 vCPU
4GB RAM
```

Better for:

```text
Docker
Minikube
Prometheus
Grafana
```

together.

---

# Key Name Variable

## Code

```terraform
variable "key_name" {
  description =
  "EC2 Key Pair Name"
}
```

---

## Purpose

Stores:

```text
EC2 SSH Key Name
```

Needed for:

```text
Secure Login
```

to EC2.

---

## Why No Default Value?

Because every AWS account has:

```text
Different Key Pair Name
```

Example:

Your key:

```text
cloud-url-monitor-key
```

Someone else's key:

```text
my-devops-key
```

So Terraform asks user during:

```bash
terraform apply
```

---

## Example Prompt

Terraform asks:

```text
var.key_name
Enter a value:
```

You enter:

```text
cloud-url-monitor-key
```

---

## Where Used?

Inside:

```terraform
aws_instance
```

Example:

```terraform
key_name =
var.key_name
```

---

## Why Important?

Without key pair:

❌ Cannot SSH into EC2

---

# SSH Workflow

```text
Key Pair
      ↓
Terraform EC2
      ↓
EC2 Attached Key
      ↓
SSH Authentication
      ↓
Server Access
```

---

# SSH Example

Command:

```bash
ssh -i "cloud-url-monitor-key.pem" ec2-user@PUBLIC_IP
```

---

# How Variables Work Together

```text
variables.tf
        ↓
main.tf references variables
        ↓
Terraform replaces values
        ↓
Infrastructure created
```

Example:

```terraform
var.instance_type
```

becomes:

```terraform
t3.micro
```

internally.

---

# Benefits of Variables

---

## 1. Reusability

Same Terraform code.

Different environments.

Example:

Development:

```text
t3.micro
```

Production:

```text
t3.large
```

---

## 2. Easy Maintenance

Update once.

Used everywhere.

---

## 3. Cleaner Code

No hardcoding.

Bad:

```terraform
instance_type =
"t3.micro"
```

Better:

```terraform
instance_type =
var.instance_type
```

---

## 4. Scalability

Easy environment switching.

---

# Variable Override Methods

Terraform variables can be overridden.

---

## Method 1 — Default Value

Current method:

```terraform
default =
```

Used automatically.

---

## Method 2 — terraform.tfvars

Example:

```terraform
instance_type = "t3.medium"
```

---

## Method 3 — CLI

Command:

```bash
terraform apply \
-var="instance_type=t3.medium"
```

---

# Verify Variables

Command:

```bash
terraform plan
```

Expected:

Terraform shows:

```text
instance_type = t3.micro
region = us-east-1
```

---

# Behind the Scenes

When Terraform runs:

```text
variables.tf
        ↓
Values Loaded
        ↓
main.tf Reads Variables
        ↓
Terraform Replaces Variables
        ↓
AWS Resources Created
```

---

# File: `outputs.tf`

## Purpose of This File

The `outputs.tf` file is responsible for:

- Displaying important infrastructure details
- Showing EC2 public IP
- Showing S3 bucket name
- Making AWS resources easier to access
- Avoiding manual AWS Console lookup

Think:

Without outputs:

```text
Terraform Creates Resources
        ↓
You manually search AWS Console
        ↓
Find EC2 IP
        ↓
Copy it
```

With outputs:

```text
Terraform Apply
        ↓
Instant Resource Information
Displayed Automatically
```

Much easier.

Without outputs:

- Manual AWS Console work  
- Hard to find EC2 IP  
- Slower workflow

---

# Complete Code

```terraform
output "ec2_public_ip" {
  description = "Public IP of EC2 Instance"

  value = aws_instance.url_monitor_ec2.public_ip
}

output "ec2_public_dns" {
  description = "Public DNS of EC2"

  value = aws_instance.url_monitor_ec2.public_dns
}

output "s3_bucket_name" {
  description = "S3 Bucket Name"

  value = aws_s3_bucket.monitor_reports.bucket
}
```

---

# Understanding the Code Line by Line

---

# Output Block

## Code

```terraform
output
```

---

## Purpose

Displays:

```text
Resource Information
```

after:

```bash
terraform apply
```

Think:

```text
Print Statement
```

for infrastructure.

Example:

Python:

```python
print(server_ip)
```

Terraform:

```terraform
output "ec2_public_ip"
```

---

# EC2 Public IP Output

## Code

```terraform
output "ec2_public_ip" {
```

---

## Purpose

Displays:

```text
EC2 Public IP Address
```

after deployment.

---

## Description

### Code

```terraform
description =
"Public IP of EC2 Instance"
```

---

## Purpose

Explains output purpose.

Helpful documentation.

---

## Value

### Code

```terraform
value =
aws_instance
.url_monitor_ec2
.public_ip
```

---

## Meaning

Terraform gets:

```text
EC2 Public IP
```

from:

```text
url_monitor_ec2 resource
```

---

## Example Output

After:

```bash
terraform apply
```

You may see:

```text
Outputs:

ec2_public_ip = "44.xx.xx.xx"
```

---

## Why Important?

Needed for:

### FastAPI

```text
http://44.xx.xx.xx:8000
```

---

### Grafana

```text
http://44.xx.xx.xx:3000
```

---

### Prometheus

```text
http://44.xx.xx.xx:9090
```

---

### SSH Login

```bash
ssh -i key.pem ec2-user@44.xx.xx.xx
```

---

# EC2 Public DNS Output

## Code

```terraform
output "ec2_public_dns"
```

---

## Purpose

Displays:

```text
Public DNS Address
```

instead of IP.

---

## Value

### Code

```terraform
aws_instance
.url_monitor_ec2
.public_dns
```

---

## Example Output

```text
ec2_public_dns =
ec2-44-xx-xx-xx.compute-1.amazonaws.com
```

---

## Why Useful?

Instead of IP:

```text
44.xx.xx.xx
```

you can use:

```text
ec2-44-xx-xx-xx.compute.amazonaws.com
```

---

## SSH Example

```bash
ssh -i key.pem \
ec2-user@ec2-44-xx-xx-xx.compute.amazonaws.com
```

---

# S3 Bucket Output

## Code

```terraform
output "s3_bucket_name"
```

---

## Purpose

Displays:

```text
S3 Bucket Name
```

after creation.

---

## Value

### Code

```terraform
aws_s3_bucket
.monitor_reports
.bucket
```

---

## Meaning

Gets bucket name from:

```text
monitor_reports
```

resource.

---

## Example Output

```text
s3_bucket_name =
cloud-url-monitor-reports-12345
```

---

## Why Useful?

Later used for:

- report storage
- monitoring logs
- backups
- Lambda uploads

without opening AWS Console.

---

# Internal Workflow

When Terraform runs:

```text
terraform apply
        ↓
AWS creates EC2
        ↓
AWS creates S3
        ↓
Terraform fetches metadata
        ↓
Outputs displayed
```

---

# Example Full Output

After:

```bash
terraform apply
```

Expected:

```text
Apply complete!

Outputs:

ec2_public_ip =
44.xx.xx.xx

ec2_public_dns =
ec2-44-xx-xx-xx.compute.amazonaws.com

s3_bucket_name =
cloud-url-monitor-reports-12345
```

---

# View Outputs Later

Even after deployment.

Command:

```bash
terraform output
```

---

## Example

```text
ec2_public_ip =
44.xx.xx.xx
```

---

## Single Output

Command:

```bash
terraform output ec2_public_ip
```

Expected:

```text
44.xx.xx.xx
```

---

# Why Outputs Matter

Without outputs:

```text
AWS Console
      ↓
EC2
      ↓
Copy Public IP
```

With outputs:

```text
terraform output
      ↓
Instant Access
```

Much faster.

---

# Behind the Scenes

Terraform flow:

```text
main.tf
      ↓
Resources Created
      ↓
outputs.tf Reads Metadata
      ↓
Displays Values
```

---


