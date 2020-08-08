from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from admins.models import Product, ProductCategory, Category, BuyerProduct, BuyerProductCategory
from users.models import Vendor, Buyer
from .models import WishlistItem, CartItem
from taggit.models import Tag
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone

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
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.filter(vendor=self.object.vendor).order_by('-date_created').exclude(product_id=self.object.product_id)
        context['title'] = self.object.name
        context['categories'] = Category.objects.all()
        context['is_seller'] = True

        if ProductCategory.objects.filter(product=self.object).exists():
            context['category'] = ProductCategory.objects.get(product=self.object)

        if WishlistItem.objects.filter(product=self.object, user=self.request.user).exists():
            context['wishlist_item'] = True
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
    
    def get_context_data(self, **kwargs):
        context = super(BuyerProductDetailView, self).get_context_data(**kwargs)
        context['products'] = BuyerProduct.objects.filter(buyer=self.object.buyer).order_by('-date_created').exclude(product_id=self.object.product_id)
        if BuyerProductCategory.objects.filter(product=self.object).exists():
            context['category'] = BuyerProductCategory.objects.get(product=self.object)
        context['title'] = self.object.name
        context['categories'] = Category.objects.all()
        context['is_seller'] = False
        return context

@login_required
def AddToWishlist(request):
    product_id = request.GET.get('product_id')
    product = Product.objects.get(product_id=product_id)
    if WishlistItem.objects.filter(user=request.user, product=product).exists():
        messages.error(request, 'This item is already in your wishlist!')
    else:
        item = WishlistItem(user=request.user, product=product)
        item.save()
        messages.success(request, 'Item added to wishlist!')
    return render(request, 'main/user/wishlist/wishlist.html')

class WishlistView(LoginRequiredMixin, ListView):
    model = WishlistItem
    paginate_by = 6
    
    def get_context_data(self, **kwargs):
        context = super(WishlistView, self).get_context_data(**kwargs)
        context['title'] = "Wishlist"
        context['items'] = WishlistItem.objects.filter(user=self.request.user)
        return context

class WishlistItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = WishlistItem

    def test_func(self):
        return self.request.user.id == self.kwargs['user_pk']

    def get_context_data(self, **kwargs):
        context = super(WishlistItemDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Delete Wishlist Item"
        return context

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Item has been removed from your wishlist')
        return reverse('wishlist')

@login_required
def AddToCart(request):
    product_id = request.GET.get('product_id')
    product = Product.objects.get(product_id=product_id)
    quantity = int(request.GET.get('quantity'))
    if CartItem.objects.filter(user=request.user, product=product).exists():
        item = CartItem.objects.get(user=request.user, product=product)
        if item.quantity == 5:
            messages.error(request, 'Product cap reached!')
            return render(request, 'main/user/cart/cart.html')
        else:
            temp = item.quantity + quantity
            if temp > 5:
                product.item_stock = product.item_stock-(5-item.quantity)
                item.quantity = 5
            else:
                item.quantity = temp
                product.item_stock = product.item_stock-quantity
            date_added = timezone.now()
    else:
        if quantity > 5:
            quantity = 5
        item = CartItem(user=request.user, product=product, quantity=quantity)
        product.item_stock = product.item_stock-quantity

    product.save()
    item.save()
    messages.success(request, 'Item added to wishlist!')
    return render(request, 'main/user/cart/cart.html')

class CartView(LoginRequiredMixin, ListView):
    model = CartItem
    context_object_name = 'items'
    paginate_by = 6
    
    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['title'] = "Cart"
        context['items'] = CartItem.objects.filter(user=self.request.user)
        return context

class CartItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CartItem
    fields = ['quantity']

    def test_func(self):
        return self.request.user.id == self.kwargs['user_pk']

    def get_context_data(self, **kwargs):
        context = super(CartItemUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Edit Item"
        return context
    
    def form_valid(self, form):
        new = form.instance.quantity
        item = CartItem.objects.get(product=self.object.product, user=self.request.user)
        if new == item.quantity:
            return super().form_valid(form)
        elif new > 5:
            messages.error(self.request, 'Maximum of 5 items per product!')
            return self.render_to_response(self.get_context_data(form=form))
        else:
            product = Product.objects.get(product_id=self.object.product.product_id)
            if item.quantity > new:
                dec = item.quantity - new
                product.item_stock = product.item_stock + dec
            elif item.quantity < new:
                add = new - item.quantity 
                product.item_stock = product.item_stock - add
            form.instance.date_added = timezone.now()
            product.save()
            return super().form_valid(form)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Cart item updated!')
        return reverse("cart")

class CartItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CartItem

    def test_func(self):
        return self.request.user.id == self.kwargs['user_pk']

    def get_context_data(self, **kwargs):
        context = super(CartItemDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Delete Cart Item"
        return context
    
    def delete(self, *args, **kwargs):
        product = Product.objects.get(product_id=self.kwargs['product_pk'])
        item = CartItem.objects.get(product=product, user=self.request.user)
        product.item_stock = product.item_stock + item.quantity
        product.save()
        return super(CartItemDeleteView, self).delete(*args, **kwargs)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Item has been removed from your cart')
        return reverse('cart')
