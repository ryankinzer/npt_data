# data/urls.py
from django.urls import path
from . import views
from .views import MyModelCreateView, MyModelUpdateView, MyModelListView

urlpatterns = [
    # path('', views.home, name='home'),
    #path('login/', 'django.contrib.auth.views.login', name='login'),
    #path('logout/', 'django.contrib.auth.views.logout', name='logout'),

    path('create/', MyModelCreateView.as_view(), name='create_model'),
    path('update/<int:pk>/', MyModelUpdateView.as_view(), name='update_model'),
    path('', MyModelListView.as_view(), name='home'),
]