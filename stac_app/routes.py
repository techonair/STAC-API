from fastapi import APIRouter, Query, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from stac_app import views
from db.database import get_db
from utils.stac_utils import generate_stac_response, stac_geojson_response
from db.models import STACItem
from geoalchemy2.shape import from_shape
from shapely.geometry import box
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/v1/stac")


class SearchRequest(BaseModel):
    bbox: List[float]
    datetime: str
    collections: Optional[List[str]] = None


@router.post("/search")
def search_items_post(
    search: SearchRequest = Body(...),
    db: Session = Depends(get_db),
):
    try:
        bbox_list = search.bbox
        datetime = search.datetime
        query = db.query(STACItem)
        if bbox_list:
            shapely_box = box(*bbox_list)
            bbox_geom = from_shape(shapely_box, srid=4326)
            query = query.filter(STACItem.bbox.intersects(bbox_geom))
        if datetime:
            if "/" in datetime:
                datetime_start, datetime_end = datetime.split("/")
            else:
                datetime_start = datetime_end = datetime
            query = query.filter(STACItem.datetime.between(datetime_start, datetime_end))
        items = query.all()
        if not items:
            raise HTTPException(status_code=404, detail="No items found")
        return stac_geojson_response(generate_stac_response(items))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
def search_items_get(
    bbox: str = Query(None, description="Comma-separated bbox: minLon,minLat,maxLon,maxLat"),
    datetime: str = Query(None),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(STACItem)
        if bbox:
            bbox_list = [float(x) for x in bbox.split(",")]
            shapely_box = box(*bbox_list)
            bbox_geom = from_shape(shapely_box, srid=4326)
            query = query.filter(STACItem.bbox.intersects(bbox_geom))
        if datetime:
            if "/" in datetime:
                datetime_start, datetime_end = datetime.split("/")
            else:
                datetime_start = datetime_end = datetime
            query = query.filter(STACItem.datetime.between(datetime_start, datetime_end))
        items = query.all()
        if not items:
            raise HTTPException(status_code=404, detail="No items found")
        return stac_geojson_response(generate_stac_response(items))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", include_in_schema=False)
def stac_root():
    return JSONResponse(
        content={
            "stac_version": "1.0.0",
            "type": "Catalog",
            "id": "local-stac-catalog",
            "description": "Local STAC API root catalog",
            "conformsTo": [
                "https://api.stacspec.org/v1.0.0-beta.4/item-search",
                "https://api.stacspec.org/v1.0.0-beta.4/core",
            ],
            "links": [
                {
                    "rel": "self",
                    "href": "http://localhost:8000/v1/stac/",
                    "type": "application/json",
                },
                {
                    "rel": "search",
                    "href": "http://localhost:8000/v1/stac/search",
                    "type": "application/geo+json",
                    "method": "POST",
                },
            ],
        },
        media_type="application/json",
    )