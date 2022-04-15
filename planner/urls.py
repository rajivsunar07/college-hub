from django.urls import path, include
from .views import *

urlpatterns = [
    path('plan/', plan, name='plan'),
    path('plan_create/', plan_create, name='plan_create'),
    path('plan_update/<int:id>', plan_update, name='plan_update'),
    path('plan_delete/<int:id>', plan_delete, name='plan_delete'),
    path('plan_complete/<int:id>', plan_complete, name='plan_complete'),
    path('delete_completed/', delete_completed, name='delete_completed'),
    path('delete_old/', delete_old, name='delete_old')
]