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


# ==============================================================================
# REAL-WORLD ANALOGY: The Shopping Cart Inspector
# ------------------------------------------------------------------------------
# Imagine you're walking through a physical store with your metal shopping cart.
# Before heading to the checkout cashier register, you stop, look inside your
# cart, review every single item you've picked, look at the quantity of each
# product, and calculate the estimated total cost to make sure it fits within
# your budget.
# 
# This `view_cart` view does exactly that digitally! First, the bouncer
# (@login_required) verifies you're logged in. Then, we fetch your unique cart
# object, gather all the items you've added (like 2 shirts and 1 laptop), calculate
# the sum total of those items, and send all this data to our `cart.html` template
# so we can show it to you beautifully on a dedicated cart review page!
# ==============================================================================
@login_required
# Protect this cart review view so that only authenticated members can inspect a shopping session
def view_cart(request):
    # 1. Fetch or initialize the user's active shopping cart bucket.
    # We use `get_or_create` to ensure that if a user visits the cart page before adding anything,
    # we initialize a clean, empty cart for them instead of throwing a database or lookup error.
    # The method returns a tuple: (cart_instance, was_created_boolean), so we unpack the first item.
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # 2. Gather all the individual items linked to this user's cart.
    # We use `.select_related('product')` to optimize our database. In database terms, this is a "JOIN" operation.
    # Instead of asking the database "get this item", then asking again "now get this item's product info" 
    # (which would hit the database repeatedly), we fetch both the item and its product details in a single query!
    cart_items = cart.items.all().select_related('product')
    
    # 3. Calculate the sum total cost of all the products sitting inside the shopping cart.
    # We start our counter at exactly 0.00 dollars.
    total_price = 0
    
    # 4. Iterate through every single item in the cart collection to calculate the cumulative price.
    for item in cart_items:
        # For each item, we multiply the product's individual unit price by the quantity selected.
        # (e.g. if the item is a pair of socks priced at $10.00 and the user has 3 in the cart: $10.00 * 3 = $30.00)
        # We add this calculation to our running total.
        total_price += item.product.price * item.quantity
        
    # 5. Pack our calculated data into a neat dictionary box (context) to ship to the frontend template.
    context = {
        'cart': cart,
        # The primary Cart object representing this user's shopping session
        'cart_items': cart_items,
        # The collection of items currently inside the shopping cart
        'total_price': total_price,
        # The calculated total cost of the customer's shopping basket
    }
    
    # 6. Render the dedicated `cart.html` review page, passing along our context data box!
    return render(request, 'cart.html', context)
