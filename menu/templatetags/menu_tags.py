from django.urls import reverse
from django.utils.safestring import mark_safe
from django import template

from menu.models import Item, Menu

register = template.Library()


@register.inclusion_tag('menu/drop_menu.html')
def draw_menu(main_menu):
    """
    Получение название меню и передача в его в шаблон
    """
    menu = Menu.objects.filter(name=main_menu)[0].items_menu.all()
    return {"menu": menu, "title": main_menu}


@register.inclusion_tag('menu/includes/control_item_menu.html')
def control_iter_menu(item):
    """
    Фукнция для обработки блоков if/elif/else для отображения древодвиного меню,
    без обращение к базе данных, только получение объектов из итератора в шаблоне
    """
    # блок записи html тегов для отображение древовидного меню
    open_html = "<ul><li><details><summary>%s</summary>" % item
    close_html = "</details></li></ul>"
    url_on_item = reverse('menu:item', args=(item.slug,))
    list_no_open = '<ul><li><a href="%s">%s</a></li></ul>' % (url_on_item, item)
    # получение разницы в уровне вложение в меню для закрытия тегов
    now_item_lvl_in_tree = item.lvl_in_tree
    diff_lvl_in_tree = item.prev_item_lvl_in_tree - now_item_lvl_in_tree

    if diff_lvl_in_tree < 0 and item.is_item_head:
        return {"open_html": mark_safe(open_html), "reverse": True}

    elif diff_lvl_in_tree < 0:
        return {"list_no_open": mark_safe(list_no_open), "reverse": True}

    elif diff_lvl_in_tree == 0 and item.is_item_head:
        return {"open_html": mark_safe(open_html), "reverse": True}

    elif diff_lvl_in_tree == 0:
        return {"list_no_open": mark_safe(list_no_open), "reverse": True}

    elif diff_lvl_in_tree > 0 and item.is_item_head:
        return {"open_html": mark_safe(open_html), "close_html": mark_safe(close_html * diff_lvl_in_tree)}

    elif 0 <= diff_lvl_in_tree <= 1:
        return {"list_no_open": mark_safe(list_no_open), "close_html": mark_safe(close_html)}

    elif diff_lvl_in_tree > 1:
        return {"list_no_open": mark_safe(list_no_open), "close_html": mark_safe(close_html * diff_lvl_in_tree)}
