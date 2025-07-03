-- Create the PostGIS extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create the STACItem table for STAC Items
CREATE TABLE STACItem (
    id VARCHAR PRIMARY KEY,
    datetime TIMESTAMP NOT NULL,
    bbox geometry(POLYGON, 4326) NOT NULL,
    collection VARCHAR NOT NULL,
    properties TEXT
);

-- Example: Insert a sample item (replace with your real data)
INSERT INTO STACItem (id, datetime, bbox, collection, properties)
VALUES (
    'item1',
    '2023-11-10T10:00:00Z',
    ST_GeomFromText('POLYGON((77.5 12.9, 77.7 12.9, 77.7 13.1, 77.5 13.1, 77.5 12.9))', 4326),
    'sentinel-2-l2a',
    '{"eo:cloud_cover": 10, "platform": "Sentinel-2A"}'
);
