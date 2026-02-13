import re
import logging
from app.utils.supabase_utils.connect import SupabaseConnection
# Certifique-se que o caminho da importação está correto conforme sua estrutura de pastas
from app.utils.pogo_iv_rank import get_rank 

# Configuração de Log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def sanitize_name(name):
    """
    Transforma 'Sirfetch'd Shadow' em 'sirfetchd_shadow'
    para bater com o speciesId do arquivo gamemaster.
    """
    if not name: return ""
    name = name.lower()
    name = name.replace("'", "").replace(".", "")
    name = name.replace(" ", "_")
    # Remove caracteres especiais mantendo apenas letras, números e underscore
    return re.sub(r'[^a-z0-9_]', '', name)

def process_iv_updates():
    logger.info("🚀 Iniciando cálculo e atualização de Ranks de IV...")

    try:
        # 1. Busca TODOS os pokémons do banco
        # Precisamos de Nome e IVs para calcular e identificar a linha
        response = SupabaseConnection.table("pokemons").select("nome, ataque_iv, defesa_iv, hp_iv").execute()
        
        if not response.data:
            logger.warning("Nenhum pokémon encontrado no banco de dados.")
            return

        total = len(response.data)
        logger.info(f"Encontrados {total} pokémons para processar.")

        for index, p in enumerate(response.data, start=1):
            name = p['nome']
            # Garante conversão para int, assumindo 0 se nulo
            atk = int(p.get('ataque_iv') or 0)
            df = int(p.get('defesa_iv') or 0)
            hp = int(p.get('hp_iv') or 0)

            # Prepara o ID para buscar no gamemaster (ex: "swampert_shadow")
            sid = sanitize_name(name)

            try:
                # 2. Calcula os Ranks Matemáticos (1 a 4096)
                # Passamos o speciesId limpo e os IVs
                rank_great = get_rank(sid, atk, df, hp, 1500)
                rank_ultra = get_rank(sid, atk, df, hp, 2500)
                rank_master = get_rank(sid, atk, df, hp, 10000) # Master League

                # 3. Atualiza no Banco usando Chave Composta (Nome + IVs)
                SupabaseConnection.table("pokemons").update({
                    "rank_iv_grande": rank_great,
                    "rank_iv_ultra": rank_ultra,
                    "rank_iv_mestra": rank_master # Opcional: bom para saber quando rodou
                }).eq("nome", name).eq("ataque_iv", atk).eq("defesa_iv", df).eq("hp_iv", hp).execute()

                logger.info(f"[{index}/{total}] ✅ {name} ({atk}/{df}/{hp}) atualizado: G#{rank_great} | U#{rank_ultra} | M#{rank_master}")

            except Exception as inner_e:
                logger.error(f"Erro ao processar {name} ({atk}/{df}/{hp}): {inner_e}")
                continue

    except Exception as e:
        logger.error(f"❌ Erro fatal na conexão ou busca: {e}")

if __name__ == "__main__":
    process_iv_updates()
    logger.info("✨ Processo de IVs concluído.")