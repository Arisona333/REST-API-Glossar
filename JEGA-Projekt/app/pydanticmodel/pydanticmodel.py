from pydantic import BaseModel, Field
from typing import Optional, List

class Begriff(BaseModel):
    id: int
    titel: str
    beschreibung: str
    kategorie_id: int | None = None
    erstellt_am: str
    aktualisiert_am: str

class BegriffCreate(BaseModel):
    titel: str
    beschreibung: str
    kategorie_id: int | None = None

class BegriffUpdate(BaseModel):
    titel: str | None = None
    beschreibung: str | None = None
    kategorie_id: int | None = None

class Kategorie(BaseModel):
    id: int
    name: str
    beschreibung: str

class KategorieCreate(Kategorie):
    pass


class KategorieUpdate(BaseModel):
    name: str | None = None
    beschreibung: str | None = None


class User(BaseModel):
    id: int
    first_name: str
    role: str
    
class UserCreate(BaseModel):
    first_name: str
    role: str 

class UserUpdate(BaseModel):
    first_name: str | None = None
    role: str | None = None

class BegriffHistory(BaseModel):
    id: int
    user_id: int
    begriff_id: int
    aktion: str
    datum: str

class BegriffHistoryCreate(BaseModel):
    user_id: int
    begriff_id: int
    aktion: str

