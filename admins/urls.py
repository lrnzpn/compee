from django.urls import path
from .views import (
    BuyerListView, BuyerDetailView, BuyerUpdateView, BuyerDeleteView,
    VendorListView, VendorDetailView, VendorUpdateView, VendorDeleteView,
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    ProductCreateView, ProductDetailView, ProductUpdateView, ProductDeleteView,
    BuyerProductCreateView, BuyerProductDetailView, BuyerProductUpdateView, BuyerProductDeleteView,
    UserListView, VendorCreateView, BuyerCreateView, GiveAdmin, RemoveAdmin,
    get_sort_orders, OrderListView, OrderDetailView, OrderUpdateView, OrderDeleteView,
    OrderItemCreateView, OrderItemUpdateView, OrderItemDeleteView
)


urlpatterns = [
    path('buyers/', BuyerListView.as_view(
        template_name='admins/buyers/buyers.html'), name='buyers'),
    path('buyer/<int:pk>/', BuyerDetailView.as_view(
        template_name='admins/buyers/buyer_detail.html'), name='buyer-detail' ),
    path('buyer/<int:pk>/update/', BuyerUpdateView.as_view(
        template_name='admins/buyers/buyer_update.html'), name='buyer-update'),
    path('buyer/<int:pk>/delete/', BuyerDeleteView.as_view(
        template_name='admins/buyers/buyer_confirm_delete.html'), name='buyer-delete'),

    path('vendors/', VendorListView.as_view(
        template_name='admins/vendors/vendors.html'), name='vendors'),
    path('vendor/<int:pk>/', VendorDetailView.as_view(
        template_name='admins/vendors/vendor_detail.html'), name='vendor-detail' ),
    path('vendor/<int:pk>/update/', VendorUpdateView.as_view(
        template_name='admins/vendors/vendor_update.html'), name='vendor-update'),
    path('vendor/<int:pk>/delete/', VendorDeleteView.as_view(
        template_name='admins/vendors/vendor_confirm_delete.html'), name='vendor-delete'),

    path('category/new/', CategoryCreateView.as_view(
        template_name='admins/products/categories/categories.html'), name='category-create'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(
        template_name='admins/products/categories/category_update.html'), name='category-update'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(
        template_name='admins/products/categories/category_confirm_delete.html'), name='category-delete'),

    path('vendor/<int:pk>/product/new/', ProductCreateView, name='product-new'),
    path('product/<str:slug>/', ProductDetailView.as_view(
        template_name='admins/products/product_detail.html'), name='product-detail'),
    path('product/<int:pk>/update', ProductUpdateView, name='product-update'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(
        template_name='admins/products/product_confirm_delete.html'), name='product-delete'),

    path('buyer/<int:pk>/product/new/', BuyerProductCreateView, name='buyer-product-new'),
    path('buyer-product/<str:slug>/', BuyerProductDetailView.as_view(
        template_name='admins/products/product_detail.html'), name='buyer-product-detail'),
    path('buyer-product/<int:pk>/update/', BuyerProductUpdateView, name='buyer-product-update'),
    path('buyer-product/<int:pk>/delete/', BuyerProductDeleteView.as_view(
        template_name='admins/products/product_confirm_delete.html'), name='buyer-product-delete'),

    path('users/', UserListView.as_view(
        template_name='admins/users/users.html'), name='users'),
    path('vendor/new/<int:pk>/', VendorCreateView.as_view(
        template_name='admins/users/make_seller.html'), name='make-seller'),
    path('buyer/new/<int:pk>/', BuyerCreateView.as_view(
        template_name='admins/users/make_buyer.html'), name='make-buyer'),
    path('admin/new/<int:pk>/', GiveAdmin, name='make-admin'),
    path('admin/remove/<int:pk>/', RemoveAdmin, name='remove-admin'),

    path('get-orders/', get_sort_orders, name='get-sort-orders'),
    path('orders/', OrderListView.as_view(
        template_name="admins/orders/orders.html"), name='orders'),
    path('order/<int:pk>/', OrderDetailView.as_view(
        template_name="admins/orders/order_detail.html"), name='order-detail'),
    path('order/<int:pk>/update-info/', OrderUpdateView.as_view(
        template_name="admins/orders/order_update.html"), name='order-update-info'),
    path('order/<int:pk>/delete/', OrderDeleteView.as_view(
        template_name="admins/orders/order_confirm_delete.html"), name="order-delete"),

    path('order/<int:pk>/update-items/', OrderItemCreateView.as_view(
        template_name="admins/orders/items/items.html"), name='order-update-items'),
    path('order/<int:product_pk>/<int:order_pk>/<int:pk>/edit/', OrderItemUpdateView.as_view(
        template_name="admins/orders/items/item_update.html"), name='order-item-edit'),
    path('order/<int:product_pk>/<int:order_pk>/<int:pk>/delete/', OrderItemDeleteView.as_view(
        template_name="admins/orders/items/item_confirm_delete.html"), name='order-item-delete'),
    
]