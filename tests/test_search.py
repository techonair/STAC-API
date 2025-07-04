from pystac_client import Client

API_URL = "http://localhost:8000/v1/stac/"

catalog = Client.open(API_URL)

search_bbox = [77.5, 12.9, 77.7, 13.1]
search_datetime = "2023-11-01/2023-11-30" 

search = catalog.search(
    collections=["sentinel-2-l2a"],
    bbox=search_bbox,
    datetime=search_datetime,
    method="POST"
)


print(f"Found {search.matched()} items")

for item in search.items():
    print(f" - Item ID: {item.id}, Date: {item.datetime.date()}")
