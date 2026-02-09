from fastapi import FastAPI, APIRouter

from .api.routes.store_data import store_data
from .api.routes.get_tier_list import get_tier_list
from .api.routes.search import autocomplete

app = FastAPI()

app.include_router(store_data.router)
app.include_router(get_tier_list.router)
app.include_router(autocomplete.router)