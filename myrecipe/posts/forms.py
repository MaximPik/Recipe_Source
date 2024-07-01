from django.forms import ModelForm, HiddenInput
from .models import Recipe, Ingredient, Tag, RecipeIngredient
from django import forms

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'tags', 'ingredients', 'cooking_time', 'description', 'image']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            # 'ingredients': ,
        }
        labels = {
            'title': 'Название рецепта',
            'image': 'Загрузить фото',
            'description': 'Описание',
            'tags': 'Теги',
            'cooking_time': 'Время приготовления',
            'ingredients': 'Ингредиенты',
        }

class RecipeIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all(), label="Ингредиент")
    quantity = forms.IntegerField(label="Количество", min_value=1)
    class Meta:
        model = RecipeIngredient
        fields = ['recipe', 'ingredient', 'quantity']
        

class TagForm(ModelForm):
     class Meta:
        model = Tag
        fields = ['name',]
         