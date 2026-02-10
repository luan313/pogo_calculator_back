from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class ResponseStatus(BaseModel):
    status: str
    message: str

class IV(BaseModel):
    ataque_iv: int
    defesa_iv: int
    hp_iv: int

class DataToStoreModel(BaseModel):
    user_id: UUID
    nome: str
    tipo: List[str]
    ataque_iv: int
    defesa_iv: int
    hp_iv: int
    rank_iv_grande: Optional[int] = None        
    rank_iv_ultra: Optional[int] = None      
    rank_iv_mestra: Optional[int] = None 
    rank_liga_grande: Optional[int] = None 
    rank_liga_ultra: Optional[int] = None 
    rank_liga_mestra: Optional[int] = None 

class PokemonInput(BaseModel):
    nome: str
    tipo: List[str]
    ivs: List[IV]

class PokemonSuggestion(BaseModel):
    name: str
    types: List[str]