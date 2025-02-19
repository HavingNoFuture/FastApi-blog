from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from app.config import settings
from app.urls import LOGIN_URL

bearer_transport = BearerTransport(tokenUrl=LOGIN_URL)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=settings.TOKEN_LIFETIME)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
