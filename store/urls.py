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
    # ==============================================================================
    # REAL-WORLD ANALOGY: The Cashier Belt Registers
    # ------------------------------------------------------------------------------
    # In a checkout lane, you have specialized conveyor belt lanes and registers for
    # adding items, subtracting items, or scanning items straight to the trash box.
    # 
    # These three URLs serve as those electronic lane pathways! When a customer taps
    # a plus, minus, or delete button in their browser, Django guides their request
    # directly to the correct database view handler with the specific Item ID to process.
    # ==============================================================================
    path('increment-cart-item/<int:item_id>/', views.increment_cart_item, name='increment_cart_item'),
    path('decrement-cart-item/<int:item_id>/', views.decrement_cart_item, name='decrement_cart_item'),
    path('delete-cart-item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    # ==============================================================================
    # REAL-WORLD ANALOGY: The Billing Desk and Invoice Receipt
    # ------------------------------------------------------------------------------
    # When you decide you're ready to buy, the checkout sign points you first to 
    # the Billing Desk (`checkout/initiate/`) where you enter your shipping details
    # to package everything up into an order invoice. Once that invoice is written,
    # the clerk hands you a slip with an order number and guides you to the dynamic
    # Review & Payment Counter (`checkout/<str:order_id>/`) to look over the details
    # and tap "Pay Now".
    # ==============================================================================
    # 1. Checkout Initiate Route (This handles form submissions from the cart page and builds the order records)
    path('checkout/initiate/', views.checkout_initiate, name='checkout_initiate'),
    # 2. Checkout Invoice Route (This displays the unpaid order details dynamically based on its 7-digit ID)
    path('checkout/<str:order_id>/', views.checkout_page, name='checkout_page'),
    
    # ==============================================================================
    # REAL-WORLD ANALOGY: The Bank Gateways and Success Screens
    # ------------------------------------------------------------------------------
    # When you click the "Pay Now" button on your invoice, you pass through the 
    # payment gate conveyor belt (`checkout/payment/<str:order_id>/`). This creates 
    # the secure Stripe session and guides your browser to their armored payment page.
    # 
    # After filling in your card details, the bank vehicle drives you back to the
    # store's local Customer Service counter (`payment/status/`), which checks the 
    # transaction status and prints a big "APPROVED" or "DECLINED" stamp on your order!
    # ==============================================================================
    # 3. Create Stripe Checkout Session Route (Processes and redirects to Stripe hosted payment form)
    path('checkout/payment/<str:order_id>/', views.create_checkout_session, name='create_checkout_session'),
    # 4. Payment Status Callback Route (Fetches session ID from Stripe to check if transaction succeeded)
    path('payment/status/', views.payment_status, name='payment_status'),
    
    # ==============================================================================
    # REAL-WORLD ANALOGY: The Account Ledger Wing
    # ------------------------------------------------------------------------------
    # In a major department store, they have a secure "Customer loyalty service desk" 
    # wing where members can ask to view their accounts dashboard or request a printed 
    # detailed copy of a past transaction receipt.
    # 
    # These routes lead directly to those two customer services:
    # 1. `/dashboard/` opens up the dynamic loyalty card statistics and order list.
    # 2. `/order/<order_id>/` opens up the full itemized details of a single receipt.
    # ==============================================================================
    # 5. Customer Loyalty Dashboard Route
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # 6. Detailed Receipt View Route
    path('order/<str:order_id>/', views.order_detail_view, name='order_detail'),

]

