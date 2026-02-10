from .connect import SupabaseConnection

def get_pokemon_by_tier(league_rank_col, iv_rank_col, target_type, user_id):
    """
    Inputs:
    - league_rank_col: 'rank_liga_grande', 'rank_liga_ultra', etc.
    - iv_rank_col: 'rank_iv_grande', 'rank_iv_ultra', etc.
    - target_type: o tipo elemental (ex: 'water')
    """
    # 1. Busca todos os candidatos do tipo filtrado
    response = SupabaseConnection.table("pokemons") \
        .select("*") \
        .contains("tipo", [target_type]) \
        .eq("user_id", user_id) \
        .is_not(league_rank_col, "null") \
        .order(iv_rank_col, desc=False) \
        .execute()

    all_candidates = response.data
    
    # 2. Mantém apenas o exemplar único com MENOR IV (melhor rank de IV)
    unique_exemplars = {}
    for poke in all_candidates:
        nome = poke['nome'].lower().strip()
        # Como ordenamos por IV Rank, o primeiro de cada nome que aparecer é o melhor
        if nome not in unique_exemplars:
            unique_exemplars[nome] = poke
            
    # 3. Transforma de volta em lista e ordena pelo RANK DA LIGA (Meta Rank)
    final_list = list(unique_exemplars.values())
    final_list.sort(key=lambda x: x[league_rank_col] if x[league_rank_col] is not None else 9999)

    # 4. Retorna apenas os Top 6
    return final_list[:6]