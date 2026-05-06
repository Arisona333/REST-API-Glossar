from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from ..dings import db
from ..pydanticmodel import pydanticmodel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

router = APIRouter(
    tags=["User"]
)
oauth2_schema = OAuth2PasswordBearer(tokenUrl = "login")

@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    if data.username == "test" and data.password == "test":
        access_token = jwt.encode({"user": data.username}, key = "secret")
        return {"access_token": access_token, "token_type": "bearer"}
    
    raise HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Benutzername/Passwort ist falsch",
        headers = {"www-Authenticate": "Bearer"},
    )

@router.get("/users/", response_model = List[pydanticmodel.User])
def read_users():
    return db.get_all_users()

@router.get("/users/{user_id}", response_model = pydanticmodel.User)
def read_user_by_id(user_id: int):
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code = 404, detail= "User nicht gefunden")
    return user 

@router.post("/users/", response_model = pydanticmodel.User)
def create_user_endpoint(data: pydanticmodel.UserCreate):
    return db.create_user(data.first_name, data.role)

@router.delete("/users/{user_id}", dependencies=[Depends(oauth2_schema)])
async def delete_user_endpoint(user_id: int):
    success = db.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User nicht gefunden")
    return {"message": f"User mit ID {user_id} wurde gelöscht"}

@router.put("/users/{user_id}", response_model=pydanticmodel.User)
def update_user(user_id: int, user: pydanticmodel.UserUpdate):
    existing_user = db.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User nicht gefunden")
    db.update_user(user_id, user.first_name, user.role)
    return db.get_user_by_id(user_id)