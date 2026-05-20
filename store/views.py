from django.shortcuts import render

# ==============================================================================
# REAL-WORLD ANALOGY: The Store Front Window
# ------------------------------------------------------------------------------
# Imagine walking past a store in the mall. The storefront window is the first thing 
# you see, showcasing the best products to invite you in.
# Our index_view is the digital storefront window, welcoming both guests and members.
# ==============================================================================
def index_view(request):
    return render(request, 'index.html')
