from django.urls import path
from store import views

# ==============================================================================
# REAL-WORLD ANALOGY: The Store Directory
# ------------------------------------------------------------------------------
# Just like the accounts directory points to login and register, our store
# directory maps the paths specifically meant for shopping and browsing.
# Currently, it maps the entrance ('') to our storefront window!
# ==============================================================================
urlpatterns = [
    path('', views.index_view, name='index'),
    # This path expects an integer (like 1, 2, 3) which represents the product ID.
    # When a user goes to /add-to-cart/5/, Django will grab product #5 and send it to our view.
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # ==============================================================================
    # REAL-WORLD ANALOGY: The Checkout Aisle Signpost
    # ------------------------------------------------------------------------------
    # In a supermarket, when you are done shopping, you look up for a signpost that
    # reads "Aisle 10: Checkout & Cart Review." 
    # 
    # This URL route acts as that dynamic signpost! When a user navigates their browser
    # to `/cart/`, this rule catches their request and guides them directly to our
    # `view_cart` clerk function to inspect their items.
    # ==============================================================================
    path('cart/', views.view_cart, name='cart'),
]
