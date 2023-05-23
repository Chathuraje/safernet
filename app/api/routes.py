from .predict import ai
from .pihole import update_list
from fastapi import APIRouter
from enum import Enum

router = APIRouter(
    tags=["api"],
)

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.get("/predict/{url}")
def predict(url: str):
    
    return int(ai.predict_url(url))


class ListType(str, Enum):
    blacklist = "regex_black"
    whitelist = "regex_white"
    white = "white"
    black = "black"

@router.get("/add_domain/{list_type}/{url}")
def add_domain(url: str, list_type: ListType):
    
    return update_list.add_domain(url, list_type.value)


@router.get("/domains/{list_type}")
def view_list(list_type: ListType):
    
    return update_list.view_list(list_type.value)


@router.get("/domains/list")
def view_complete_list():
    
    return update_list.view_complete_list(list_type.value)