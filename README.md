# Cloud Management System

A GUI-based Cloud Management System built with Python and PySimpleGUI that allows users to manage virtual machines (VMs) and Docker containers seamlessly from a single desktop interface.

## 📌 Features

### 🖥️ Virtual Machine Management (QEMU)
- Launch virtual machines with predefined settings:
  - **Low-Power** (1 CPU, 512MB RAM, 10GB Disk)
  - **Standard** (2 CPU, 1024MB RAM, 20GB Disk)
  - **High-Performance** (4 CPU, 2048MB RAM, 40GB Disk)
- Customize CPU cores, memory (MB), and disk size (GB)
- Simple click-to-launch interface using `qemu-system-x86_64`

### 🐳 Docker Management
- **Create Dockerfiles** from GUI
- **Build Docker images** with custom names
- **List available Docker images**
- **List running containers**
- **Stop containers** by ID
- **Search Docker Hub** for public images
- **Pull images** from Docker Hub

## 🛠️ Technologies Used

- **Python 3.x**
- **PySimpleGUI** – for building the GUI
- **QEMU** – for VM emulation
- **Docker CLI** – for container management
- **Subprocess module** – to handle shell command execution

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Docker installed and configured
- QEMU installed and accessible via command line
- Windows OS (paths are Windows-style)

