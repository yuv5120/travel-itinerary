# Travel Itinerary Backend

A FastAPI backend system for managing travel itineraries

## Features
- SQLAlchemy database schema for itineraries, hotels, activities, and transfers
- REST API endpoints for creating and viewing itineraries
- MCP server endpoint for recommended itineraries based on duration

## Setup
```bash
pip install -r requirements.txt
uvicorn main:app --reload
