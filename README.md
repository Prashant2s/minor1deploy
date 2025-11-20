# Certificate Verification Using AI Summarizer

A certificate verification system that uses AI to extract information from uploaded certificates and verify them against a university database. The project includes a Python backend, a web portal, and Docker-based deployment.

# Features

- AI-based certificate text extraction (OCR + model processing)
- Verification against a stored university database
- Clean web portal for uploading and checking certificates
- Fully containerized using Docker and docker-compose

# Tech Stack

- **Backend**: Python (FastAPI / Flask)  
- **Frontend / Portal**: HTML/CSS/JS 
- **Database**: (e.g., postgreSQl,SQlite)
- **Deployment**: Docker & docker-compose

# Prerequisites
- Docker & Docker Compose  
- Environment variables configured via `.env` (see `.env.example`)  
- Database (as per `docker-compose.yml`)  

# Installation & Running Locally
1. Clone the repo  
2. Copy `.env.example` → `.env` and set your secrets  
3. Run `docker-compose up --build`  
4. Backend API will be available on `localhost:…` and Portal on `localhost:…`  

## Deployment
Use the `docker` folder to deploy using your chosen environment (cloud / VPS). The `DEPLOYMENT_GUIDE.md` has step-by-step deployment instructions.
