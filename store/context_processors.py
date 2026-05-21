# store/context_processors.py

# We import our CartItem model so we can query the database and count what's in the cart
from store.models import CartItem

# ==============================================================================
# REAL-WORLD ANALOGY: The Shopping Badge Counter
# ------------------------------------------------------------------------------
# Imagine walking through a retail department store. The store clerk continuously 
# counts the items you place into your cart and updates a small digital badge counter 
# visible on the cart's handle so you always know exactly how many items you are 
# holding, no matter which section of the store you walk into.
#
# In Django, a "context processor" is like that helper clerk. It automatically 
# calculates a variable (like the total quantity of all items in the user's cart) 
# and makes it available to *every single HTML page* (like the header or navigation bar) 
# without us having to fetch and pass it manually in every single view function!
# ==============================================================================
def cart_item_count(request):
    # 1. If the customer is not logged in (anonymous guest), they cannot have items in a database-backed cart.
    # Therefore, we return a default count of 0 items.
    if not request.user.is_authenticated:
        return {'cart_count': 0}
        
    try:
        # 2. Query the database to find all CartItem objects belonging to this user's cart.
        # We look up items where the cart's owner matches the currently logged-in user.
        items = CartItem.objects.filter(cart__user=request.user)
        
        # 3. Sum up the quantity field of each item in the cart.
        # For example, if they have 2 laptops and 3 shirts, we sum (2 + 3) to get 5 total items in the cart.
        # If the cart is empty or there are no items, sum() automatically returns 0.
        total_count = sum(item.quantity for item in items)
        
        # 4. Return the key-value dictionary. This key `cart_count` becomes globally
        # accessible as a variable across all our HTML templates!
        return {'cart_count': total_count}
        
    except Exception:
        # Fallback to 0 if anything goes wrong (e.g. database table doesn't exist yet during initial setup/migrations)
        return {'cart_count': 0}
