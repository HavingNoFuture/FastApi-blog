from fastapi import FastAPI

from app.routes import user_router
from app.routes.auth import auth_router, pass_reset_router, register_router, verify_router
from app.urls import API_URL, AUTH_URL

app = FastAPI()


app.include_router(register_router, prefix=AUTH_URL, tags=["auth"])
app.include_router(auth_router, prefix=AUTH_URL, tags=["auth"])
app.include_router(pass_reset_router, prefix=AUTH_URL, tags=["auth"])
app.include_router(verify_router, prefix=AUTH_URL, tags=["auth"])
app.include_router(user_router, prefix=API_URL, tags=["users"])
