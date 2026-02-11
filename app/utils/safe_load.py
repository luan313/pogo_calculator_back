import logging
import os

from app.utils.base_loader import carregar_base


logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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