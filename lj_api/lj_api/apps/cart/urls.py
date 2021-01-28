from django.urls import path

from cart import views

urlpatterns = [
    path('add_cart/', views.CartViewSet.as_view(
        {"post": "add_cart", "get": "cart_list", "put": "change_select", "delete": "delete_cart"})),
]
