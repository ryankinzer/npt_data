# datasets.urls

# data/urls.py
from django.urls import path
from . import views

from .views import DatasetList, DatasetCreate, DatasetUpdate, delete_model, update_fields

app_name = 'datasets'

urlpatterns = [
    path('', DatasetList.as_view(), name='list_datasets'),
    path('datasets/create/', DatasetCreate.as_view(), name='create_dataset'),
    path('datasets/update/<int:pk>/', DatasetUpdate.as_view(), name='update_dataset'),
    path('datasets/delete-model/<int:pk>/', delete_model, name='delete_model'),
    path('datasets/model/<int:pk>/', update_fields, name='update_fields'),
]