from django.urls import path
from .views import *

urlpatterns = [
    path('create/', group_create, name='group_create'),
    path('update/<int:id>', group_update, name='group_update'),
    path('delete/', group_delete, name='group_delete'),
    path('add_user/<str:name>/', add_user_group, name='add_user_group'),
    path('remove_user/<str:name>', remove_user_group, name='remove_user_group')
]
