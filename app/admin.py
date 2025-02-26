from sqladmin import ModelView

from app.models import Comment, Post, Rating, Subscription, User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]


class SubscriptionAdmin(ModelView, model=Subscription):
    column_list = [Subscription.id, Subscription.user_id, Subscription.author_id]


class PostAdmin(ModelView, model=Post):
    column_list = [Post.id, Post.author_id]


class CommentAdmin(ModelView, model=Comment):
    column_list = [Comment.id, Comment.author_id]


class RatingAdmin(ModelView, model=Rating):
    column_list = [Rating.id, Rating.score, Rating.post_id, Rating.user_id]
