# data/urls.py
from django.urls import path
from . import views
from .views import ActivityListView

app_name = 'data'

urlpatterns = [
    #path('dataset/', DatasetList.as_view(), name='list_dataset'),
    # path('create/', DatasetCreate.as_view(), name='create_dataset'),
    # path('update/<int:pk>/', DatasetUpdate.as_view(), name='update_dataset'),
    #path('delete-model/<int:pk>/', delete_model, name='delete_model'),


    #path('', DatasetList.as_view(), name = 'dataset_list'),
    #path('dataset/new/', views.dataset_new, name='dataset_new'),

    path('activities/', ActivityListView.as_view(), name='list_activities'),
    path('activity/new/', views.activity_new, name = 'create_activity'),
    path('acitivity/edit/<int:pk>/', views.activity_edit, name='update_activity'),

]