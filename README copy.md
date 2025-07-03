# STAC API Proof-of-Concept

## Overview
This project implements a minimal SpatioTemporal Asset Catalog (STAC) API for searching satellite imagery by space and time, using PostgreSQL/PostGIS and FastAPI.

## Design Choices
- **Database:** PostgreSQL with PostGIS for spatial queries. Table `stacitem` stores STAC Items with geometry and asset metadata.
- **API:** FastAPI for modern, async web API. Search endpoint supports bbox and datetime filters, returns STAC-compliant GeoJSON.
- **Containerization:** Docker and docker-compose for easy local setup.

## Setup Instructions

### 1. Clone the repository
```sh
git clone <your-repo-url>
cd STAC-API
```

### 2. Build and start services
```sh
docker-compose up --build
```
This will start both the PostGIS database and the STAC API server.

### 3. Initialize the database
In a new terminal, load the sample data:
```sh
docker-compose exec db psql -U postgres -d stac-db -f db/init_stac_db.sql
```

### 4. Query the API
Example cURL:
```sh
curl -X POST "http://localhost:8000/v1/stac/search?bbox=77.5,12.9,77.7,13.1&datetime=2023-11-01T00:00:00Z/2023-11-30T23:59:59Z"
```

Example Python (using requests):
```python
import requests
url = "http://localhost:8000/v1/stac/search"
params = {"bbox": "77.5,12.9,77.7,13.1", "datetime": "2023-11-01T00:00:00Z/2023-11-30T23:59:59Z"}
r = requests.post(url, params=params)
print(r.json())
```

## Testing
Run tests with:
```sh
pytest
```

## Notes
- See `db/init_stac_db.sql` for sample data and schema.
- API returns STAC-compliant GeoJSON with correct content type.
