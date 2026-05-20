from django.shortcuts import render, redirect, get_object_or_404
# We import the Product model from our local models.py file
# This allows us to interact with the database table that stores all our catalog items
from store.models import Product, Cart, CartItem

# We import login_required to act as a bouncer for our add_to_cart view
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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


# ==============================================================================
# REAL-WORLD ANALOGY: Throwing an Item in Your Cart
# ------------------------------------------------------------------------------
# When you're in a physical store and you like a shirt, you pick it up off the shelf 
# and toss it into your metal shopping cart.
# 
# This view does exactly that digitally! First, the bouncer (@login_required) ensures 
# you actually have an account. If you do, it finds your specific cart, looks at the
# product you clicked, and throws it in! If you already have that product in your cart,
# it simply adds +1 to the quantity instead of making a messy duplicate entry.
# ==============================================================================
@login_required
def add_to_cart(request, product_id):
    # 1. Grab the product from the shelf. If the product ID doesn't exist, throw a 404 Not Found error.
    product = get_object_or_404(Product, id=product_id)
    
    # 2. Get the user's shopping cart bucket. If they don't have one yet, build them a new one!
    # get_or_create returns a tuple: (the_object, created_boolean). We just want the object.
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # 3. Check if this specific product is already sitting inside the cart bucket.
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    # 4. If the item was already in the cart, we just add 1 to the quantity.
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        # Like saying "I already had one pair of these socks in the cart, let's make it two!"
    
    # Send a cheerful success message to the customer using Django's message framework
    messages.success(request, f"Added {product.title} to your cart!")
    
    # 5. Send the customer right back to the storefront so they can keep shopping!
    return redirect('index')
