from django.urls import path
import admins.views as v

urlpatterns = [
    path('buyers/', v.BuyerListView.as_view(
        template_name='admins/buyers/buyers.html'), name='buyers'),
    path('buyer/<int:pk>/', v.BuyerDetailView.as_view(
        template_name='admins/buyers/buyer_detail.html'), name='buyer-detail' ),
    path('buyer/<int:pk>/update/', v.BuyerUpdateView.as_view(
        template_name='admins/buyers/buyer_update.html'), name='buyer-update'),
    path('buyer/<int:pk>/delete/', v.BuyerDeleteView.as_view(
        template_name='admins/buyers/buyer_confirm_delete.html'), name='buyer-delete'),

    path('vendors/', v.VendorListView.as_view(
        template_name='admins/vendors/vendors.html'), name='vendors'),
    path('vendor/<int:pk>/', v.VendorDetailView.as_view(
        template_name='admins/vendors/vendor_detail.html'), name='vendor-detail' ),
    path('vendor/<int:pk>/update/', v.VendorUpdateView.as_view(
        template_name='admins/vendors/vendor_update.html'), name='vendor-update'),
    path('vendor/<int:pk>/delete/', v.VendorDeleteView.as_view(
        template_name='admins/vendors/vendor_confirm_delete.html'), name='vendor-delete'),

    path('vendor/<int:pk>/product/new/', v.ProductCreateView, name='product-new'),
    path('product/<str:slug>/', v.ProductDetailView.as_view(
        template_name='admins/products/product_detail.html'), name='product-detail'),
    path('product/<int:pk>/update', v.ProductUpdateView, name='product-update'),
    path('product/<int:pk>/delete', v.ProductDeleteView.as_view(
        template_name='admins/products/product_confirm_delete.html'), name='product-delete'),

    path('buyer/<int:pk>/product/new/', v.BuyerProductCreateView, name='buyer-product-new'),
    path('buyer-product/<str:slug>/', v.BuyerProductDetailView.as_view(
        template_name='admins/products/product_detail.html'), name='buyer-product-detail'),
    path('buyer-product/<int:pk>/update/', v.BuyerProductUpdateView, name='buyer-product-update'),
    path('buyer-product/<int:pk>/delete/', v.BuyerProductDeleteView.as_view(
        template_name='admins/products/product_confirm_delete.html'), name='buyer-product-delete'),

    path('users/', v.UserListView.as_view(
        template_name='admins/users/users.html'), name='users'),
    path('vendor/new/<int:pk>/', v.VendorCreateView.as_view(
        template_name='admins/users/roles/make_seller.html'), name='make-seller'),
    path('buyer/new/<int:pk>/', v.BuyerCreateView.as_view(
        template_name='admins/users/roles/make_buyer.html'), name='make-buyer'),
    path('admin/new/<int:pk>/', v.GiveAdmin, name='make-admin'),
    path('admin/remove/<int:pk>/', v.RemoveAdmin, name='remove-admin'),

    path('users/<int:pk>/wishlist/', v.WishlistView.as_view(
        template_name='admins/users/wishlist.html'), name='user-wishlist'),
    path('users/<int:pk>/cart/', v.CartView.as_view(
        template_name='admins/users/cart.html'), name='user-cart'),

    path('get-orders/', v.get_sort_orders, name='get-sort-orders'),
    path('orders/', v.OrderListView.as_view(
        template_name="admins/orders/orders.html"), name='orders'),
    path('order/<int:pk>/', v.OrderDetailView.as_view(
        template_name="admins/orders/order_detail.html"), name='order-detail'),
    path('order/<int:pk>/update-info/', v.OrderUpdateView.as_view(
        template_name="admins/orders/order_update.html"), name='order-update-info'),
    path('order/<int:pk>/delete/', v.OrderDeleteView.as_view(
        template_name="admins/orders/order_confirm_delete.html"), name="order-delete"),

    path('order/<int:pk>/update-items/', v.OrderItemCreateView.as_view(
        template_name="admins/orders/items/items.html"), name='order-update-items'),
    path('order/<int:product_pk>/<int:order_pk>/<int:pk>/edit/', v.OrderItemUpdateView.as_view(
        template_name="admins/orders/items/item_update.html"), name='order-item-edit'),
    path('order/<int:product_pk>/<int:order_pk>/<int:pk>/delete/', v.OrderItemDeleteView.as_view(
        template_name="admins/orders/items/item_confirm_delete.html"), name='order-item-delete'),

    path('settings/', v.Settings, name="settings"),
    
    path('categories/', v.CategoryCreateView.as_view(
        template_name='admins/settings/categories/categories.html'), name='category-create'),
    path('category/<int:pk>/update/', v.CategoryUpdateView.as_view(
        template_name='admins/settings/categories/category_update.html'), name='category-update'),
    path('category/<int:pk>/delete/', v.CategoryDeleteView.as_view(
        template_name='admins/settings/categories/category_confirm_delete.html'), name='category-delete'),

    path('payments/', v.PaymentCreateView.as_view(
        template_name='admins/settings/payment_methods/payments.html'), name='payment-methods'),
    path('payment/<int:pk>/update/', v.PaymentUpdateView.as_view(
        template_name='admins/settings/payment_methods/payment_update.html'), name='payment-update'),
    path('payment/<int:pk>/delete/', v.PaymentDeleteView.as_view(
        template_name='admins/settings/payment_methods/payment_confirm_delete.html'), name='payment-delete'),
    
    path('rates/', v.ShippingRateCreateView.as_view(
        template_name='admins/settings/shipping_rates/rates.html'), name='shipping-rates'),
    path('rate/<int:pk>/update/', v.ShippingRateUpdateView.as_view(
        template_name='admins/settings/shipping_rates/rate_update.html'), name='rate-update'),
    path('rate/<int:pk>/delete/', v.ShippingRateDeleteView.as_view(
        template_name='admins/settings/shipping_rates/rate_confirm_delete.html'), name='rate-delete'),
    
    path('rate/<int:pk>/vendors/', v.ShippingVendorsListView.as_view(
        template_name='admins/settings/shipping_rates/vendors/rate_vendors.html'), name='rate-vendors'),
    path('rate/<int:pk>/vendor/<int:vendor_pk>/add/', v.AssignVendortoRate.as_view(
        template_name='admins/settings/shipping_rates/vendors/rate_add_vendor.html'), name='rate-vendor-add'),
    path('rate/<int:rate_pk>/vendor/<int:pk>/remove/', v.ShippingVendorDeleteView.as_view(
        template_name='admins/settings/shipping_rates/vendors/rate_remove_vendor.html'),name='rate-vendor-remove'),
]