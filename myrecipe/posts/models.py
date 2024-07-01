from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() 

class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True)
    dimension = models.CharField(max_length=50) # единица измерения
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=10, unique=True)
    color = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.name
        
class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='posts/media/')
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', blank=True)
    tags = models.ManyToManyField(Tag)
    #tags = models.CharField(max_length=50, choices=TAG_CHOISES)
    cooking_time = models.PositiveIntegerField()
    pub_date = models.DateTimeField("date published", auto_now_add = True)
    def __str__(self):
        return self.title
    def get_ingredients(self):
        return self.recipeingredient_set.all()

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.quantity} {self.ingredient.dimension} of {self.ingredient.name} in {self.recipe.title}"
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'recipe')

class Follow(models.Model):
    # ПОДПИСКИ. Это поле создаёт связь с моделью пользователя, указывая, кто подписывается.
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    # ПОДПИСЧИКИ. Это поле создаёт связь с моделью пользователя, указывая, на кого подписываются.
    author = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'author')
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='prevent_self_follow',
            ),
        ]

    def __str__(self):
        return f'{self.user} follows {self.author}'
    
class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'recipe')