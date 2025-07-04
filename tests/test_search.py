from pystac_client import Client

# URL of your locally running STAC API
API_URL = "http://localhost:8000/v1/stac/"  # Use the correct STAC Catalog endpoint

# Connect to the API
catalog = Client.open(API_URL)

# Define a bounding box and time range for the search
search_bbox = [77.5, 12.9, 77.7, 13.1]  # Example: A box over Bangalore
search_datetime = "2023-11-01/2023-11-30"  # Use an interval for STAC API

# Perform the search against your POST /search endpoint
search = catalog.search(
    collections=["sentinel-2-l2a"],  # Or your collection name
    bbox=search_bbox,
    datetime=search_datetime,
    method="POST"  # Ensure you specify POST
)

# Print the number of items found
print(f"Found {search.matched()} items")

# Print the details of the found items
for item in search.items():
    print(f" - Item ID: {item.id}, Date: {item.datetime.date()}")
