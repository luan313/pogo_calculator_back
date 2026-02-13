import json
import os
import logging
import math

logger = logging.getLogger(__name__)

# Caminho para os dados
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        logger.error(f"Arquivo {filename} não encontrado em {path}")
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_rank(pokemon_id: str, atk: int, df: int, hp: int, league: int):
    logger.info(f"📊 Calculando Rank IV (Matemático) para {pokemon_id} ({atk}/{df}/{hp}) na liga {league}")

    # 1. Carrega os dados necessários
    gm = load_json("gamemaster.json")
    cpm_data = load_json("cpm.json")

    if not gm or not cpm_data:
        return None

    cpms = cpm_data.get("cpms", [])
    
    # 2. Busca os Stats Base do Pokémon
    pokemon_stats = next((p for p in gm.get("pokemon", []) if p.get("speciesId") == pokemon_id.lower()), None)

    if not pokemon_stats:
        logger.warning(f"Pokémon {pokemon_id} não encontrado no gamemaster.")
        return None

    base_stats = pokemon_stats.get("baseStats")
    b_atk, b_def, b_hp = base_stats["atk"], base_stats["def"], base_stats["hp"]

    # --- INÍCIO DA CORREÇÃO ---
    def get_stat_product(a, d, h, limit):
        best_sp = 0
        
        # Lógica especial para Master League (Sem limite de CP)
        if limit <= 0 or limit >= 10000:
            final_cpm = cpms[-1] # Nível 50
            
            # Na Master, usamos o HP arredondado (floor)
            hp_final = math.floor((b_hp + h) * final_cpm)
            if hp_final < 10: hp_final = 10
            
            # Retorna o Stat Product direto
            return (b_atk + a) * final_cpm * (b_def + d) * final_cpm * hp_final

        # Simula do nível 1 ao 50 (usando a tabela de CPM)
        for cpm in cpms:
            # 1. Calcula os atributos "brutos"
            cur_atk = (b_atk + a) * cpm
            cur_def = (b_def + d) * cpm
            
            # CORREÇÃO CRÍTICA: O HP é arredondado para baixo ANTES de calcular o CP
            cur_hp = math.floor((b_hp + h) * cpm)
            if cur_hp < 10: cur_hp = 10

            # 2. Fórmula oficial de CP: Floor( (Atk * Def^0.5 * HP_INTEIRO^0.5) / 10 )
            cp = math.floor((cur_atk * math.sqrt(cur_def) * math.sqrt(cur_hp)) / 10)
            
            if cp <= limit:
                # O Stat Product usa o HP arredondado
                product = cur_atk * cur_def * cur_hp
                if product > best_sp:
                    best_sp = product
            else:
                # Passou do limite da liga (ex: 2501 CP), para de verificar níveis mais altos
                break
                
        return best_sp
    # --- FIM DA CORREÇÃO ---

    # 3. Calcula o Stat Product do Pokémon do usuário
    user_sp = get_stat_product(atk, df, hp, league)

    # 4. Gera todas as 4096 combinações de IVs possíveis (0-15)
    all_products = []
    for i_a in range(16):
        for i_d in range(16):
            for i_h in range(16):
                all_products.append(get_stat_product(i_a, i_d, i_h, league))

    # 5. Ordena do maior Stat Product para o menor (Rank 1 é o maior SP)
    all_products.sort(reverse=True)
    
    try:
        # O Rank é a posição na lista + 1 (porque lista começa no índice 0)
        # index() retorna a primeira aparição do valor (resolve empates corretamente dando o melhor rank)
        rank = all_products.index(user_sp) + 1
        logger.info(f"✅ Rank {rank} calculado localmente para {pokemon_id}")
        return rank
    except ValueError:
        logger.error("Erro ao localizar o produto de atributos na lista gerada.")
        return None