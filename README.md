# Cloud-Native Task Manager

A containerized Task Management application designed with a microservices architecture. This project demonstrates advanced cloud deployment strategies, including fully automated CI/CD pipelines, robust relational database design, and strict SSL/TLS security enforcement.

## ✨ Key Features
* **Secure Authentication:** User registration, login, and session management.
* **Full CRUD Operations:** Create, Read, Update, and Delete tasks seamlessly.
* **Advanced Relational Data:** Utilizes One-to-Many (Categories) and Many-to-Many (Tags) database relationships.
* **Optimized Containerization:** Multi-stage Docker builds keeping the application image size minimal.
* **Zero-Downtime CI/CD:** Automated testing, building, and deployment via GitHub Actions.
* **Enterprise Security:** Nginx reverse proxy with Let's Encrypt SSL termination and HTTP-to-HTTPS redirection.

## 🏗️ Technology Stack
1. **Ingress Controller:** Nginx handles incoming traffic, serves static files, and routes dynamic requests securely over Port 443.
2. **Application Server:** Gunicorn serves the Django 6.0 application, decoupled from the host network.
3. **Database:** PostgreSQL 15 provides persistent, stateless data storage via isolated Docker volumes.

## 🚀 Local Setup Instructions

### Prerequisites
* Docker and Docker Compose installed on local machine.
* Git.
* Python 3.12+

 **Clone the repository:**
   ```bash
   git clone https://github.com/Zafarbek05/DSCC-CW-00016417.git
   cd DSCC-CW-00016417
   ```

 **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   ```

 **Activate the Virtual Environment:**
   ```bash
   venv\Scripts\activate
   ```
 
 **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

 **Create Environment Variables (.env) file:**
   ```bash
   cp .env.example .env
   ```

## 🔄 Deployment Instructions

### This application is configured for Continuous Deployment to an Azure Virtual Machine.

1. **Server Provisioning:** Ensure the host server has Docker and Docker Compose installed, and ports 80 (HTTP), 443 (HTTPS), and 22 (SSH) are open.

2. **GitHub Secrets:** Configure the following repository secrets for the CI/CD pipeline:

    * *SSH_HOST:* The public IP of your Virtual Machine
    * *SSH_USERNAME:* Your host username
    * *SSH_PRIVATE_KEY:* Private RSA key for server access
    * *DOCKERHUB_USERNAME & DOCKERHUB_TOKEN*: for pushing the images

3. **Push Changes to GitHub:** pushing changes to the main branch triggers CI/CD pipeline

4. **Pipeline Execution:** GitHub Actions will run tests, build the Docker image and deploy to the server

## ⚙️ Environment Variables Documentation
To run this application, you must create a `.env` file in the root directory. This decouples sensitive credentials from the source code.

| Variable | Description | Development Value | Production Value |
| :--- | :--- | :--- | :--- |
| `DEBUG` | Toggles Django's debug mode and SSL enforcement. | `True` | `False` |
| `SECRET_KEY` | Cryptographic key for session/cookie hashing. | `django-insecure-...` | `[Secure Random String]` |
| `ALLOWED_HOSTS` | Comma-separated list of permitted domains. | `localhost,127.0.0.1` | `django16417.duckdns.org` |
| `DB_ENGINE` | The database backend to utilize. | `django.db.backends.postgresql` | `django.db.backends.postgresql` |
| `DB_NAME` | Name of the PostgreSQL database. | `postgres` | `postgres` |
| `DB_USER` | PostgreSQL superuser account name. | `postgres` | `admin` |
| `DB_HOST` | Hostname of the database server. | `db` | `db` |
| `DB_PORT` | Port exposed by the database. | `5432` | `5432` |