from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Added name for the home view
    path('add-cart/<pizza_uid>/', add_Cart, name='add_cart'),  # Corrected view name
    path('cart/', cart, name='cart'),  # Corrected view name
    path('remove_cart_items/<cart_item_uid>/', remove_cart_items, name='remove_cart_items'),
    path('orders/',orders,name='orders'),
    path('login/', login_page, name='login'),  # Added name for login view
    path('register/', register_page, name='register'),  # Added name for register view
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
