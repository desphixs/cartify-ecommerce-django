# We import standard Django utilities for handling view logic.
# render: used to load and send HTML templates back to the browser.
# redirect: used to send the user to a different URL (like shifting pages).
from django.shortcuts import render, redirect

# We import the get_user_model function from Django's authentication system.
# Analogy: Instead of hardcoding the import for our User class, get_user_model is like asking
# the settings directory: "Which User blueprint is the active one right now?"
# This is safe and keeps our code completely modular.
from django.contrib.auth import get_user_model, authenticate, login, logout
# We import the login_required decorator from Django's authentication library.
# Analogy: This acts as our professional digital Bouncer.
# By placing this decorator directly above any view function, we instruct Django:
# "Ensure the visitor has an active stamped session pass. If they don't, lock the door,
# block the page, and kick them out straight to the login registration gate!"
from django.contrib.auth.decorators import login_required

# We call get_user_model to retrieve the active custom User model.
User = get_user_model()

# ==============================================================================
# REAL-WORLD ANALOGY: The Custom Registration View
# ------------------------------------------------------------------------------
# Imagine you are a clerk behind the reception desk of a private members-only club.
# When someone walks up:
# 1. If they just want to look at the registration form (GET request), you hand them the paper form.
# 2. If they fill out the form and submit it to you (POST request), you check their details:
#    - Are all the fields filled in?
#    - Is their email already in the registry?
#    - Is their nickname already taken?
# 3. If everything is valid, you write their details down, securely hide (hash) their password
#    so nobody else can read it, and slide their profile into the physical cabinet (database).
# 4. Once saved, you point them towards the official login entrance (redirect to login page).
# ==============================================================================

# We define the view function to handle user registration.
def register_user(request):
    # We check if the browser sent a POST request (meaning the user clicked "Submit" on the form).
    if request.method == 'POST':
        # We extract the email address directly from the form submission dictionary.
        # .strip() removes any accidental spaces the user might have typed at the start/end.
        email = request.POST.get('email', '').strip()
        # We extract the username nickname from the form submission.
        username = request.POST.get('username', '').strip()
        # We extract the password from the form submission.
        password = request.POST.get('password', '')

        # ---- VALIDATION 1: Ensure all fields are filled in ----
        # If any of the fields are completely empty, we reject the form.
        if not email or not username or not password:
            # We send them back to the form, displaying a clear validation error.
            return render(request, 'register.html', {
                'error': 'All fields are required! Please fill out every box.'
            })

        # ---- VALIDATION 2: Check if email is already registered ----
        # We ask our database if a user record with this exact email already exists.
        if User.objects.filter(email=email).exists():
            # We reload the registration page and inform the user that their email is already in use.
            return render(request, 'register.html', {
                'error': 'A user account with this email address already exists!'
            })

        # ---- VALIDATION 3: Check if username is already taken ----
        # We ask our database if a user record with this exact username nickname already exists.
        if User.objects.filter(username=username).exists():
            # We reload the page and tell them to pick a different nickname.
            return render(request, 'register.html', {
                'error': 'This username is already taken. Please choose a different one!'
            })

        # ---- STEP 4: Creating and saving the User securely ----
        # We use 'create_user' instead of the raw 'User.objects.create()' method.
        # Why? Because 'create_user' automatically hashes the password!
        # Analogy: Password hashing is like locking their plain text password in a heavy-duty
        # safe. Even if someone steals the safe (database breach), they cannot read the password inside!
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # ---- STEP 5: Redirect to the login view ----
        # Now that the user is safely written in our database, we redirect them to the login page.
        # This will point to the URL mapped to the name 'login'.
        return redirect('login')

    # If the request method is GET, it means the user just typed in the URL or refreshed.
    # We simply render the empty HTML registration form.
    return render(request, 'register.html')


# ==============================================================================
# REAL-WORLD ANALOGY: The Secure Entry Gate (Login System)
# ------------------------------------------------------------------------------
# Imagine our user has already registered and got their physical membership card.
# Now, they walk up to the entrance gate of the club:
# 1. If they just walk up to look at the entrance lobby (GET request), we show them the beautiful entrance doors (the login form).
# 2. If they present their email address and password (POST request), the gatekeeper performs two checks:
#    - Authenticate: The gatekeeper takes their password, melts it in the special chemical bouncer machine (hashes it),
#      and compares the melted result with the melted safe-key on their membership card in the file cabinet.
#      If the keys match, the gatekeeper says: "Yes, you are indeed who you say you are!" (returns a User object).
#      If they don't match, the gatekeeper rejects them.
#    - Login: The gatekeeper hands them an active, stamped "Visitor Session Pass" (sets up the browser session).
#      This pass stays in their pocket (cookie) so they don't have to keep proving their identity at every single door inside the club!
# 3. Once logged in, we guide them straight into the VIP Lounge (the Dashboard page).
# ==============================================================================

