from django.contrib import admin

from django.db import models

# Register your models here.
from .models import Recipe, recipecategory, recipeseries


class TutorialAdmin(admin.ModelAdmin):
    #fields = ["recipe_title", "recipe_published", "recipe_content"]
    fieldsets = [
        ("Title/date", {'fields': ["recipe_title", "recipe_published"]}),
        ("URL", {'fields': ["recipe_slug"]}),
        ("Series", {'fields': ["recipe_series"]}),
        ("Content", {"fields": ["recipe_content"]})
    ]



admin.site.register(recipecategory)

admin.site.register(recipeseries)

admin.site.register(Recipe, TutorialAdmin)
