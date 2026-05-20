# We import the admin module from Django to register our models for the Django Admin dashboard.
from django.contrib import admin
# We import the UserAdmin class, which is Django's built-in manager panel designed specifically for users.
from django.contrib.auth.admin import UserAdmin
# We import our custom User model that we just defined in the models.py file.
from .models import User

# ==============================================================================
# REAL-WORLD ANALOGY: Connecting the Security Dashboard
# ------------------------------------------------------------------------------
# Imagine the Django Admin is a physical security control room with screens and buttons.
# If we just registered our new custom User model like a regular database table, Django 
# would give us a very generic panel—just a plain spreadsheet list.
# 
# But users are special! They need specific, heavy-duty controls like password reset 
# buttons, permission toggles, and group assignment grids.
# 
# By registering our custom `User` model along with Django's built-in `UserAdmin` control 
# panel, we tell Django: "Please add our new custom User model to the control room, but 
# give it the high-tech, custom control desk (UserAdmin) so we can manage passwords and 
# permissions easily!"
# ==============================================================================

# We register our custom User model using the standard UserAdmin setup.
# This ensures that when we click a user in the Django Admin, we get the premium layout
# with field groups, permission management, and password helper links.
admin.site.register(User, UserAdmin)
