"""
URL configuration for authify_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# We import path and include from django.urls.
# path: used to define exact web address routes.
# include: used to reference other local app urls.py files, keeping routing modular.
from django.urls import path, include
# We import the admin module to route to Django's built-in administration site.
from django.contrib import admin

# ==============================================================================
# REAL-WORLD ANALOGY: The Central Information Desk
# ------------------------------------------------------------------------------
# Imagine the main `urls.py` is the chief receptionist standing at the front door 
# of the Django tower. 
# 
# When a visitor walks in and asks to visit "/admin/", the chief receptionist 
# handles it directly by pointing them to Django's built-in admin room.
# 
# But when a visitor asks for anything else (like "/register/"), the receptionist
# doesn't know every single private desk layout. Instead, they look at the rule:
# `path('', include('accounts.urls'))`
# 
# This rule tells the receptionist: "For any standard site traffic, hand the visitor's
# map over to the Accounts Department receptionist (accounts.urls) and let them guide
# the visitor to the final desk!"
# ==============================================================================

# We define the master list of URL paths for the entire website.
urlpatterns = [
    # Routes any requests starting with 'admin/' directly to the Django Admin backend.
    path('admin/', admin.site.urls),
    # Include store app urls for the storefront and catalog
    path('', include('store.urls')),
    # We include our accounts app urls.py. By passing an empty string '' as the prefix,
    # we allow routes defined in accounts/urls.py (like 'register/') to be accessed
    # directly at the root level (e.g., 'http://127.0.0.1:8000/register/').
    path('', include('accounts.urls')),
]

# We import settings and static to tell Django how to serve uploaded media files during development
from django.conf import settings
from django.conf.urls.static import static

# ==============================================================================
# REAL-WORLD ANALOGY: The Art Gallery Guide
# ------------------------------------------------------------------------------
# In production (live server), Django refuses to serve uploaded images (media files).
# It's like having an art gallery where the security guard (Django) says "I don't
# handle paintings, I only handle visitors."
# 
# For development on our local computer, we need to temporarily give the security 
# guard a side-job as an art guide. We do this by appending `static(settings.MEDIA_URL, ...)`
# to our url patterns. This tells Django: "When someone asks for an image, go to 
# the MEDIA_ROOT folder, find it, and hand it to them!"
# ==============================================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
