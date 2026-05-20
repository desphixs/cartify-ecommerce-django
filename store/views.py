from django.shortcuts import render
# We import the Product model from our local models.py file
# This allows us to interact with the database table that stores all our catalog items
from store.models import Product

# ==============================================================================
# REAL-WORLD ANALOGY: The Store Front Window
# ------------------------------------------------------------------------------
# Imagine walking past a store in the mall. The storefront window is the first thing 
# you see, showcasing the best products to invite you in.
# Our index_view is the digital storefront window, welcoming both guests and members.
# ==============================================================================
def index_view(request):
    # We ask the database manager to give us every single product stored in the database
    # It's like asking the warehouse manager to bring out all the items they have in stock
    products = Product.objects.all()
    
    # We create a dictionary (context) to pack our products into a neat box
    # This box will be shipped over to our HTML template so it can display them
    context = {
        'products': products
    }
    
    # We return the compiled HTML template 'index.html', and we pass along our context box!
    return render(request, 'index.html', context)
