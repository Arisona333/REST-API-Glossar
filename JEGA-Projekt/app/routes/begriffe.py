from fastapi import APIRouter, HTTPException, Depends
from ..routes.users import oauth2_schema
from ..dings import db
from ..pydanticmodel import pydanticmodel

router = APIRouter(
    prefix="/begriffe",
    tags=["Begriffe"],
)

@router.get("/", response_model=list[pydanticmodel.Begriff])
def get_all_begriffe():
    return db.get_all_begriffe()

@router.get("/{begriff_id}", response_model=pydanticmodel.Begriff)
def get_begriff(begriff_id: int):
    begriff = db.get_begriff_by_id(begriff_id)
    if not begriff:
        raise HTTPException(status_code=404, detail="Begriff not found")
    return begriff

@router.post("/", response_model=pydanticmodel.Begriff)
def create_begriff(begriff: pydanticmodel.BegriffCreate):
    return db.create_begriff_full(begriff.titel, begriff.beschreibung, begriff.kategorie_id)

@router.put("/{begriff_id}", response_model=pydanticmodel.Begriff)
def update_begriff(begriff_id: int, begriff: pydanticmodel.BegriffUpdate):
    existing_begriff = db.get_begriff_by_id(begriff_id)
    if not existing_begriff:
        raise HTTPException(status_code=404, detail="Begriff wurde nicht gefunden")
    db.update_begriff(begriff_id, begriff.titel, begriff.beschreibung, begriff.kategorie_id)
    return db.get_begriff_by_id(begriff_id)

@router.delete("/{begriff_id}", dependencies=[Depends(oauth2_schema)])
def delete_begriff(begriff_id: int):
    success = db.delete_begriff(begriff_id)
    if not success:
        raise HTTPException(status_code=404, detail="Begriff wurde nicht gefunden")
    return {"message": f"Begriff mit ID {begriff_id} wurde gelöscht"}