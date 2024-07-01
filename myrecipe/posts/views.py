from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, RecipeIngredient, Tag, Ingredient, Favorite, Follow, ShoppingList
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
import json


User = get_user_model()

# Create your views here.
def index(request):
    tags = request.GET.getlist('tags')
    post_list = Recipe.objects.order_by('-pub_date').all()
    if request.user.is_authenticated:
        favorite_recipes = post_list.filter(favorite__user=request.user)
        recipe_names = list(favorite_recipes.values_list('id', flat=True))
        shop_list_recipes = ShoppingList.objects.filter(user=request.user).values_list('recipe__id', flat=True)
        shop_list_recipes = list(shop_list_recipes)
    else: 
        recipe_names = []
        shop_list_recipes = []
    
    # shop_list_recipes = ShoppingList.objects.filter(user=request.user).values_list('recipe__id', flat=True)
    # shop_list_recipes = list(shop_list_recipes)

    if tags:
        for tag in tags:
            post_list = post_list.filter(tags__name=tag).distinct()
    all_tags = Tag.objects.all()
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        "page": page,
        "paginator": paginator,
        "all_tags": all_tags,
        'selected_tags': tags,
        "favorite_recipes": recipe_names,
        "shop_list_recipes": shop_list_recipes,
    }
    return render(request, "index.html", context)

def recipe_view(request, username, recipe_id):
    user_profile = get_object_or_404(User, username=username)
    #Выбранный пост автора
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = recipe.get_ingredients()
    # Определяем, может ли текущий пользователь редактировать профиль
    edit = request.user.is_authenticated and request.user == user_profile
    if request.user.is_authenticated:
        shop_list_recipes = ShoppingList.objects.filter(user=request.user).values_list('recipe__id', flat=True)
        shop_list_recipes = list(shop_list_recipes)
    else:
        shop_list_recipes = []
    context = {
        "recipe": recipe,
        "user_profile": user_profile,
        "edit": edit,
        "ingredients": ingredients,
        "shop_list_recipes": shop_list_recipes,
    }
    return render(request, "recipe_item.html", context)


@login_required
def new_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)  # Не сохраняем сразу
            recipe.author = request.user  # Устанавливаем автора
            recipe.save()  # Теперь сохраняем

            # Получаем список ID тегов из формы
            tag_ids = request.POST.getlist('tags')  # ['1', '2']

            # Добавляем теги к рецепту
            for tag_id in tag_ids:
                tag = Tag.objects.get(pk=tag_id)
                recipe.tags.add(tag)

            # Получение данных об ингредиентах
            ingredient_keys = [key for key in request.POST if key.startswith('nameIngredient_')]
            ingredients = []
            quantities = []
            units = []

            for key in ingredient_keys:
                index = key.split('_')[1]
                ingredients.append(request.POST.get(f'nameIngredient_{index}'))
                quantities.append(request.POST.get(f'valueIngredient_{index}'))
                units.append(request.POST.get(f'unitsIngredient_{index}'))

            # Создание объектов RecipeIngredient
            for i in range(len(ingredients)):
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=Ingredient.objects.get(name=ingredients[i]),
                    quantity=quantities[i],
                )
            return redirect('index') 
        else:
            for field in form:
                print(f'Поле: {field.name}, значение: {field.value()}, ошибки: {field.errors}')
    else:
        form = RecipeForm()
    shop_list_recipes = ShoppingList.objects.filter(user=request.user).values_list('recipe__id', flat=True)
    context = {
        'form': form,
        'edit': False,
        "shop_list_recipes": shop_list_recipes,
    }
    return render(request, 'formRecipe.html', context)


def ingredients(request):
    query = request.GET.get('query')
    ingredients = Ingredient.objects.filter(name__istartswith=query)
    listy =[]
    for ingredient in ingredients:
        dicty={}
        dicty['title'] = ingredient.name
        dicty['dimension'] = ingredient.dimension
        listy.append(dicty)
    return JsonResponse(listy, safe=False)

