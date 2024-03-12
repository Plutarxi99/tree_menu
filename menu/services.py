from menu import models


def get_link_item(pk):
    """
    Получение индикатора на который ссылается объект
    """
    item_now = models.Item.objects.filter(pk=pk).first()
    if item_now.is_include:
        item_link_pk = item_now.link_id
        return {"item_link_pk": item_link_pk, "result": True}
    else:
        return {"result": False}


def get_lvl_tree_and_path(pk):
    """
    Получение уровня вложенности в меню и путь индефикаторов к началу меню
    """
    path_the_root = []
    iter_lvl = 1
    pk_item_link = models.Item.objects.filter(pk=pk).first().pk
    while True:
        path_the_root.insert(0, pk_item_link)
        dict_pk_item_link = get_link_item(pk_item_link)
        if dict_pk_item_link['result']:
            iter_lvl += 1
            pk_item_link = dict_pk_item_link['item_link_pk']
            continue
        else:
            break
    return {"lvl_in_tree": iter_lvl, "path_the_root": path_the_root}


def update_data_after_create(pk_link_item: int, flag: bool):
    """
    обновление флага, является ли меню отцом
    """
    if flag:
        models.Item.objects.filter(pk=pk_link_item).update(is_item_head=True)
    else:
        models.Item.objects.filter(pk=pk_link_item).update(is_item_head=False)
