from django.urls import path
import admins.views as v

urlpatterns = [
    path('service-providers/', v.ProviderListView.as_view(
        template_name='admins/providers/providers.html'), name='providers'),
    path('provider/<int:pk>/', v.ProviderDetailView.as_view(
        template_name='admins/providers/provider_detail.html'), name='provider-detail' ),
    path('provider/<int:pk>/update/', v.ProviderUpdateView.as_view(
        template_name='admins/providers/provider_update.html'), name='provider-update'),
    path('provider/<int:pk>/delete/', v.ProviderDeleteView.as_view(
        template_name='admins/providers/provider_confirm_delete.html'), name='provider-delete'),

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
        template_name='admins/vendors/products/product_detail.html'), name='product-detail'),
    path('product/<int:pk>/update', v.ProductUpdateView, name='product-update'),
    path('product/<int:pk>/delete', v.ProductDeleteView.as_view(
        template_name='admins/vendors/products/product_confirm_delete.html'), name='product-delete'),

    path('provider/<int:pk>/item/new/', v.ServiceItemCreateView, name='service-item-new'),
    path('service-item/<str:slug>/', v.ServiceItemDetailView.as_view(
        template_name='admins/providers/items/service_item_detail.html'), name='service-item-detail'),
    path('service-item/<int:pk>/update/', v.ServiceItemUpdateView, name='service-item-update'),
    path('service-item/<int:pk>/delete/', v.ServiceItemDeleteView.as_view(
        template_name='admins/providers/items/service_item_confirm_delete.html'), name='service-item-delete'),

    path('provider/<int:pk>/service/new/', v.ServiceCreateView, name='service-new'),
    path('service/<str:slug>/', v.ServiceDetailView.as_view(
        template_name='admins/providers/services/service_detail.html'), name='service-detail'),
    path('service/<int:pk>/update/', v.ServiceUpdateView, name='service-update'),
    path('service/<int:pk>/delete/', v.ServiceDeleteView.as_view(
        template_name='admins/providers/services/service_confirm_delete.html'), name='service-delete'),

    path('users/', v.UserListView.as_view(
        template_name='admins/users/users.html'), name='users'),
    path('vendor/new/<int:pk>/', v.VendorCreateView.as_view(
        template_name='admins/users/roles/make_seller.html'), name='make-seller'),
    path('provider/new/<int:pk>/', v.ProviderCreateView.as_view(
        template_name='admins/users/roles/make_provider.html'), name='make-provider'),
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
    path('order-item/<int:pk>/edit/', v.OrderItemUpdateView.as_view(
        template_name="admins/orders/items/item_update.html"), name='order-item-edit'),
    path('order-item/<int:pk>/delete/', v.OrderItemDeleteView.as_view(
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
    
    path('compee-cares/<int:pk>/edit', v.CaresRateUpdateView.as_view(
        template_name='admins/settings/compee_cares/rate_update.html'), name='cares-rate'),
    path('compee-cares/', v.RenewalRequestListView.as_view(
        template_name='admins/settings/compee_cares/requests.html'), name='renewal-requests'),
    path('compee-cares/request/<int:pk>/', v.RenewalRequestDetailView.as_view(
        template_name='admins/settings/compee_cares/request_detail.html'), name='renewal-request'),
    path('compee-cares/request/<int:pk>/resolve/', v.ResolveRenewalRequest.as_view(
        template_name='admins/settings/compee_cares/request_resolve.html'), name='renewal-request-resolve'),
    path('compee-cares/request/<int:pk>/unresolve/', v.UnresolveRenewalRequest.as_view(
        template_name='admins/settings/compee_cares/request_unresolve.html'), name='renewal-request-unresolve'),
    path('compee-cares/request/<int:pk>/delete/', v.RenewalRequestDeleteView.as_view(
        template_name='admins/settings/compee_cares/request_confirm_delete.html'), name='renewal-request-delete'),

    path('product-guides/', v.ProductGuideListView.as_view(
        template_name='admins/settings/product_guides/guides.html'),name='product-guides'),
    path('product-guides/new', v.ProductGuideCreateView.as_view(
        template_name='admins/settings/product_guides/guide_create.html'),name='guide-create'),
    path('product-guides/<int:pk>/detail/', v.ProductGuideDetailView.as_view(
        template_name='admins/settings/product_guides/guide_detail.html'),name='guide-detail'),
    path('product-guides/<int:pk>/update/', v.ProductGuideUpdateView.as_view(
        template_name='admins/settings/product_guides/guide_update.html'),name='guide-update'),
    path('product-guides/<int:pk>/delete/', v.ProductGuideDeleteView.as_view(
        template_name='admins/settings/product_guides/guide_delete.html'),name='guide-delete'),

    path('display-groups/', v.DisplayGroupCreateView.as_view(
        template_name='admins/settings/display_groups/display_groups.html'), name='display-groups'),
    path('display-group/<int:pk>/update/', v.DisplayGroupUpdateView.as_view(
        template_name='admins/settings/display_groups/display_group_edit.html'), name='display-group-edit'),
    path('display-group/<int:pk>/delete/', v.DisplayGroupDeleteView.as_view(
        template_name='admins/settings/display_groups/display_group_confirm_delete.html'), name='display-group-delete'),
    
    path('display-group/<int:pk>/edit-products/', v.EditProductsInGroup, name='edit-products'),
    path('display-group/<int:pk>/add-products/', v.AddProductsToGroup, name='add-products')
]