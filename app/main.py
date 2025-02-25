from fastapi import FastAPI
from sqladmin import Admin

from app.admin import CommentAdmin, PostAdmin, SubscriptionAdmin, UserAdmin
from app.db import engine
from app.routes import user_router
from app.routes.auth import auth_router, pass_reset_router, register_router, verify_router
from app.routes.comments import comments_router
from app.routes.posts import posts_router
from app.routes.subscriptions import subscriptions_router
from app.urls import AUTH_URL

app = FastAPI()


app.include_router(register_router, prefix=AUTH_URL, tags=["auth"])
app.include_router(auth_router, prefix=AUTH_URL, tags=["auth"])
app.include_router(pass_reset_router, prefix=AUTH_URL, tags=["auth"])
app.include_router(verify_router, prefix=AUTH_URL, tags=["auth"])

app.include_router(user_router)
app.include_router(subscriptions_router)

app.include_router(posts_router)
app.include_router(comments_router)


# region Admin

admin = Admin(app, engine)

admin.add_view(UserAdmin)
admin.add_view(SubscriptionAdmin)
admin.add_view(PostAdmin)
admin.add_view(CommentAdmin)

# endregion Admin
