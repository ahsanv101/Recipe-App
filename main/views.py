from django.shortcuts import render, redirect
from .models import Recipe, recipeseries, recipecategory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm
from django.http import HttpResponse

def single_slug(request, single_slug):
    # first check to see if the url is in categories.

    categories = [c.category_slug for c in recipecategory.objects.all()]
    if single_slug in categories:
        matching_series = recipeseries.objects.filter(recipe_category__category_slug=single_slug)
        series_urls = {}

        for m in matching_series.all():
            part_one = Recipe.objects.filter(recipe_series__recipe_series=m.recipe_series).earliest("recipe_published")
            series_urls[m] = part_one.recipe_slug 

        return render(request=request,
                      template_name='main/category.html',
                      context={"recipe_series": matching_series, "part_ones": series_urls})
    recipes=[t.recipe_slug for t in Recipe.objects.all()]

    if single_slug in recipes:
        this_recipe = Recipe.objects.get(recipe_slug=single_slug)
        recipes_from_series = Recipe.objects.filter(recipe_series__recipe_series=this_recipe.recipe_series).order_by('recipe_published')
        this_recipe_idx = list(recipes_from_series).index(this_recipe)

    return render(request=request,
                    template_name='main/recipe.html',
                    context={"recipe": this_recipe,
                            "sidebar": recipes_from_series,
                            "this_tut_idx": this_recipe_idx})
    
# Create your views here.
def homepage(request):
    return render(request=request,
                  template_name='main/categories.html',
                  context={"categories": recipecategory.objects.all})

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, "New Account Created:{username}")
            
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.info(request, "You are now logged in as {username}")

            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request,"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})


def logout_request(request):
    logout(request)
    messages.info(request,"Logged out")
    return redirect("main:homepage")



def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})