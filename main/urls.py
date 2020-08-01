from django.urls import path
from .views import index, TagProductsListView, CategoryProductsListView

urlpatterns = [
    path('', index, name='home'),
    path('tag/<str:name>/', TagProductsListView, name='tag-filter'),
    path('category/<str:name>/', CategoryProductsListView, name='category-filter')
]