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
]
