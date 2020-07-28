from django.urls import path
from .views import (
    MainDashboard, 
    VendorListView, VendorDetailView, VendorUpdateView, VendorDeleteView,
    TermCreateView, TermUpdateView, TermDeleteView,
    ProductCreateView, ProductDetailView, ProductUpdateView, ProductDeleteView)

urlpatterns = [
    path('', MainDashboard, name='main-dash'),
    path('vendors/', VendorListView.as_view(
        template_name='admins/vendors/vendors.html'), name='vendors'),
    path('vendor/<int:pk>/', VendorDetailView.as_view(
        template_name='admins/vendors/vendor_detail.html'), name='vendor-detail' ),
    path('vendor/<int:pk>/update/', VendorUpdateView.as_view(
        template_name='admins/vendors/vendor_update.html'), name='vendor-update'),
    path('vendor/<int:pk>/delete/', VendorDeleteView.as_view(
        template_name='admins/vendors/vendor_confirm_delete.html'), name='vendor-delete'),

    path('term/new/', TermCreateView.as_view(
        template_name='admins/products/terms/terms.html'), name='term-create'),
    path('term/<int:pk>/update/', TermUpdateView.as_view(
        template_name='admins/products/terms/term_update.html'), name='term-update'),
    path('term/<int:pk>/delete/', TermDeleteView.as_view(
        template_name='admins/products/terms/term_confirm_delete.html'), name='term-delete'),

    path('vendor/<int:pk>/product/new/', ProductCreateView, name='product-new'),
    path('product/<int:pk>/', ProductDetailView.as_view(
        template_name='admins/products/product_detail.html'), name='product-detail'),
    path('product/<int:pk>/update', ProductUpdateView, name='product-update'),
    path('product/<int:pk>/delete', ProductDeleteView.as_view(
        template_name='admins/products/product_confirm_delete.html'), name='product-delete'),
]