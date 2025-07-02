# STAC API Project

## Overview
This project implements a SpatioTemporal Asset Catalog (STAC) compliant API service for searching satellite imagery based on spatial and temporal queries. The service is designed to facilitate environmental analysis by providing easy access to satellite datasets.

## Project Structure
```
stac-api-project
├── stac_api
│   ├── api
│   │   ├── main.py          # Entry point for the API service
│   │   └── routes.py        # Defines API endpoints
│   ├── db
│   │   ├── models.py        # Database models for STAC metadata
│   │   └── database.py      # Database connection management
│   ├── stac
│   │   ├── catalog.json     # Root catalog for STAC implementation
│   │   └── items            # Directory containing individual STAC Item JSON files
│   ├── utils
│   │   └── stac_utils.py    # Utility functions for STAC metadata handling
│   └── tests
│       └── test_search.py    # Unit tests for the search endpoint
├── requirements.txt          # Project dependencies
├── docker-compose.yml        # Containerized environment configuration
├── Dockerfile                # Instructions for building the Docker image
├── .env.example              # Example environment variables
├── README.md                 # Project documentation
└── setup.py                  # Packaging and installation metadata
```

## Core Requirements
- **Data Acquisition**: The project includes a sample of satellite imagery sourced from an open data provider.
- **Metadata Generation**: The acquired imagery is cataloged in compliance with the STAC specification.
- **Database Integration**: STAC metadata is stored in a PostgreSQL database, designed for efficient querying of geospatial and temporal attributes.

## Setup Instructions
1. **Clone the Repository**:
   ```
   git clone <repository-url>
   cd stac-api-project
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.8 or higher installed. Then, install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. **Set Up the Database**:
   - Create a PostgreSQL database and configure the connection details in a `.env` file based on the `.env.example` provided.
   - Run the database migrations (if applicable) to set up the schema.

4. **Run the API Service**:
   Start the API service using:
   ```
   uvicorn stac_api.api.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Access the API**:
   The API will be available at `http://localhost:8000`. You can use tools like Postman or cURL to interact with the endpoints.

## Usage Example
To perform a search against the API, you can use the following Python script:

```python
from pystac_client import Client

API_URL = "http://localhost:8000"  # Replace with your server's address/endpoint
catalog = Client.open(API_URL)

search_bbox = [77.5, 12.9, 77.7, 13.1]  # Example bounding box over Bangalore
search_datetime = "2023-11-01"  # Date of the satellite imagery

search = catalog.search(
    collections=["sentinel-2-l2a"],  # Replace with your collection name
    bbox=search_bbox,
    datetime=search_datetime,
    method="POST"
)

print(f"Found {search.matched()} items")
for item in search.items():
    print(f" - Item ID: {item.id}, Date: {item.datetime.date()}")
```

## Design Choices
- **Database Schema**: The schema is designed to efficiently store and query geospatial and temporal attributes of satellite imagery.
- **API Framework**: FastAPI is chosen for its performance and ease of use in building RESTful APIs.

## Testing
Unit tests are provided in `stac_api/tests/test_search.py` to verify the functionality of the search endpoint. Run the tests using:
```
pytest stac_api/tests
```

## Conclusion
This STAC API project serves as a proof-of-concept for a geospatial data infrastructure, enabling efficient access to satellite imagery for environmental analysis.

# Enable pgGIS
CREATE EXTENSION postgis;
SELECT PostGIS_full_version();