from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("ingredients/", views.ingredients, name='ingredients'),
    path('recipes/new/', views.new_recipe, name='new_recipe'),
    path('add-favorites/<int:recipe_id>/', views.add_favorite, name='add_favorite'),
    path('remove-favorites/<int:recipe_id>/', views.remove_favorite, name='remove_favorite'),
    path("subscriptions/", views.subscriptions, name="my_subscriptions"),
    path("follow/subscribe/<int:author_id>/", views.subscribe, name="subscribe"), 
    path("follow/unsubscribe/<int:author_id>/", views.unsubscribe, name="unsubscribe"),

    path('add_to_shopping_list/<int:recipe_id>/', views.add_to_shop_list, name='add_to_shop_list'),
    path('remove_from_shopping_list/<int:recipe_id>/', views.remove_from_shop_list, name='remove_from_shop_list'),
    path('shop_list/', views.shopping_list, name='shop_list'),
    path("add-recipe/<int:recipe_id>/", views.add_recipe, name="add_recipe"),
    path("remove-recipe/<int:recipe_id>/", views.remove_recipe, name="add_recipe"),

    path('<str:username>/<int:recipe_id>/edit/', views.recipe_edit, name='edit_recipe'),
    path('<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('favorite/', views.favorite, name='favorite'),
    path('<str:username>/', views.profile, name='profile'),
]