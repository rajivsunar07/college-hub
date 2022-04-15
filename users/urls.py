from django.urls import path
from .views import *

urlpatterns = [
    path('user_create', user_create, name='user_create'),
    path('delete/', user_delete, name='user_delete'),
    path('update/<int:id>/', user_update, name='user_update'),
    path('password_change/', password_change, name='password_change'),
    path('recent_posts/<str:name>/', recent_posts, name='recent_posts'),
    path('recent_logins/<str:name>/', recent_logins, name='recent_logins'),
]
