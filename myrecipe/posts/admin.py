from django.contrib import admin
# из файла models импортируем модель Post
from .models import Recipe, Ingredient, RecipeIngredient, Tag, Favorite, Follow, ShoppingList


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ("pk", "author", "title", "cooking_time")
    inlines = [RecipeIngredientInline]
    search_fields = ("title", "description")
    list_filter = ("tags", "author")
    filter_horizontal = ("tags",)

admin.site.register(Recipe, RecipeAdmin)

class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "dimension")
    search_fields = ("name",)

admin.site.register(Ingredient, IngredientAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color",)
    search_fields = ("name",)

admin.site.register(Tag, TagAdmin)

class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "quantity")

admin.site.register(RecipeIngredient, RecipeIngredientAdmin)

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")

admin.site.register(Favorite, FavoriteAdmin)

class FollowAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "author")

admin.site.register(Follow, FollowAdmin)

class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")

admin.site.register(ShoppingList, ShoppingListAdmin)

