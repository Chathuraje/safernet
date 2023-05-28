from fastapi import APIRouter
from .scripts import basic_scripts

router = APIRouter(
    tags=["Nmap Scanner"],
    prefix="/nmap_scanner",
)

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.get("/scan/{ip}")
def scan_ip(ip: str):
    
    return basic_scripts.scan_domain(ip)