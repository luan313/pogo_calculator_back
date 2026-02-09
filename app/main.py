import logging

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import store_data
from .api.routes import get_tier_list
from .api.routes import search
from .api.routes import remove_pokemon

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(name)s - %(message)s"
)

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
app.include_router(remove_pokemon.router)