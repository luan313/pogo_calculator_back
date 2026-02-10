import logging
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

def get_rank(pokemon: str, atk: int, df: int, hp: int, league: int):
    # Log de entrada para verificar se os parâmetros chegam corretos
    logger.info(f"🔍 Iniciando scraping de IV para {pokemon} ({atk}/{df}/{hp}) na liga {league}")
    
    with sync_playwright() as p:
        try:
            # Lançamento do browser
            logger.debug("Tentando abrir Chromium headless...")
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            url = f"https://pvpivs.com/?mon={pokemon}&cp={league}&IVs={atk}_{df}_{hp}"
            logger.info(f"🔗 Acessando URL: {url}")
            
            # Timeout de navegação
            page.goto(url, timeout=15000)
            logger.debug("Página carregada. Aguardando tabela de resultados...")

            # Verifica se o seletor existe antes de capturar
            page.wait_for_selector("#resultsTable", timeout=10000)
            
            # Captura o texto bruto
            rank_text = page.locator("#resultsTable tbody tr:first-child td:first-child").inner_text()
            logger.info(f"📝 Texto bruto capturado do rank: '{rank_text}'")
            
            if not rank_text:
                logger.warning("A tabela foi encontrada, mas o campo de rank estava vazio.")
                return None

            rank_limpo = rank_text.replace('#', '').strip()
            resultado = int(rank_limpo)
            
            logger.info(f"✅ Rank processado com sucesso: {resultado}")
            return resultado

        except Exception as e:
            # Captura erros de timeout ou seletores que mudaram
            logger.error(f"❌ Falha no scraping para {pokemon}: {str(e)}")
            return None
        finally:
            if 'browser' in locals():
                browser.close()
                logger.debug("Browser encerrado.")