from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.env import get_settings
from schemas.channels import Channel
from settings import Settings
from utils.db import get_db
from utils.request import check_users_list

app = APIRouter()


@app.get("/")
def index():
    return {"message": "Hello World from channels"}


@app.post('/', response_model=list)
def check_users(channels: list[Channel], db: Session = Depends(get_db), settings: Settings = Depends(get_settings)):
    result = check_users_list(channels, db, settings)
    return result
