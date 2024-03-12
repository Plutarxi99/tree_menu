from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView

from menu.models import Menu, Item


class MenuView(TemplateView):
    model = Menu
    template_name = 'menu/index.html'
    context_object_name = 'main_menu'
    # Здесь вставлять меню для отображений нескольких меню
    extra_context = {
        'main_menu': 'test',
        'main_menu_2': 'test'
    }


class ShowItem(DetailView):
    template_name = 'menu/item.html'
    slug_url_kwarg = 'name_item'

    def get_object(self, queryset=None):
        slug_search = self.kwargs[self.slug_url_kwarg]
        return get_object_or_404(Item, slug=slug_search)
