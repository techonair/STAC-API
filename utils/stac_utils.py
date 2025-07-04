import json
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from fastapi.responses import JSONResponse

def stac_geojson_response(data):
    return JSONResponse(content=data, media_type="application/geo+json")

def generate_stac_response(items):
    feature_collection = {
        "type": "FeatureCollection",
        "features": [],
        "bbox": None,
        "links": [],
        "numberMatched": len(items),
        "numberReturned": len(items)
    }

    all_coords = []
    for item in items:
        
        geometry = None
        bbox = None
        if item.bbox is not None:
            try:
                shapely_geom = to_shape(item.bbox)
                geometry = mapping(shapely_geom)
                bbox = list(shapely_geom.bounds)
                all_coords.extend(list(shapely_geom.exterior.coords))
            except Exception:
                geometry = None
                bbox = [None, None, None, None]
        
        assets = {}
        try:
            props = json.loads(item.properties) if item.properties else {}
            assets = props.get('assets', {})
        except Exception:
            assets = {}
        feature = {
            "type": "Feature",
            "id": item.id,
            "stac_version": "1.0.0",
            "properties": {
                "datetime": str(item.datetime),
                "collection": item.collection,
                "description": getattr(item, 'description', ''),
                
            },
            "geometry": geometry if geometry else {},
            "bbox": bbox if bbox else [None, None, None, None],
            "links": [],
            "assets": assets,
            "stac_extensions": [],
            "collection": item.collection
        }
        feature_collection['features'].append(feature)

    
    if all_coords:
        lons, lats = zip(*all_coords)
        feature_collection['bbox'] = [min(lons), min(lats), max(lons), max(lats)]
    else:
        feature_collection['bbox'] = [None, None, None, None]

    return feature_collection

def parse_bbox(bbox):
    if len(bbox) != 4:
        raise ValueError("Bounding box must contain exactly four values: [min_lon, min_lat, max_lon, max_lat]")
    return {
        "min_lon": bbox[0],
        "min_lat": bbox[1],
        "max_lon": bbox[2],
        "max_lat": bbox[3]
    }

def parse_datetime(datetime_str):
    from dateutil import parser
    return parser.isoparse(datetime_str)