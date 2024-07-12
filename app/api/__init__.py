from fastapi import APIRouter, Depends

from dependency import db


common_dependencies = [
    Depends(db_session),
]

api_router = APIRouter()