def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    # Получаем список постов пользователя
    recipe_list = Recipe.objects.filter(author=user_profile).order_by('-pub_date').all()
    # Определяем, может ли текущий пользователь редактировать профиль
    edit = request.user.is_authenticated and request.user == user_profile

    if request.user.is_authenticated:
        favorite_recipes = recipe_list.filter(favorite__user=request.user)
        recipe_names = list(favorite_recipes.values_list('id', flat=True))
        shop_list_recipes = ShoppingList.objects.filter(user=request.user)
        subscriptions = Follow.objects.filter(user=request.user).values_list('author', flat=True)
        if user_profile.id in subscriptions:
            subscription = True
        else:
            subscription = False
    else: 
        recipe_names = []
        shop_list_recipes = []
        subscription = False

    tags = request.GET.getlist('tags')
    if tags:
        for tag in tags:
            recipe_list = recipe_list.filter(tags__name=tag).distinct()
    all_tags = Tag.objects.all()

    # Пагинация
    paginator = Paginator(recipe_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    context = {
        "page": page,
        "paginator": paginator,
        "edit": edit,
        "user_profile": user_profile,  # Переименовал переменную для ясности
        "all_tags": all_tags,
        "selected_tags": tags,
        "subscription": subscription,
        "favorite_recipes": recipe_names,
        "shop_list_recipes": shop_list_recipes,
    }
    return render(request, 'profile.html', context)

@login_required
def recipe_edit(request, username, recipe_id):
    profile = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=profile)
    ingredients = recipe.get_ingredients()
    if request.user != profile:
        return redirect('profile', username=username)
    if request.method == 'POST':
        if request.POST.get('action') == 'save':
            form = RecipeForm(request.POST, request.FILES, instance=recipe)
            if form.is_valid():
                form.save()
                # Удаляем все старые ингредиенты рецепта
                RecipeIngredient.objects.filter(recipe=recipe).delete()
                # Получение данных об ингредиентах
                ingredient_keys = [key for key in request.POST if key.startswith('nameIngredient_')]
                ingredients = []
                quantities = []
                units = []
                for key in ingredient_keys:
                    index = key.split('_')[1]
                    ingredients.append(request.POST.get(f'nameIngredient_{index}'))
                    quantities.append(request.POST.get(f'valueIngredient_{index}'))
                    units.append(request.POST.get(f'unitsIngredient_{index}'))
                # Создание объектов RecipeIngredient
                for i in range(len(ingredients)):
                    RecipeIngredient.objects.create(
                        recipe=recipe,
                        ingredient=Ingredient.objects.get(name=ingredients[i]),
                        quantity=quantities[i],
                    )
                return redirect('recipe', username=username, recipe_id=recipe.id)
        elif request.POST.get('action') == 'delete':
            recipe.delete()
            return redirect('profile', username=username)
    else:
        form = RecipeForm(instance=recipe)
    
    shop_list_recipes = ShoppingList.objects.filter(user=request.user).values_list('recipe__id', flat=True)
    context = {
        "form": form,
        "recipe": recipe,
        "edit": True,
        "ingredients": ingredients,
        "shop_list_recipes": shop_list_recipes,
    }
    return render(request, "formRecipe.html", context)

@login_required
@require_http_methods(["POST"])
def add_favorite(request, recipe_id):
    recipe_id = json.loads(request.body).get('id')
    if not recipe_id:
        return HttpResponseBadRequest("Missing recipe ID")

    recipe = get_object_or_404(Recipe, id=recipe_id)
    Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    return JsonResponse({'success': True})

@require_http_methods(["DELETE"])
def remove_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorite = get_object_or_404(Favorite, user=request.user, recipe=recipe)
    favorite.delete()
    return JsonResponse({'success': True})

# Create your views here.
def favorite(request):
    user = request.user
    post_list = Recipe.objects.order_by('-pub_date').all()
    favorite_recipes = post_list.filter(favorite__user=user)

    if request.user.is_authenticated:
        recipe_names = list(favorite_recipes.values_list('id', flat=True))
    else: 
        recipe_names = []
    shop_list_recipes = ShoppingList.objects.filter(user=request.user).values_list('recipe__id', flat=True)
    shop_list_recipes = list(shop_list_recipes)

    tags = request.GET.getlist('tags')
    if tags:
        for tag in tags:
            favorite_recipes = favorite_recipes.filter(tags__name=tag).distinct()
    all_tags = Tag.objects.all()
    paginator = Paginator(favorite_recipes, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator,
        "all_tags": all_tags,
        'selected_tags': tags,
        "favorite_recipes": recipe_names,
        "shop_list_recipes": shop_list_recipes,
    }
    return render(request, "favorite.html", context)

@login_required
@require_http_methods(["POST"])
def subscribe(request, author_id):
    # author_id = json.loads(request.body).get('id')
    author = get_object_or_404(User, id=author_id)
    Follow.objects.get_or_create(user=request.user, author=author)
    return JsonResponse({'success': True})

@login_required
@require_http_methods(["DELETE"])
def unsubscribe(request, author_id):
    author = get_object_or_404(User, id=author_id)
    Follow.objects.filter(user=request.user, author=author).delete()
    return JsonResponse({'success': True})

@login_required
def subscriptions(request):
    #Вывод постов, на которые подписан пользователь
    # Получаю подписки
    subscriptions = Follow.objects.filter(user=request.user)

    # # Получаем посты этих авторов
    paginator = Paginator(subscriptions, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    shop_list_recipes = ShoppingList.objects.filter(user=request.user).values_list('recipe__id', flat=True)
    context = {
        "page": page,
        "paginator": paginator,
        "shop_list_recipes": shop_list_recipes,
    }
    return render(request, "follow.html", context)

@require_http_methods(["POST"])
def add_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ShoppingList.objects.get_or_create(user=request.user, recipe=recipe)
    return JsonResponse({'success': True})

@require_http_methods(["DELETE"])
def remove_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ShoppingList.objects.filter(user=request.user, recipe=recipe).delete()
    return JsonResponse({'success': True})

def shopping_list(request):
    if request.user.is_authenticated:
        shop_list_recipes = ShoppingList.objects.filter(user=request.user)
        context = {
            "recipes": shop_list_recipes,
        }
        return render(request, "shop_list.html", context)
    else:
        # Обработка случая, когда пользователь не авторизован
        # Например, перенаправление на страницу входа
        return redirect('login')

def remove_from_shop_list(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ShoppingList.objects.filter(user=request.user, recipe=recipe).delete()
    return redirect(request.META.get('HTTP_REFERER', 'shop_list'))

def add_to_shop_list(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ShoppingList.objects.get_or_create(user=request.user, recipe=recipe)
    return redirect(request.META.get('HTTP_REFERER', 'shop_list'))
    