# We define the view function to handle user login.
def login_user(request):
    # We check if the browser sent a POST request (meaning the user clicked "Sign In" on the form).
    if request.method == 'POST':
        # We extract the email address directly from the login form.
        # .strip() removes any accidental spaces the user might have typed at the start/end.
        email = request.POST.get('email', '').strip()
        # We extract the password directly from the login form.
        password = request.POST.get('password', '')

        # ---- VALIDATION 1: Ensure all fields are filled in ----
        if not email or not password:
            # We send them back to the login page, displaying a clear validation error.
            return render(request, 'login.html', {
                'error': 'Both email and password are required to sign in!'
            })

        # ---- STEP 2: Authenticate the user against the database ----
        # In our custom model, we configured 'email' as the main login identifier (USERNAME_FIELD).
        # However, Django's built-in 'authenticate' function always expects the login identifier
        # to be passed as the parameter named 'username'.
        # Therefore, we pass email under 'username=email' so the bouncer knows what to search for!
        user = authenticate(request, username=email, password=password)

        # ---- STEP 3: Check if authentication succeeded ----
        # If the email exists and the password hash matches, authenticate returns the User object.
        # If not, it returns None (rejecting the user).
        if user is not None:
            # ---- STEP 4: Start the session ----
            # We call Django's built-in login() function to stamp their session pass.
            # This creates a secure, temporary session cookie in their browser.
            login(request, user)
            
            # ---- STEP 5: Redirect to the dashboard ----
            # Once authenticated and logged in, we send them to their dashboard home page.
            # (We will create and name this route 'dashboard' in Task 5).
            return redirect('dashboard')
        else:
            # If the user is None, the credentials were invalid.
            # We reload the login form with a clear error message.
            # Note: For security, we keep the error slightly generic so hackers don't know
            # whether it was the email or the password that was wrong!
            return render(request, 'login.html', {
                'error': 'Invalid email address or password. Please try again!'
            })

    return render(request, 'login.html')


# ==============================================================================
# REAL-WORLD ANALOGY: The Public Plaza (Index Page)
# ------------------------------------------------------------------------------
# Imagine our home/index view is like the public plaza outside our member club.
# Anyone walking on the street (authenticated members and completely anonymous guests)
# is allowed to stand in the plaza and look around (this view is public).
# However, we display a beautiful information board (our dynamic header):
# 1. If they are a registered member wearing their wristband, we show them their name and a
#    quick link to enter the private VIP Lounge (Go to Dashboard).
# 2. If they are an unauthenticated guest, we show them signposts to get registered or sign in.
# ==============================================================================

# We define the index_view to handle the public home page of our application.
def index_view(request):
    # This view is completely public, so we don't put any decorators here.
    # We simply load and return our home/index page template.
    return render(request, 'index.html')


# ==============================================================================
# REAL-WORLD ANALOGY: The VIP Private Lounge (Protected Dashboard View)
# ------------------------------------------------------------------------------
# Imagine the dashboard is the private VIP lounge inside our members club.
# We hire a strict Bouncer (the @login_required decorator) to stand right in front
# of the lounge doors. 
# 
# When a visitor tries to pull open the door handle (request the dashboard URL):
# 1. The Bouncer checks if they are wearing the active visitor session wristband.
# 2. If yes, the bouncer smiles and lets them inside to see their details.
# 3. If no, the bouncer immediately stops them, grabs their arm, and walks them back 
#    to the lobby reception desk (redirects them straight to the Login page!).
# ==============================================================================

# We place the bouncer decorator directly above our dashboard view function.
# This single line protects the entire view from anonymous guest visits.
@login_required
def dashboard_view(request):
    # If the bouncer lets them pass, request.user will hold the authenticated User object.
    # We load our protected dashboard template and return it to the logged-in user.
    return render(request, 'dashboard.html')


# ==============================================================================
# REAL-WORLD ANALOGY: Handing Back the Session Pass (The Logout Flow)
# ------------------------------------------------------------------------------
# Imagine you are leaving the members-only club for the day. You walk up to the exit desk.
# 
# To officially leave and lock your profile:
# 1. You hand back your stamped Visitor Session Pass (Django's built-in logout() function).
# 2. The clerk immediately cuts the pass in half (destroys the session record in the database)
#    and throws it in the bin (deletes the cookie from the browser).
# 3. Once you walk out the front exit doors, your wristband is completely gone. If you try to turn
#    around and walk back into the VIP Lounge, the bouncer will immediately stop you!
# 4. We then politely guide you back to the front entrance gate (redirect to the login page).
# ==============================================================================

# We define the logout_user view function to clear the current active session.
def logout_user(request):
    # We call Django's built-in logout function.
    # This automatically locates the active session cookie for this request,
    # completely deletes the session record from our database, and clears the cookie from the browser.
    logout(request)
    
    # After successfully destroying their session pass, we redirect the user to the login page.
    return redirect('login')



