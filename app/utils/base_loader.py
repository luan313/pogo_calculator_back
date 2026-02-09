import requests
import os
import json
import logging

# Configuração de log para monitorar o carregamento no Vercel
logger = logging.getLogger(__name__)

# Definimos o caminho da pasta 'data' relativo à raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")

def carregar_base(nome_arquivo, url_fallback):
    caminho = os.path.join(DATA_DIR, nome_arquivo)
    
    # 1. Tenta carregar o arquivo local (muito rápido)
    if os.path.exists(caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                logger.info(f"✅ Carregando {nome_arquivo} do disco local.")
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ Erro ao ler arquivo local {nome_arquivo}: {e}")

    # 2. Fallback: Se o arquivo não existir ou falhar, baixa da URL
    logger.warning(f"⚠️ {nome_arquivo} não encontrado em {caminho}. Baixando de {url_fallback}...")
    try:
        response = requests.get(url_fallback, timeout=10) # Timeout para não travar a API
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"🚨 Falha crítica ao baixar base de {url_fallback}: {e}")
        # Retorna um dicionário vazio para evitar erro de 'NoneType' no map do front
        return {}