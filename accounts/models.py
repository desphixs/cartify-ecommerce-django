# We import models from django.db to use base model fields if needed, though AbstractUser handles most.
from django.db import models
# We import AbstractUser, which provides all the standard fields (like password, first_name, last_name)
# of Django's default user model so we don't have to build them from scratch.
from django.contrib.auth.models import AbstractUser

# ==============================================================================
# REAL-WORLD ANALOGY: The Library Card System Upgrade
# ------------------------------------------------------------------------------
# Imagine Django's default user system is like a standard school library card. 
# By default, the librarian identifies you using a unique "Username" (like "john_doe123").
# But usernames are hard to remember, and people often forget them. 
# 
# We want to upgrade this library card so that the librarian looks you up using your 
# unique "Email Address" instead, which is much easier to remember.
# 
# Instead of building a brand-new library card from scratch (which would require us to 
# manually re-create slots for passwords, first names, and permissions), we inherit (copy)
# the standard card's structure using `AbstractUser` and just make two tweaks:
# 1. We make sure every card's email slot is completely unique (no duplicates!).
# 2. We tell the librarian to use the email slot as the main way to identify you.
# ==============================================================================

# We create our custom User class, inheriting from AbstractUser.
# This means our User class starts off with all standard fields (first_name, last_name, groups, etc.).
class User(AbstractUser):
    # Overriding the default email field to make it unique.
    # By default, Django's email field is optional and not unique.
    # We set unique=True so that two different users cannot register with the exact same email.
    # Analogy: This is like telling the librarian that no two library cards can have the same email address.
    email = models.EmailField(unique=True)

    # Setting the USERNAME_FIELD to 'email'.
    # This is a special Django setting that tells Django: "When someone logs in,
    # use the email field as their unique username identifier."
    # Analogy: This is telling the librarian to look up accounts using the email field instead of a username.
    USERNAME_FIELD = 'email'

    # Defining REQUIRED_FIELDS.
    # This list specifies which fields must be filled in when creating a superuser via 'createsuperuser'.
    # Note: USERNAME_FIELD is automatically required and MUST NOT be in this list.
    # We add 'username' here so that Django still prompts for a username when creating a superuser.
    # Analogy: When filling out a new VIP library card form, the librarian still asks for a username nickname.
    REQUIRED_FIELDS = ['username']
