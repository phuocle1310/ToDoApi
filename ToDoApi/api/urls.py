from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from .views import *


router = DefaultRouter()
router.register(r'api', views.ToDoView, basename="todo_api")

urlpatterns = [
    path('', include(router.urls)),
]