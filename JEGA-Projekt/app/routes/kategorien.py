from fastapi import FastAPI, HTTPException, APIRouter, Depends
from ..dings import db
from ..pydanticmodel import pydanticmodel
from typing import List
from ..routes.users import oauth2_schema


router = APIRouter(
    tags=["kategorien"],
)

@router.get("/kategorie/", response_model = List[pydanticmodel.Kategorie])
def read_kategorien():
    return db.get_all_kategorien()

@router.get("/kategorien/{kategorie_id}", response_model = pydanticmodel.Kategorie)
def read_kategorie(kategorie_id: int):
    querry = db.get_kategorien_by_id(kategorie_id)
    if not querry:
        raise HTTPException(status_code = 404, detail = "Kategorie nicht gefunden")
    return querry

@router.post("/kategorien/", response_model = pydanticmodel.Kategorie)
def create_category_endpoint(data: pydanticmodel.KategorieCreate):
    return db.create_kategorie(data.name, data.beschreibung)

@router.put("/kategorien/{kategorie_id}", response_model=pydanticmodel.Kategorie)
def update_kategorie(kategorie_id: int, kategorien: pydanticmodel.KategorieUpdate):
    existing_kategorien = db.get_kategorien_by_id(kategorie_id)
    if not existing_kategorien:
        raise HTTPException(status_code=404, detail="kategorien not found")
    db.update_kategorie(kategorie_id, kategorien.name, kategorien.beschreibung)
    return db.get_kategorien_by_id(kategorie_id)

@router.delete("/kategorien/{kategorie_id}", dependencies=[Depends(oauth2_schema)])
def delete_kategorie(kategorie_id: int):
    success = db.delete_kategorie(kategorie_id)
    if not success:
        raise HTTPException(status_code=404, detail="Kategorie nicht gefunden")
    return {"message": f"Kategorie mit ID {kategorie_id} wurde gelöscht"}

@router.get("/kategorie/{kategorie_id}", response_model=list[pydanticmodel.Begriff])
def get_begriffe_by_kategorie(kategorie_id: int):
    return db.get_begriffe_by_kategorie(kategorie_id)