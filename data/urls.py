# data/urls.py
from django.urls import path
from . import views
from .views import DatasetList, DatasetCreate, ActivityListView

urlpatterns = [
    # path('', views.home, name='home'),
    #path('login/', 'django.contrib.auth.views.login', name='login'),
    #path('logout/', 'django.contrib.auth.views.logout', name='logout'),

    # path('create/', ParentCreateView.as_view(), name='create_model'),
    # path('update/<int:pk>/', ParentUpdateView.as_view(), name='update_model'),

    path('', DatasetList.as_view(), name = 'dataset_list'),
    path('dataset/new/', DatasetCreate.as_view(), name='dataset_new'),

    path('activities/', ActivityListView.as_view(), name='activity_list'),
    path('activity/new/', views.activity_new, name = 'activity_new'),
    path('acitivity/edit/<int:pk>/', views.activity_edit, name='activity_edit'),
]