from fastapi import FastAPI
from api.domain_validator.routes import router as domain_validator
from api.nmap_scanner.routes import router as nmap_scanner

app = FastAPI()
app.include_router(domain_validator)
app.include_router(nmap_scanner)
