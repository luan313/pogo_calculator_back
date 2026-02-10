from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# Supondo que você tenha seu cliente supabase instanciado em algum lugar
from app.utils.supabase_utils.connect import SupabaseConnection 

# Instancia o esquema de segurança
security = HTTPBearer()

async def get_current_user(auth: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependência que valida o token JWT do Supabase e retorna o objeto do usuário.
    """
    token = auth.credentials
    
    try:
        # O SDK do Supabase verifica se o token é válido e retorna o usuário atual
        res = SupabaseConnection.auth.get_user(token)
        
        if not res.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado ou token inválido",
            )
            
        return res.user # Retorna o objeto completo do usuário (id, email, etc)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Sessão inválida: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )