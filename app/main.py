from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import store_data
from .api.routes import get_tier_list
from .api.routes import search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://pogo-calculator-front.vercel.app"], # Permite o seu frontend
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"], # Permite todos os headers
)

app.include_router(store_data.router)
app.include_router(get_tier_list.router)
app.include_router(search.router)