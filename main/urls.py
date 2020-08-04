from django.urls import path
from .views import (
    Home, About, Contact,
    TagProductsListView, CategoryProductsListView,
    VendorListView, VendorDetailView,
    BuyerListView, BuyerDetailView
)

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

    path('vendors/', VendorListView.as_view(
        template_name="main/vendors/vendors.html"), name='vendors-main'),
    path('shop/<str:slug>/', VendorDetailView.as_view(
        template_name='main/vendors/vendor_detail.html'), name='vendor-detail-main'),
]