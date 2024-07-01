# recipes/management/commands/load_ingredients.py
import json
from django.core.management.base import BaseCommand
from posts.models import Ingredient

class Command(BaseCommand):
    help = 'Load ingredients from a JSON file'

    def handle(self, *args, **kwargs):
        with open('D:/All_web_projects/Cooking_blog/ingredients.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        for item in data:
            Ingredient.objects.create(
                name=item['title'],
                dimension=item['dimension']
            )
            self.stdout.write(self.style.SUCCESS(f"Successfully added ingredient '{item['title']}'"))