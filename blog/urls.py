
from django.urls import path
from blog import views
from .views import *

urlpatterns = [
    path('<str:name>/', post, name='post'),
    path('<str:name>/post/<int:pk>/', post_detail, name='post_detail'),
    path('<str:name>/<str:post_type>/new/', post_create, name='post_create'),
    path('<str:name>/<str:post_type>/<int:pk>/update', post_update, name='post_update'),    
    path('<str:name>/post/delete/', post_delete, name='post_delete'),   
    path('post/requests/', post_requests, name='post_requests'),
    path('post/<int:pk>/commentAdd/', comment_create, name='comment_create'),
    path('post/comment/update/', comment_update, name='comment_update'),
    path('post/comment/delete/', comment_delete, name='comment_delete'),
    path('post/choose/', post_option, name='post_option'),
]

