# datasets.urls

# data/urls.py
from django.urls import path
from . import views

from .views import home, DatasetList, DatasetCreate, DatasetUpdate, delete_model, update_fields, ProtocolList, ProtocolCreate, ProtocolUpdate, TaskList, TaskCreate, TaskUpdate

app_name = 'datasets'

urlpatterns = [
    path('',home,name='home'),
    path('datasets/', DatasetList.as_view(), name='list_datasets'),
    path('datasets/create/', DatasetCreate.as_view(), name='create_dataset'),
    path('datasets/update/<int:pk>/', DatasetUpdate.as_view(), name='update_dataset'),
    path('datasets/delete-model/<int:pk>/', delete_model, name='delete_model'),
    path('datasets/model/<int:pk>/', update_fields, name='update_fields'),

    path('protocols/', ProtocolList.as_view(), name='list_protocols'),
    path('protocols/create/', ProtocolCreate.as_view(), name='create_protocol'),
    path('protocols/update/<int:pk>/', ProtocolUpdate.as_view(), name='update_protocol'),

    path('tasks/', TaskList.as_view(), name='list_tasks'),
    path('tasks/create/', TaskCreate.as_view(), name='create_task'),
    path('tasks/update/<int:pk>/', TaskUpdate.as_view(), name='update_task'),
]