from django.urls import path
from . import views

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
]
