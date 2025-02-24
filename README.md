# Blockhouse Work Trial

A **FastAPI-powered trading service** that allows users to **place trade orders** and **retrieve trade history** with a PostgreSQL database. The project is **fully containerized using Docker** and **deployed on AWS EC2** with an automated **CI/CD pipeline using GitHub Actions**.

## Features
**REST API for Trade Orders** (Place & Retrieve Orders)    
**PostgreSQL for Order Persistence**  
**Dockerized Deployment** for Scalability  
**CI/CD with GitHub Actions** (Automated Deployment to AWS EC2)  
**Deployed on AWS EC2**  

---

## Tech Stack
- **Backend:** Python, FastAPI, Uvicorn
- **Database:** PostgreSQL (Dockerized)
- **Containerization:** Docker, Docker Compose
- **Deployment:** AWS EC2 (Ubuntu)
- **CI/CD:** GitHub Actions

---

## Installation & Running Locally
To run this project locally, follow these steps:

### ** #1️ Clone the Repository**
```sh
git clone https://github.com/yourusername/Blockhouse.git
cd Blockhouse
```

### ** #2 Set up virtual environment & Install Dependencies
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### ** #3 Start FastAPI Server
uvicorn app.main:app --reload

## Running with Docker

### ** #1 Build and Run the Container
```sh
docker build -t blockhouse .
docker run -p 8000:8000 blockhouse
```
### API will be available at: http://localhost:8000/docs

### ** #2 Run with Docker Compose (Includes PostgreSQL)
```sh
docker-compose up -d
```

## CI/CD: Automated Deployment to AWS EC2
Everytime a push called to main, GitHub Actions will:
- SSH into EC2
- Pull the latest code
- Rebuild and restart the Docker container

**Secrets Configured in Github Actions:
- EC2_Host -> Your EC2 Public IP
- EC2_SSH_Key -> Your private key for SSH access

## API Endpoints
Method | Endpoint	| Description
POST	 | /orders	| Place a new trade order
GET	   | /orders  | Retrieve all orders

Swagger UI: http://your-ec2-public-ip:8000/docs

