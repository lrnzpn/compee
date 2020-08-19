from django.urls import path
from .views import (
    Home, About, Contact,
    TagProductsListView, CategoryProductsListView,
    VendorListView, VendorDetailView, ProductDetailView,
    BuyerListView, BuyerDetailView, BuyerProductDetailView,
    AddToWishlist, WishlistView, WishlistItemDeleteView,
    AddToCart, CartView, CartItemDeleteView, CartItemUpdateView,
    Checkout, OrderListView, CancelOrderView, ReceiveOrder, 
    AddReviewPage, VendorReviewCreateView, VendorReviewUpdateView, VendorReviewDeleteView,
    ProductReviewCreateView, ProductReviewUpdateView, ProductReviewDeleteView
)
from admins.views import BuyerProductCreateView, BuyerProductUpdateView, BuyerProductDeleteView

urlpatterns = [
    path('', Home, name='home'),
    path('about/', About, name='about'),
    path('contact/', Contact, name='contact'),
    path('tag/<str:name>/', TagProductsListView, name='tag-filter'),
    path('category/<str:name>/', CategoryProductsListView, name='category-filter'),

    path('buyers/', BuyerListView.as_view(
        template_name="main/buyers/buyers.html"), name='buyers-main'),
    path('buyer/<str:slug>/', BuyerDetailView.as_view(
        template_name='main/buyers/buyer_detail.html'), name='buyer-detail-main'),
    path('buyer-product/<str:slug>/', BuyerProductDetailView.as_view(
        template_name='main/buyers/products/buyer_product.html'), name='buyer-product'),

    path('buyer-product/<int:pk>/new/', BuyerProductCreateView, name='buyer-product-new-main'),
    path('buyer-product/<int:pk>/update/', BuyerProductUpdateView, name='buyer-product-update-main'),
    path('buyer-product/<int:pk>/delete/', BuyerProductDeleteView.as_view(
        template_name='main/buyers/products/buyer_product_confirm_delete.html'),name='buyer-product-delete-main'),

    path('vendors/', VendorListView.as_view(
        template_name="main/vendors/vendors.html"), name='vendors-main'),
    path('shop/<str:slug>/', VendorDetailView.as_view(
        template_name='main/vendors/vendor_detail.html'), name='vendor-detail-main'),
    path('product/<str:slug>/', ProductDetailView.as_view(
        template_name='main/vendors/vendor_product.html'), name='vendor-product'),

    path('wishlist/add', AddToWishlist, name='wishlist-add'),
    path('wishlist/', WishlistView.as_view(
        template_name="main/user/wishlist/wishlist.html"), name='wishlist'),
    path('wishlist/<int:product_pk>/<int:user_pk>/<int:pk>/remove/', WishlistItemDeleteView.as_view(
        template_name="main/user/wishlist/wishlist_confirm_delete.html"), name='wishlist-remove'),

    path('cart/add/', AddToCart, name='cart-add'),
    path('cart/', CartView.as_view(
        template_name='main/user/cart/cart.html'), name='cart'),
    path('cart/<int:product_pk>/<int:user_pk>/<int:pk>/remove/', CartItemDeleteView.as_view(
        template_name='main/user/cart/cart_confirm_delete.html'), name='cart-remove'),
    path('cart/<int:product_pk>/<int:user_pk>/<int:pk>/edit/', CartItemUpdateView.as_view(
        template_name='main/user/cart/cart_edit_item.html'), name='cart-edit'),

    path('checkout/', Checkout.as_view(
        template_name='main/orders/checkout.html'), name='checkout'),
    path('my-orders', OrderListView.as_view(
        template_name='main/orders/orders.html'), name='my-orders'),
    path('order/<int:pk>/cancel', CancelOrderView.as_view(
        template_name='main/orders/order_confirm_cancel.html'), name='cancel-order'),
    path('order/receive/', ReceiveOrder, name='receive-order' ),

    path('order/<int:pk>/reviews/', AddReviewPage, name='add-review'),

    path('order/<int:pk>/reviews/vendor/new/', VendorReviewCreateView.as_view(
        template_name="main/orders/reviews/vendor/vendor_review_form.html"), name='vendor-review'),
    path('reviews/vendor/<int:pk>/edit/', VendorReviewUpdateView.as_view(
        template_name="main/orders/reviews/vendor/vendor_review_form_edit.html"), name='vendor-review-edit'),
    path('reviews/vendor/<int:pk>/delete/', VendorReviewDeleteView.as_view(
        template_name="main/orders/reviews/vendor/vendor_review_confirm_delete.html"), name='vendor-review-delete'),

    path('order/<int:order_pk>/reviews/product/<int:pk>/new/', ProductReviewCreateView.as_view(
        template_name="main/orders/reviews/product/product_review_form.html"), name='product-review'),
    path('reviews/product/<int:pk>/edit/', ProductReviewUpdateView.as_view(
        template_name='main/orders/reviews/product/product_review_form_edit.html'), name='product-review-edit'),
    path('reviews/product/<int:pk>/delete/', ProductReviewDeleteView.as_view(
        template_name="main/orders/reviews/product/product_review_confirm_delete.html"), name='product-review-delete'),
]