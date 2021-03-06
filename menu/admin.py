from django.contrib import admin
from . models import FoodMenu


@admin.register(FoodMenu)
class MenuAdmin(admin.ModelAdmin):
    """
    Registering the FoodMenu database in the admin panel.
    Setting list display and filter items
    """

    list_filter = ('title', 'course')
    list_display = ('title', 'course')
    search_fields = ['course']
