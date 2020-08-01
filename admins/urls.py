from django.urls import path
from .views import (
    MainDashboard, 
    VendorListView, VendorDetailView, VendorUpdateView, VendorDeleteView,
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
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
]