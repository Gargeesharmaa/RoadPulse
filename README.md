# RoadPulse AI
### Community-Driven Traffic & Road Infrastructure Intelligence

RoadPulse AI is an AI-powered platform that enables citizens to report road infrastructure issues such as potholes, waterlogging, accidents, blocked roads, and traffic signal failures. The system automatically analyzes uploaded images, classifies incidents, detects duplicate reports, assigns the appropriate government department, and stores reports for monitoring and analytics.

This project was built as an MVP for an Agentic AI Hackathon.

---

## Problem Statement

Road infrastructure issues often remain unreported or are reported through informal channels.

As a result:

- Delayed repairs
- Vehicle damage
- Traffic congestion
- Increased accident risk
- Lack of transparency

RoadPulse AI solves this by creating a community-driven reporting platform powered by AI.

---

# MVP Features

- Upload road issue images
- AI-powered image analysis
- Automatic incident classification
- Severity prediction
- Duplicate report detection using embeddings
- Automatic department routing
- Report management dashboard
- Analytics dashboard
- SQLite database
- REST API using FastAPI
- Modern Streamlit frontend

---

# Supported Incidents

- Pothole
- Waterlogging
- Accident
- Blocked Road
- Signal Failure
- Construction
- Normal Road

---

# Project Workflow

```text
             Citizen

                │
                ▼

      Upload Image + Location

                │
                ▼

          Streamlit Frontend

                │

                ▼

          FastAPI Backend

                │

                ▼

        AI Processing Pipeline

     ┌──────────────┬──────────────┬─────────────┐
     │              │              │             │
     ▼              ▼              ▼             ▼

 Image AI      Embedding      Duplicate      Routing
 Analysis      Generation      Detection     Department

     └──────────────┬──────────────┬─────────────┘

                    ▼

             SQLite Database

                    │

                    ▼

        Reports + Dashboard + Analytics
```

---

# Tech Stack

## Frontend

- Streamlit
- Plotly
- Folium
- Requests

---

## Backend

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

---

## AI

- Google Gemini Vision (Image Understanding)
- Groq LLM
- Sentence Transformers
- Cosine Similarity

---

## Deployment

- Render
- GitHub

---

# Project Structure

```text
RoadPulse-AI/

│

├── frontend/
│   └── app.py
│
├── api/
│   └── routes.py
│
├── database/
│   ├── db.py
│   ├── crud.py
│   └── models.py
│
├── schemas/
│   └── report.py
│
├── services/
│   ├── gemini.py
│   ├── embedding.py
│   ├── duplicate.py
│   ├── routing.py
│   └── pipeline.py
│
├── static/
│   └── uploads/
│
├── main.py
│
├── requirements.txt
│
└── README.md
```

---

# API Workflow

```text
POST /reports

        │

        ▼

Upload Image

        │

        ▼

Analyze Image

        │

        ▼

Generate Embedding

        │

        ▼

Check Duplicate

        │

        ▼

Assign Department

        │

        ▼

Save Database

        │

        ▼

Return JSON Response
```

---

# Dashboard

The dashboard provides:

- Total reports
- Pending complaints
- Resolved complaints
- Critical incidents
- Recent activity
- AI insights

---

# Analytics

- Incident Distribution
- Severity Analysis
- Department-wise Complaints
- Resolution Status
- Infrastructure Statistics

---

# Installation

Clone the repository

```bash
git clone https://github.com/yourusername/RoadPulse-AI.git
```

Move into the project

```bash
cd RoadPulse-AI
```

Create a virtual environment

```bash
python -m venv venv
```

Activate virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

---

# Run Backend

```bash
uvicorn main:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

---

# Run Frontend

```bash
streamlit run frontend/app.py
```

---

# Future Scope

If more development time is available, RoadPulse AI can be extended with:

- Real-time traffic prediction
- Live alternate route recommendation
- GPS-based automatic location detection
- Government complaint portal integration
- WhatsApp and Telegram reporting
- Push notifications
- Ward-level infrastructure quality score
- AI-based complaint verification from multiple users
- Multi-language support
- Real-time admin dashboard
- Cloud deployment with PostgreSQL
- Authentication and user profiles

---

# Why RoadPulse AI?

RoadPulse AI combines Artificial Intelligence, Computer Vision, GIS, and Community Reporting to create a smarter, safer, and more responsive road infrastructure management system.

Instead of simply collecting complaints, the platform analyzes, validates, prioritizes, and routes issues automatically, reducing manual effort and enabling faster action.

---

# Contributors

Developed for the Agentic AI Hackathon.

---

# License

This project is intended for educational and hackathon purposes.
