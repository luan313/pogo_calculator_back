from playwright.sync_api import sync_playwright

def get_rank(pokemon: str, atk: int, df: int, hp: int, league: int):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = f"https://pvpivs.com/?mon={pokemon}&cp={league}&IVs={atk}_{df}_{hp}"
        
        page.goto(url)

        try:
            page.wait_for_selector("#resultsTable", timeout=10000)

            rank = page.locator("#resultsTable tbody tr:first-child td:first-child").inner_text()
            
            rank_limpo = rank.replace('#', '').strip()
            
            return int(rank_limpo)
        except Exception as e:
            print(f"Erro ao capturar o rank: {e}")
            return None
        finally:
            browser.close()