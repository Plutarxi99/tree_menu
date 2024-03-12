from django.contrib import admin
from django.utils.translation import ngettext
from menu import models
from django.contrib import messages


@admin.register(models.Item)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['item', 'link', 'is_include', 'lvl_include', 'is_item_head', ]
    readonly_fields = ['is_include', 'path_the_root', 'lvl_in_tree', 'lvl_include', 'is_item_head',
                       'prev_item_lvl_in_tree', ]
    actions = ['delete_model', 'refresh_db']
    prepopulated_fields = {"slug": ("item",)}

    @admin.action(description="Кнопка для удаления и авт обновление бд")
    def delete_model(self, request, obj):
        """
        Кнопка для удаления и обновления данных, после изменения в базе данных
        """
        obj.delete()
        for item in models.Item.objects.all():
            is_item_head = models.Item.objects.filter(link_id=item.pk).exists()
            if not is_item_head:
                item.is_item_head = False
                item.refresh_from_db()
                item.save()
            else:
                pass

    @admin.action(description="Обновление полей в бд")
    def refresh_db(self, request, queryset):
        """
        Кнопка активности для обнуление задолженности
        """
        refresh_db = queryset
        for i_db in refresh_db:
            i_db.save()


@admin.register(models.Menu)
class ItemMenu(admin.ModelAdmin):
    list_display = ['name', ]
