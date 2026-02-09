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
    rank_iv_grande: int        
    rank_iv_ultra: int       
    rank_iv_mestra: int
    rank_liga_grande: int
    rank_liga_ultra: int
    rank_liga_mestra: int

class PokemonInput(BaseModel):
    nome: str
    tipo: List[str]
    ivs: List[IV]