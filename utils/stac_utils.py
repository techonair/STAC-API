def generate_stac_response(items):
    feature_collection = {
        "type": "FeatureCollection",
        "features": []
    }

    for item in items:
        feature = {
            "type": "Feature",
            "id": item['id'],
            "properties": {
                "datetime": item['datetime'],
                "collection": item['collection'],
                "description": item.get('description', ''),
            },
            "geometry": item['geometry'],
            "links": item.get('links', [])
        }
        feature_collection['features'].append(feature)

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