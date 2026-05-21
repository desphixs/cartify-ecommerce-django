from django.db import models
from django.conf import settings # We use settings.AUTH_USER_MODEL to refer to our custom User model

# --- 1. CATEGORY MODEL ---
# This model represents a category that groups similar products together (e.g., 'Electronics', 'Clothing').
class Category(models.Model):
    # The name of the category. CharField is used for short text.
    name = models.CharField(max_length=255)
    
    # A slug is a URL-friendly version of the name. It uses only letters, numbers, hyphens, or underscores.
    # unique=True ensures no two categories have the same URL path.
    slug = models.SlugField(unique=True, help_text="Used for clean browser URLs")

    # The Meta class provides extra information about how the model behaves.
    class Meta:
        # Django automatically pluralizes model names, but 'Categorys' looks wrong. 
        # This tells Django to use 'Categories' instead.
        verbose_name_plural = "Categories"

    # This method determines how the object is displayed when printed or viewed in the admin panel.
    def __str__(self):
        return self.name


# --- 2. PRODUCT MODEL ---
# This model represents an individual item available for purchase in our store.
class Product(models.Model):
    # A ForeignKey links this product to exactly one Category. 
    # 'related_name' allows us to access all products inside a category backwards (e.g., category.products.all()).
    # on_delete=models.CASCADE means if the Category is deleted, all its associated products are deleted too.
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    
    # The title or name of the product.
    title = models.CharField(max_length=255)
    
    # FileField allows us to upload an image file. It will be saved inside the 'products/images' directory.
    # null=True, blank=True means an image is completely optional.
    image = models.FileField(upload_to='products/images', null=True, blank=True)
    
    # TextField is for longer descriptions without a strict character limit. Optional field.
    description = models.TextField(blank=True, null=True)
    
    # DecimalField is the safest way to store money because it prevents floating-point rounding errors.
    # max_digits=10 allows numbers up to 99,999,999.99
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    
    # IntegerField tracks how many items we have in our warehouse. Defaults to 0.
    stock = models.IntegerField(default=0) 
    
    # DateTimeField automatically sets the current date and time when the product is first created in the database.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Displays the product's title in the admin panel.
        return self.title


# --- 3. CART MODEL ---
# A Cart holds the items a user intends to buy.
# Since we are enforcing that users MUST be logged in, we link it strictly to the User.
class Cart(models.Model):
    # A ForeignKey links this cart to a registered User. 
    # user cannot be null because guest checkout is disabled.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Tracks when the cart was created.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # We always have a user now, so we return the cart ID and the username.
        return f"Cart {self.id} - User: {self.user.username}"


# --- 4. CART ITEM MODEL ---
# CartItem represents a specific product inside a specific cart, along with the quantity.
class CartItem(models.Model):
    # Links this item to a specific Cart. If the Cart is deleted, the CartItem is deleted too.
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    
    # Links this item to the actual Product being purchased.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # PositiveIntegerField ensures they can't order a negative quantity. Defaults to 1.
    quantity = models.PositiveIntegerField(default=1)

    # ==============================================================================
    # REAL-WORLD ANALOGY: The Subtotal Line on a Receipt
    # ------------------------------------------------------------------------------
    # When you buy 3 shirts at $20.00 each, the receipt doesn't just show $20.00 and
    # let you guess the cost. It shows a subtotal line that multiplies $20.00 by 3
    # to display $60.00 for that row.
    # 
    # This `subtotal` property does exactly that dynamically! Whenever a template
    # calls `{{ item.subtotal }}`, it automatically calculates the total cost of this
    # specific item collection by multiplying the unit price by the quantity selected.
    # ==============================================================================
    @property
    def subtotal(self):
        # Multiply the individual product's unit price by the quantity selected in the cart item
        return self.product.price * self.quantity

    def __str__(self):
        # Example: "2 x MacBook Pro"
        return f"{self.quantity} x {self.product.title}"


import random # Import the random module to generate random integers for our unique order ID

# Helper function to generate a unique 7-digit order ID containing only numbers
def generate_unique_order_id():
    # We use a while loop that runs forever until we find an ID that is not already in the database
    while True:
        # Generate a random 7-digit integer as a string (between 1000000 and 9999999 inclusive)
        new_id = str(random.randint(1000000, 9999999))
        
        # Check the database if this generated ID already exists in any Order record
        if not Order.objects.filter(order_id=new_id).exists():
            # If the ID does not exist, it is unique! We return it and exit the function
            return new_id

# --- 5. ORDER MODEL ---
# Order represents a finalized purchase.
class Order(models.Model):
    # We use SET_NULL so that if a user deletes their account, we don't lose the financial record of their past orders!
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Unique 7-digit order ID containing only numbers, with unique=True to prevent duplicates in the database
    order_id = models.CharField(max_length=7, unique=True, null=True, blank=True, help_text="Unique 7-digit order identifier")
    
    # Shipping Information Fields (Required for delivery)
    full_name = models.CharField(max_length=100)
    
    # The delivery address where the items will be shipped.
    address = models.CharField(max_length=255)
    
    # The total cost of everything in the order.
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Tracks when the order was placed.
    created_at = models.DateTimeField(auto_now_add=True)
    
    # BooleanField tracks if the user has successfully paid for the order yet.
    is_paid = models.BooleanField(default=False)

    # We override the built-in save method to automatically assign a unique 7-digit ID when the order is first created
    def save(self, *args, **kwargs):
        # Check if the order_id has not been set yet
        if not self.order_id:
            # Call our helper generator function to assign a unique 7-digit number
            self.order_id = generate_unique_order_id()
        # Call the parent class's standard save method to store the record in the database
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id} by {self.full_name}"


# --- 6. ORDER ITEM MODEL ---
# OrderItem is a snapshot of a CartItem the moment it was purchased.
class OrderItem(models.Model):
    # Links this item to a specific Order.
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    
    # Links to the Product. 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # The quantity purchased.
    quantity = models.PositiveIntegerField(default=1)
    
    # CRITICAL: We save the price *at the moment of purchase*.
    # If the owner changes the Product price a year later, we don't want old orders to look like they paid the new price!
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # ==============================================================================
    # REAL-WORLD ANALOGY: Line Item Subtotal on a Printed Invoice Receipt
    # ------------------------------------------------------------------------------
    # Similar to how the CartItem calculates dynamic prices, when reviewing a printed
    # receipt, you want to see exactly how much you paid for that row (e.g. 2 books
    # at $15.00 each equals a subtotal of $30.00). 
    # This property performs this calculation using the locked-in historical price.
    # ==============================================================================
    @property
    def subtotal(self):
        # Multiply the frozen purchase price by the quantity ordered
        return self.price * self.quantity

    def __str__(self):
        return f"Item {self.id} for Order {self.order.id}"
