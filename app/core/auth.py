from datetime import datetime, timedelta, timezone
import jwt
from app.core.configs import settings

def criar_token_acesso(dados: dict) -> str:
    dados_token = dados.copy()
    expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    dados_token.update({"exp": expiracao})
    token = jwt.encode(
        dados_token,
        settings.JWT_SECRET,
        algorithm=settings.ALGORITHM
    )

    return token

def decodificar_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.ALGORITHM]
    )