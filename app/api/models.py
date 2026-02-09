from pydantic import BaseModel
from typing import List

class ResponseStatus(BaseModel):
    status: str
    message: str

class IV(BaseModel):
    ataque_iv: int
    defesa_iv: int
    hp_iv: int

class DataToStoreModel(BaseModel):
    nome: str
    tipo: List[str]
    ataque_iv: int
    defesa_iv: int
    hp_iv: int
    rank_iv_grande: int | None = None        
    rank_iv_ultra: int | None = None       
    rank_iv_mestra: int | None = None
    rank_liga_grande: int | None = None
    rank_liga_ultra: int | None = None
    rank_liga_mestra: int | None = None

class PokemonInput(BaseModel):
    nome: str
    tipo: List[str]
    ivs: List[IV]