from django.urls import path
from .views import MyModelViewSet
from . import views

urlpatterns = [
    path('', views.index),
    # path('v1/')
]
