from django.db import models
from datetime import datetime
# Create your models here.

class recipecategory(models.Model):

    recipe_category = models.CharField(max_length=200)
    category_summary = models.CharField(max_length=200)
    category_slug = models.CharField(max_length=200, default=1)

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.recipe_category

class recipeseries(models.Model):
    recipe_series = models.CharField(max_length=200)

    recipe_category = models.ForeignKey(recipecategory, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)
    series_summary = models.CharField(max_length=200)

    class Meta:
        # otherwise we get "recipe Seriess in admin"
        verbose_name_plural = "Series"

    def __str__(self):
        return self.recipe_series



class Recipe(models.Model):
    recipe_title = models.CharField(max_length=200)
    recipe_content = models.TextField()
    recipe_published = models.DateTimeField('date published')
    #https://docs.djangoproject.com/en/2.1/ref/models/fields/#django.db.models.ForeignKey.on_delete
    recipe_series = models.ForeignKey(recipeseries, default=1, verbose_name="Series", on_delete=models.SET_DEFAULT)
    recipe_slug = models.CharField(max_length=200, default=1)
    
    def __str__(self):
        return self.recipe_title