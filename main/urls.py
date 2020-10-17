from django.urls import path
import main.views as v

urlpatterns = [
    path('search/', v.SearchBar, name='search-bar'),
    path('', v.Home, name='home'),
    path('about/', v.About, name='about'),
    path('contact/', v.Contact, name='contact'),

    path('compee-cares/', v.CompeeCares, name='compee-cares'),
    path('compee-concierge/', v.CompeeConcierge, name='compee-concierge'),
    path('product-guides/', v.ProductGuideListView.as_view(
        template_name='main/pages/concierge/product_guides.html'), name='product-guides-main'),
    path('product-guides/post/<str:slug>', v.ProductGuideDetailView.as_view(
        template_name='main/pages/concierge/product_guide.html'), name='product-guide'),

    path('tag/<str:name>/', v.TagProductsListView, name='tag-filter'),
    path('category/<str:name>/', v.CategoryProductsListView, name='category-filter'),
    path('compare-prices/<str:name>/', v.PriceComparison, name='compare-price'),

    path('services/', v.ProviderListView.as_view(
        template_name="main/providers/providers.html"), name='services-main'),
    path('service/<str:slug>/', v.ProviderDetailView.as_view(
        template_name='main/providers/provider_detail.html'), name='provider-detail-main'),
    path('service-item/<str:slug>/', v.ServiceItemDetailView.as_view(
        template_name='main/providers/service_item.html'), name='service-item'),
    path('service-product/<str:slug>/', v.ServiceDetailView.as_view(
        template_name='main/providers/service_product.html'), name='service-product'),

    path('vendors/', v.VendorListView.as_view(
        template_name="main/vendors/vendors.html"), name='vendors-main'),
    path('shop/<str:slug>/', v.VendorDetailView.as_view(
        template_name='main/vendors/vendor_detail.html'), name='vendor-detail-main'),
    path('product/<str:slug>/', v.ProductDetailView.as_view(
        template_name='main/vendors/vendor_product.html'), name='vendor-product'),

    path('wishlist/add', v.AddToWishlist, name='wishlist-add'),
    path('wishlist/', v.WishlistView.as_view(
        template_name="main/user/wishlist/wishlist.html"), name='wishlist'),
    path('wishlist/<int:pk>/remove/', v.WishlistItemDeleteView.as_view(
        template_name="main/user/wishlist/wishlist_confirm_delete.html"), name='wishlist-remove'),
    path('wishlist/share/',v.ShareWishlist, name='share-wishlist'),
    path('wishlist/share/pdf/', v.wishlist_render_pdf_view, name='share-wishlist-pdf'),

    path('cart/add/', v.AddToCart, name='cart-add'),
    path('cart/', v.CartView.as_view(
        template_name='main/user/cart/cart.html'), name='cart'),
    path('cart/<int:pk>/remove/', v.CartItemDeleteView.as_view(
        template_name='main/user/cart/cart_confirm_delete.html'), name='cart-remove'),
    path('cart/<int:pk>/edit/', v.CartItemUpdateView.as_view(
        template_name='main/user/cart/cart_edit_item.html'), name='cart-edit'),
    
    path('checkout/compee-cares/', v.CompeeCaresForm, name='compee-cares'),
    path('checkout/', v.Checkout.as_view(
        template_name='main/orders/checkout.html'), name='checkout'),
    path('my-orders', v.OrderListView.as_view(
        template_name='main/orders/orders.html'), name='my-orders'),
    path('order/<int:pk>/', v.OrderDetailView.as_view(
        template_name='main/orders/order_detail.html'),name='order-detail-main'),
    path('order/<int:pk>/cancel', v.CancelOrderView.as_view(
        template_name='main/orders/order_confirm_cancel.html'), name='cancel-order'),
    path('order/receive/', v.ReceiveOrder, name='receive-order' ),
    
    path('compee-cares/<str:pk>/request/', v.RequestRenewal, name='request-renewal'),
    path('order/<int:pk>/reviews/', v.AddReviewPage, name='add-review'),

    path('order/<int:pk>/reviews/vendor/new/', v.VendorReviewCreateView.as_view(
        template_name="main/orders/reviews/vendor/vendor_review_form.html"), name='vendor-review'),
    path('reviews/vendor/<int:pk>/edit/', v.VendorReviewUpdateView.as_view(
        template_name="main/orders/reviews/vendor/vendor_review_form_edit.html"), name='vendor-review-edit'),
    path('reviews/vendor/<int:pk>/delete/', v.VendorReviewDeleteView.as_view(
        template_name="main/orders/reviews/vendor/vendor_review_confirm_delete.html"), name='vendor-review-delete'),

    path('order/<int:pk>/reviews/provider/new/', v.ProviderReviewCreateView.as_view(
        template_name="main/orders/reviews/vendor/vendor_review_form.html"), name='provider-review'),
    path('reviews/provider/<int:pk>/edit/', v.ProviderReviewUpdateView.as_view(
        template_name="main/orders/reviews/vendor/vendor_review_form_edit.html"), name='provider-review-edit'),
    path('reviews/provider/<int:pk>/delete/', v.ProviderReviewDeleteView.as_view(
        template_name="main/orders/reviews/vendor/vendor_review_confirm_delete.html"), name='provider-review-delete'),

    path('order/<int:order_pk>/reviews/product/<int:pk>/new/', v.ProductReviewCreateView.as_view(
        template_name="main/orders/reviews/product/product_review_form.html"), name='product-review'),
    path('reviews/product/<int:pk>/edit/', v.ProductReviewUpdateView.as_view(
        template_name='main/orders/reviews/product/product_review_form_edit.html'), name='product-review-edit'),
    path('reviews/product/<int:pk>/delete/', v.ProductReviewDeleteView.as_view(
        template_name="main/orders/reviews/product/product_review_confirm_delete.html"), name='product-review-delete'),
    
    path('order/<int:order_pk>/reviews/service/<int:pk>/new/', v.ServiceReviewCreateView.as_view(
        template_name="main/orders/reviews/product/product_review_form.html"), name='service-review'),
    path('reviews/service/<int:pk>/edit/', v.ServiceReviewUpdateView.as_view(
        template_name='main/orders/reviews/product/product_review_form_edit.html'), name='service-review-edit'),
    path('reviews/service/<int:pk>/delete/', v.ServiceReviewDeleteView.as_view(
        template_name="main/orders/reviews/product/product_review_confirm_delete.html"), name='service-review-delete'),
]