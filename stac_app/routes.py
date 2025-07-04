from fastapi import APIRouter
from stac_app import views

router = APIRouter(prefix="/v1/stac")

router.post("/search")(views.search_items)