from django.urls import path
from .views import (
    MainDashboard, 
    VendorListView, VendorDetailView, VendorUpdateView, VendorDeleteView)

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
]