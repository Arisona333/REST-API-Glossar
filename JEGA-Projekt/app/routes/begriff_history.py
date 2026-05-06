from fastapi import APIRouter, HTTPException
from ..dings import db
from ..pydanticmodel import pydanticmodel

router = APIRouter(
    prefix="/begriff-history",
    tags=["BegriffHistory"],
)

@router.get("/", response_model=list[pydanticmodel.BegriffHistory])
def get_all_history():
    return db.get_all_begriff_history()

@router.post("/", response_model=pydanticmodel.BegriffHistory)
def create_history(entry: pydanticmodel.BegriffHistoryCreate):
    return db.create_begriff_history(entry.user_id, entry.begriff_id, entry.aktion)
