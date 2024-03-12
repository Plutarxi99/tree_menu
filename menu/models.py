import random

from django.db import models
from django.urls import reverse

from config import settings
from menu import services


class ItemMixin(models.Model):
    is_include = models.BooleanField(default=False, verbose_name='Вложен ли пункт меню')
    lvl_include = models.CharField(default=0, unique=True, verbose_name="Путь вложенности")
    lvl_in_tree = models.PositiveSmallIntegerField(default=0, verbose_name="Уровень вложенности")
    path_the_root = models.CharField(default=0, verbose_name="Путь к началу наследования меню")
    is_item_head = models.BooleanField(default=False, verbose_name='Является ли пункт меню заголовком')
    link = models.ForeignKey("Item", related_name='item_link', on_delete=models.SET_NULL, **settings.NULLABLE,
                             verbose_name='привязка к верхнему уровню меню')
    prev_item_lvl_in_tree = models.PositiveIntegerField(verbose_name="Предыдущий элемент меню по уровню вложеннсоти")

    def save(self, *args, **kwargs):
        # блок на проверку, если пункт меню ссылается на верхний уровень, иначе создаем верхние уровни меню
        try:
            # если существует ссылка на отцовский пункт меню
            if self.link.pk:
                # обновляем значение флага, является ли пункт меню родителем
                services.update_data_after_create(self.link.pk, True)
                # вложен ли в него меню
                self.is_include = True
                # блок на проверку, если поле меню, которое ссылается на отцовский пункт меню поменяли
                # и у него не осталость детей, то ставим флаг, что он не отец
                try:
                    parent_id = Item.objects.get(pk=self.pk).link_id
                    if self.link_id != parent_id:
                        items_parents = Item.objects.filter(link_id=parent_id).count()
                        if items_parents == 1:
                            services.update_data_after_create(parent_id, False)
                except:
                    pass
                # обновляем данные флага, является ли он отцом
                self.is_item_head = Item.objects.filter(link_id=self.pk).exists() if self.pk else False

                # получение пути до начала верхнего уровня меню на который ссылается
                lvl_tree_and_path = services.get_lvl_tree_and_path(self.link.pk)
                lit = lvl_tree_and_path["lvl_in_tree"]
                a = self.lvl_in_tree
                ptr = lvl_tree_and_path['path_the_root']
                # составляем новый путь и приводим к нужному ввиду
                new_path_the_root = '/'.join(map(str, ptr))
                # если новый путь поменяли, то он меняется автоматически
                if new_path_the_root != self.path_the_root or lit != self.lvl_in_tree:
                    self.lvl_in_tree = lit
                    self.path_the_root = new_path_the_root
                    # получаем связанные объекты, которые ссылаются на тот же родительский пункт меню
                    link_items_with_parent = Item.objects.filter(link=self.link)
                    # если такие объекты есть, то берем последнее значение для установки
                    # пути включения меню, иначе делаем новое значение этого поля
                    if link_items_with_parent:
                        item_link = link_items_with_parent.order_by('lvl_include').values_list('lvl_include').last()[0]
                        last_value = f"{item_link}"
                    else:
                        item_link = Item.objects.get(pk=self.link.pk).lvl_include
                        last_value = f"{item_link}.0"

                    # получаем путь следования и составления правильного меню с учетом их вложенности друг в друга
                    list_lvl_include = last_value.split('.')
                    # при добавлении пункта меню, прибавляется один
                    change_number = list_lvl_include[lit]
                    new_value = str(int(change_number) + 1)
                    list_lvl_include[lit] = new_value
                    lvl_include = '.'.join(list_lvl_include)
                    self.lvl_include = lvl_include
                self.prev_item_lvl_in_tree = Item.objects.filter(lvl_include__lt=self.lvl_include).last().lvl_in_tree
            else:
                pass

        except:
            # при создании нового объекта, ему присвоится 1, и это условие сохраняет это значение,
            # если попробовать пересохранить этот пункт в админ панель
            if self.lvl_include == '1':
                self.lvl_include = 1
                self.is_include = False
                self.is_item_head = Item.objects.filter(link_id=self.pk).exists()
                self.prev_item_lvl_in_tree = 0
            # если уже существует объекты, то идёт запись уникального индефикатор
            elif Item.objects.filter(is_include=False).exists():
                # если уже есть, то не перезаписываем уник индефикатор
                lvl_inc = self.lvl_include
                pk = self.pk
                if pk:
                    items_lvl_up = lvl_inc
                # иначе, считаем количество уже созданных пунктов верхних меню
                # и если есть уже в бд, такой индефикатор, то берем рандомно число и прибавляем к нему
                else:
                    head_menu_items = Item.objects.filter(is_include=False)
                    count_head = head_menu_items.count()
                    list_head_menu_items = list(map(int, head_menu_items.values_list('lvl_include', flat=True)))
                    count_head_random = count_head + random.randint(1, 100)
                    if count_head not in list_head_menu_items:
                        items_lvl_up = count_head
                    elif count_head_random not in list_head_menu_items:
                        items_lvl_up = count_head_random
                    else:
                        items_lvl_up = count_head_random

                self.lvl_include = items_lvl_up
                self.is_include = False
                self.is_item_head = Item.objects.filter(link_id=self.pk).exists()
                self.prev_item_lvl_in_tree = Item.objects.order_by('lvl_include').filter(
                    lvl_include__lt=self.lvl_include).last().lvl_in_tree
        super(ItemMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Item(ItemMixin):
    item = models.CharField(max_length=255, verbose_name="Пункт меню")
    menu = models.ForeignKey('Menu', on_delete=models.SET_NULL, related_name='items_menu',
                             verbose_name='пункты меню относящиеся к этому меню', **settings.NULLABLE)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug")

    def __str__(self):
        return self.item

    class Meta:
        verbose_name = "Настройка пункта меню"
        verbose_name_plural = "Настройка пунктов меню"
        ordering = ['lvl_include']


class Menu(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Названия меню")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
