from django.urls import path

from menu.apps import MenuConfig

app_name = MenuConfig.name

urlpatterns = [
    path(...)
]