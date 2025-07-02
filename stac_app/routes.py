from fastapi import APIRouter

router = APIRouter("/v1/check")

router.post("/search")("search_items")