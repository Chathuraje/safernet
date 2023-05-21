from .predict.ai import predict_url
from fastapi import APIRouter


router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.get("/predict/{url}")
def predict(url: str):
    
    return predict_url(url)