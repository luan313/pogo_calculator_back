from fastapi import FastAPI, APIRouter

from .api.routes import store_data
from .api.routes import get_tier_list
from .api.routes import search

app = FastAPI()

app.include_router(store_data.router)
app.include_router(get_tier_list.router)
app.include_router(search.router)