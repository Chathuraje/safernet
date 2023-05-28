from fastapi import FastAPI
from .api.domain_validator.routes import router as domain_validator

app = FastAPI()
app.include_router(domain_validator)
