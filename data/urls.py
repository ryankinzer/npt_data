# data/urls.py
from django.urls import path
from . import views
from .views import ActivityListView

app_name = 'data'

urlpatterns = [

    path('activities/', ActivityListView.as_view(), name='list_activities'),
    path('activity/new/', views.activity_new, name = 'create_activity'),
    path('acitivity/edit/<int:pk>/', views.activity_edit, name='update_activity'),
    path('activities/<int:pk>', views.activity_view ,name='view_activities')

]