
# Travel Itinerary Backend

A FastAPI backend system for managing travel itineraries

## ✈️ Features

- SQLAlchemy database schema for itineraries, hotels, activities, and transfers (Goa & Manali regions)
- REST API endpoints for creating and viewing itineraries
- MCP server endpoint to recommend itineraries based on trip duration
- Seeded realistic data (Indian places): Goa Beach Resort, Manali Mountain Retreat, Scuba Diving, Paragliding

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/sde-assignment-travel-itinerary.git
cd sde-assignment-travel-itinerary
```

### 2️⃣ Create virtual environment & activate

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the FastAPI server

```bash
uvicorn main:app --reload
```

The server will auto-create a `travel.db` SQLite database and seed Indian data.

## 🛠️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/docs` | Swagger API Documentation |
| POST | `/itineraries/` | Create a new itinerary |
| GET | `/itineraries/` | View all itineraries |
| GET | `/mcp/{nights}` | Get recommended itineraries for given nights |

## 🌍 Seeded Data (India)

| Hotels | Locations |
|--------|-----------|
| Goa Beach Resort | Goa |
| Manali Mountain Retreat | Manali |

| Activities | Locations |
|------------|-----------|
| Scuba Diving | Goa |
| Paragliding | Manali |

| Transfers |
|-----------|
| Goa → Manali |
| Manali → Goa |

## 🧪 Example API Test

**POST /itineraries/**

```json
{
  "name": "Goa Adventure Trip",
  "nights": 5,
  "hotel_id": 1,
  "activity_ids": [1],
  "transfer_ids": [1]
}
```

## 📋 Author

Yuvraj Singh Gour  
[GitHub: yuv5120](https://github.com/yuv5120)

---
