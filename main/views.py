from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from admins.models import Product, ProductCategory, Category, BuyerProduct, BuyerProductCategory
from users.models import Vendor, Buyer
from django.views.generic import ListView, DetailView

def Home(request):
    categories = Category.objects.all()

    context = {
        'categories' : categories
    }
    return render(request, 'main/pages/home.html', context)

def About(request):
    return render(request, 'main/pages/about.html')

def Contact(request):
    return render(request, 'main/pages/contact.html')

def TagProductsListView(request, name):
    tag = get_object_or_404(Tag, name=name)
    products = Product.objects.filter(tags=tag)
    context = {
        'products' : products,
        'tag' : tag,
        'title' : f"Search for '{tag}'"
    }
    return render(request, 'main/filters/tag_detail.html', context )

def CategoryProductsListView(request, name):
    category = Category.objects.get(name=name)
    product_cats = ProductCategory.objects.filter(category=category)
    products = []
    for i in product_cats:
        products.append(i.product)
    context = {
        'products' : products,
        'category' : category,
        'title' : f"Search for '{category}'"
    }
    return render(request, 'main/filters/category_detail.html', context )

class VendorListView(ListView):
    model = Vendor
    context_object_name = 'vendors'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(VendorListView, self).get_context_data(**kwargs)
        context['title'] = "Vendors"
        context['categories'] = Category.objects.all()
        return context

class VendorDetailView(DetailView):
    model = Vendor
    
    def get_context_data(self, **kwargs):
        context = super(VendorDetailView, self).get_context_data(**kwargs)
        vendor = Vendor.objects.get(slug=self.kwargs['slug'])
        context['products'] = Product.objects.filter(vendor=vendor).order_by('-date_created')
        context['title'] = vendor.store_name
        context['categories'] = Category.objects.all()
        context['is_seller'] = True
        return context

class ProductDetailView(DetailView):
    model = Product

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.filter(vendor=self.object.vendor).order_by('-date_created').exclude(product_id=self.object.product_id)
        if ProductCategory.objects.get(product=self.object):
            context['category'] = ProductCategory.objects.get(product=self.object)
        context['title'] = self.object.name
        context['categories'] = Category.objects.all()
        context['is_seller'] = True
        return context

class BuyerListView(ListView):
    model = Buyer
    context_object_name = 'buyers'
    paginate_by = 6
    
    def get_context_data(self, **kwargs):
        context = super(BuyerListView, self).get_context_data(**kwargs)
        context['title'] = "Buyers"
        context['categories'] = Category.objects.all()
        return context

class BuyerDetailView(DetailView):
    model = Buyer

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(BuyerDetailView, self).get_context_data(**kwargs)
        buyer = Buyer.objects.get(slug=self.kwargs['slug'])
        context['products'] = BuyerProduct.objects.filter(buyer=buyer).order_by('-date_created')
        context['title'] = buyer.store_name
        context['categories'] = Category.objects.all()
        context['is_seller'] = False
        return context

class BuyerProductDetailView(DetailView):
    model = BuyerProduct

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(BuyerProductDetailView, self).get_context_data(**kwargs)
        context['products'] = BuyerProduct.objects.filter(buyer=self.object.buyer).order_by('-date_created').exclude(product_id=self.object.product_id)
        if BuyerProductCategory.objects.get(product=self.object):
            context['category'] = BuyerProductCategory.objects.get(product=self.object)
        context['title'] = self.object.name
        context['categories'] = Category.objects.all()
        context['is_seller'] = False
        return context