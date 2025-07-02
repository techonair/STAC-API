from sqlalchemy.orm import Session
from typing import List
from stac_api.db.database import get_db
from stac_api.utils.stac_utils import create_stac_response
from stac_api.db.models import STACItem

def search_items(bbox: List[float], datetime: str, db: Session = Depends(get_db)):
    # Implement the logic to query the database based on bbox and datetime
    items = db.query(STACItem).filter(
        STACItem.geometry.intersects(bbox),  # Assuming geometry is a PostGIS field
        STACItem.datetime.between(datetime_start, datetime_end)  # Adjust datetime filtering as needed
    ).all()

    if not items:
        raise HTTPException(status_code=404, detail="No items found")

    return create_stac_response(items) 