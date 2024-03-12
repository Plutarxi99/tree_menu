from django.urls import path

from menu import views
from menu.apps import MenuConfig

app_name = MenuConfig.name

urlpatterns = [
    path('', views.MenuView.as_view(), name='menu_drop'),
    path('<slug:name_item>/', views.ShowItem.as_view(), name='item')
]