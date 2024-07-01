# Generated by Django 5.0.3 on 2024-06-25 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_tag_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(blank=True, through='posts.RecipeIngredient', to='posts.ingredient'),
        ),
    ]
