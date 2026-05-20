# We import path from django.urls to register specific URL routes for our views.
from django.urls import path
# We import our views file from the current directory to link paths to our view functions.
from . import views

# ==============================================================================
# REAL-WORLD ANALOGY: The Sub-Department Signposts
# ------------------------------------------------------------------------------
# Imagine the main Django project's urls.py is the giant signpost at the entrance 
# of a major shopping mall. 
# 
# Instead of listing every single item in the grocery section right at the front 
# entrance (which would look cluttered and messy), the main entrance signpost simply 
# points to the "Accounts Department" wing.
# 
# Creating this local `accounts/urls.py` file is like setting up a dedicated, clean
# signpost *inside* the Accounts Department wing, pointing shoppers specifically to
# the "Register" register desk (`/register/`) and eventually the "Login" desk (`/login/`).
# ==============================================================================

# We define the list of URL patterns that are active inside our accounts app.
urlpatterns = [
    # We map the URL path 'register/' directly to our register_user view function.
    # We give it a unique name 'register' so we can refer to this path easily in HTML templates
    # or redirect statements using {% url 'register' %} or redirect('register').
    path('register/', views.register_user, name='register'),
    # We map the URL path 'login/' directly to our login_user view function.
    # We give it a unique name 'login' so we can refer to this path easily in templates
    # and redirect statements (like our register_user view redirecting to 'login'!).
    path('login/', views.login_user, name='login'),
    # We map the URL path 'dashboard/' directly to our protected dashboard_view function.
    # We give it a unique name 'dashboard' to handle post-login redirects and navigation links.
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # We map the URL path 'logout/' directly to our logout_user view function.
    # We give it a unique name 'logout' so templates can safely trigger a sign-out sequence.
    # Analogy: This is the official "Exit Door" signpost pointing to the exit desk.
    path('logout/', views.logout_user, name='logout'),
]

