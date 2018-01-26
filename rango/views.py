from django.shortcuts import render

from django.http import HttpResponse

from rango.models import Category, Page
from rango.forms import CategoryForm

def index(request):
    category_list_likes = Category.objects.order_by('-likes')[:5]
    page_list_views = Page.objects.order_by('-views')[:5]
    context_dict = {'categories_likes': category_list_likes,
                    'pages_views':page_list_views}

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {}
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
# Create a context dictionary which we can pass
# to the template rendering engine.
    context_dict = {}
    try:
# Can we find a category name slug with the given name?
# If we can't, the .get() method raises a DoesNotExist exception.
# So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
# Retrieve all of the associated pages.
# Note that filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)
# Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
# We also add the category object from
# the database to the context dictionary.
# We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
# We get here if we didn't find the specified category.
# Don't do anything -
# the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None
# Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    form = CategoryForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved
            # We could give a confirmation message
            # But since the most recent category added is on the index page
            # Then we can direct the user back to the index page.
            return index(request)
        else:
            # The supplied form contained errors
            # just print them to the terminal.

            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


