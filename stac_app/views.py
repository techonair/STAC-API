from sqlalchemy.orm import Session
from fastapi import Query
from db.database import get_db
from utils.stac_utils import generate_stac_response, stac_geojson_response
from db.models import STACItem
from fastapi import Depends, HTTPException
from geoalchemy2.shape import from_shape
from shapely.geometry import box

def search_items(
    bbox: str = Query(..., description="Comma-separated bbox: minLon,minLat,maxLon,maxLat"),
    datetime: str = Query(...),
    db: Session = Depends(get_db)
):
    try:
        bbox_list = [float(x) for x in bbox.split(',')]
        datetime_start, datetime_end = datetime.split('/')
        # Convert bbox_list to a Shapely box and then to WKT for PostGIS
        shapely_box = box(*bbox_list)
        bbox_geom = from_shape(shapely_box, srid=4326)
        items = db.query(STACItem).filter(
            STACItem.bbox.intersects(bbox_geom),
            STACItem.datetime.between(datetime_start, datetime_end)
        ).all()
        if not items:
            raise HTTPException(status_code=404, detail="No items found")
        return stac_geojson_response(generate_stac_response(items))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))