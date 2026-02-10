from fastapi import APIRouter, HTTPException
from ..models import DataToStoreModel, PokemonInput, ResponseStatus

from ...services.rank_fetcher import great_fetcher, ultra_fetcher, master_fetcher
from ...utils.supabase_utils.insert import insert_pokemon
from ...utils.base_loader import carregar_base

import os
import logging

from ...config import URL_GREAT, URL_ULTRA, URL_MASTER

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def safe_load(nome_arquivo, url_fallback):
    path = os.path.join(BASE_DIR, "data", nome_arquivo)
    
    # 1. Tenta carregar do disco (Prioridade Máxima)
    if os.path.exists(path):
        try:
            return carregar_base(path, url_fallback)
        except Exception as e:
            logger.error(f"Erro ao ler {nome_arquivo}: {e}")

    # 2. Fallback: Baixa da URL para o site não ficar offline
    logger.warning(f"Arquivo {nome_arquivo} não encontrado. Usando fallback via URL.")
    try:
        import requests
        return requests.get(url_fallback).json()
    except Exception as e:
        logger.error(f"Falha total ao carregar {nome_arquivo}: {e}")
        return {} # Retorna dicionário vazio para evitar erro de tipo

# Carregamento robusto
BASE_GREAT = safe_load("base_great.json", URL_GREAT)
BASE_ULTRA = safe_load("base_ultra.json", URL_ULTRA)
BASE_MASTER = safe_load("base_master.json", URL_MASTER)

router = APIRouter()

@router.post("/store_data", response_model=ResponseStatus)
def store_data(payload: PokemonInput):
    try:
        name = payload.nome
        typep = payload.tipo

        contador = 0

        if not name or not typep:
            raise HTTPException(status_code=400, detail="Nome e tipo são obrigatórios.")
        
        for each in payload.ivs:
            output = DataToStoreModel(
                nome=name,
                tipo=typep,
                ataque_iv = each.ataque_iv,
                defesa_iv = each.defesa_iv,
                hp_iv = each.hp_iv
            )
            
            great_fetcher(BASE_GREAT, output)
            ultra_fetcher(BASE_ULTRA, output)
            master_fetcher(BASE_MASTER, output)
        
            insert_pokemon(output)
            contador += 1

        return ResponseStatus(
            status="SUCCESS",
            message=f"Foram adicionados {contador} Pokémon."
        )

    except Exception as e:
        logger.error(f"Erro ao salvar: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")