# NexusID - UBID & Business Activity Intelligence

## Overview
NexusID is an AI-powered platform that generates a Unified Business Identifier (UBID) and classifies business activity.

## Features
- Entity matching with confidence scoring
- Explainable AI decisions
- Activity classification (Active/Dormant/Closed)
- Query engine for insights

## Setup Instructions

### 1. Clone Repository
git clone <repo_url>
cd nexusid

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Run Application
cd backend
uvicorn app:app --reload

### 4. Access API
http://127.0.0.1:8000/docs

## Demo Endpoints

### Match Records
/match?id1=1&id2=2

### Activity Status
/activity/1

### Query
/query?pincode=560001
