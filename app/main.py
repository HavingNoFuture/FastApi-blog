from fastapi import FastAPI

from app.routes import user_router
from app.routes.auth import auth_router, pass_reset_router, register_router, verify_router
from app.routes.posts import posts_router
from app.urls import AUTH_URL

app = FastAPI()


app.include_router(register_router, prefix=AUTH_URL, tags=["auth"])
app.include_router(auth_router, prefix=AUTH_URL, tags=["auth"])
app.include_router(pass_reset_router, prefix=AUTH_URL, tags=["auth"])
app.include_router(verify_router, prefix=AUTH_URL, tags=["auth"])

app.include_router(user_router)

app.include_router(posts_router)
