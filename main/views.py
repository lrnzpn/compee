from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from admins.models import (
    Product, ProductCategory, Category, BuyerProduct, BuyerProductCategory, ProductReview, VendorShipping ) 
from users.models import Vendor, Buyer, VendorReview
from .models import WishlistItem, CartItem, SiteOrder, OrderItem, Transaction
from taggit.models import Tag
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
import decimal
from admins.funcs import updateVendorStatus

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

def SearchBar(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        context = {
            'title':"Search results for " + query,
            'is_seller': True,
            'query':query
        }
        queries = query.split(" ")
        products = []
        vendors = []
        for q in queries:
            prods = Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(tags__name__icontains=q)).distinct()
            if prods:
                for prod in prods:
                    if prod.vendor.status == "Active":
                        products.append(prod)

            sellers = Vendor.objects.filter(Q(store_name__icontains=q) | Q(store_info__icontains=q)).distinct()
            if sellers:
                for vendor in sellers:
                    vendors.append(vendor)
        
        if products:
            context.update({'products':list(set(products))})
        if vendors:
            context.update({'vendors':list(set(vendors))})
        return render(request, 'main/filters/search_result.html', context )

def TagProductsListView(request, name):
    tag = get_object_or_404(Tag, name=name)
    products = Product.objects.filter(tags=tag)
    for p in products:
        if p.vendor.status == "Inactive":
            products = products.exclude(product_id=p.product_id)
    context = {
        'products' : products,
        'tag' : tag,
        'title' : f"Search for '{tag}'",
        'is_seller': True
    }
    return render(request, 'main/filters/tag_detail.html', context )

def CategoryProductsListView(request, name):
    category = Category.objects.get(name=name)
    product_cats = ProductCategory.objects.filter(category=category)
    for p in product_cats:
        if p.product.vendor.status == "Inactive":
            product_cats = product_cats.exclude(product=p.product)
    products = []
    for i in product_cats:
        products.append(i.product)
    context = {
        'products' : products,
        'category' : category,
        'title' : f"Search for '{category}'",
        'is_seller': True
    }
    return render(request, 'main/filters/category_detail.html', context )

class VendorListView(ListView):
    model = Vendor
    context_object_name = 'vendors'
    paginate_by = 12

    def get_queryset(self):
        return Vendor.objects.filter(status="Active")

    def get_context_data(self, **kwargs):
        context = super(VendorListView, self).get_context_data(**kwargs)
        updateVendorStatus()
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
        context['reviews'] = VendorReview.objects.filter(vendor=self.object)
        if self.object.status == "Inactive":
            context['inactive'] = True
        return context

class ProductDetailView(DetailView):
    model = Product
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['title'] = self.object.name
        context['categories'] = Category.objects.all()
        if self.object.vendor.status == "Inactive":
            context['inactive'] = True
        else:
            context['products'] = Product.objects.filter(vendor=self.object.vendor).order_by('-date_created').exclude(product_id=self.object.product_id)
            context['is_seller'] = True
            context['reviews'] = ProductReview.objects.filter(product=self.object)

            if ProductCategory.objects.filter(product=self.object).exists():
                context['category'] = ProductCategory.objects.get(product=self.object)

            if WishlistItem.objects.filter(product=self.object, user=self.request.user).exists():
                context['wishlist_item'] = True

            similar = Product.objects.filter(name=self.object.name).exclude(product_id=self.object.product_id)
            if similar:
                context['similar'] = True
        return context

def PriceComparison(request, name):
    products = Product.objects.filter(name=name)
    for p in products:
        if p.vendor.status == "Inactive":
            products = products.exclude(product_id=p.product_id)
    context = {
        'products' : products,
        'name' : name,
        'title' : f"Prices for '{name}'",
        'is_seller': True
    }
    return render(request, 'main/filters/price_comparison.html', context)

class BuyerListView(ListView):
    model = Buyer
    context_object_name = 'buyers'
    paginate_by = 12
    
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
        if buyer.user == self.request.user:
            context['is_owner'] = True
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
        context['is_owner'] = self.object.buyer.user.id == self.request.user.id
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
    context_object_name = 'items'
    paginate_by = 6

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super(WishlistView, self).get_context_data(**kwargs)
        context['title'] = "Wishlist"
        return context

class WishlistItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = WishlistItem

    def test_func(self):
        return self.request.user.id == self.kwargs['user_pk'] or self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(WishlistItemDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Delete Wishlist Item"
        return context

    def get_success_url(self, **kwargs):
        if self.request.user.groups.filter(name='Admin').exists():
            messages.success(self.request, 'Item has been removed from their wishlist')
            return reverse("user-wishlist", kwargs={'pk':self.kwargs['user_pk']})
        else:
            messages.success(self.request, 'Item has been removed from your wishlist')
            return reverse('wishlist')

@login_required
def AddToCart(request):
    product_id = request.GET.get('product_id')
    product = Product.objects.get(product_id=product_id)
    quantity = request.GET.get('quantity')
    if quantity == None:
        quantity = 1
    else:
        quantity = int(request.GET.get('quantity'))

    if product.item_stock < quantity:
        messages.error(request, 'Item is out of stock!')
        return render(request, 'main/user/cart/cart.html')
    else:
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
    
    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['title'] = "Cart"
        vendors = []
        fees = []
        for i in CartItem.objects.filter(user=self.request.user):
            if i.product.vendor.vendor_id not in vendors:
                vendor = Vendor.objects.get(vendor_id=i.product.vendor.vendor_id)
                if VendorShipping.objects.filter(vendor=vendor).exists():
                    fees.append(VendorShipping.objects.get(vendor=vendor))
                vendors.append(i.product.vendor.vendor_id)

        if len(vendors) == len(fees):
            context['fees'] = fees
        else:
            messages.error(self.request, 'At least one of the selected vendors have not set a shipping rate.')
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
        return self.request.user.id == self.kwargs['user_pk'] or self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(CartItemDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Delete Cart Item"
        return context
    
    def delete(self, *args, **kwargs):
        product = Product.objects.get(product_id=self.kwargs['product_pk'])
        user = User.objects.get(id=self.kwargs['user_pk'])
        item = CartItem.objects.get(product=product, user=user)
        product.item_stock = product.item_stock + item.quantity
        product.save()
        return super(CartItemDeleteView, self).delete(*args, **kwargs)

    def get_success_url(self, **kwargs):
        if self.request.user.groups.filter(name='Admin').exists():
            messages.success(self.request, 'Item has been removed from their cart')
            return reverse("user-cart", kwargs={'pk':self.kwargs['user_pk']})
        else:
            messages.success(self.request, 'Item has been removed from your cart')
            return reverse('cart')

class Checkout(LoginRequiredMixin, CreateView):
    model = SiteOrder
    fields = ['contact_no', 'address_line', 'city', 'state', 'zip_code', 'payment_method']

    def get_context_data(self, **kwargs):
        context = super(Checkout, self).get_context_data(**kwargs)
        context['title'] = "Checkout"
        context['items'] = CartItem.objects.filter(user=self.request.user)
        vendors = []
        fees = []
        for i in CartItem.objects.filter(user=self.request.user):
            if i.product.vendor.vendor_id not in vendors:
                vendor = Vendor.objects.get(vendor_id=i.product.vendor.vendor_id)
                if VendorShipping.objects.filter(vendor=vendor).exists():
                    fees.append(VendorShipping.objects.get(vendor=vendor))
                vendors.append(i.product.vendor.vendor_id)

        if len(vendors) == len(fees):
            context['fees'] = fees
        else:
            messages.error(self.request, 'At least one of the selected vendors have not set a shipping rate.')
        return context

    def form_valid(self, form):
        items = CartItem.objects.filter(user=self.request.user)
        order_list = []
        for i in items:
            order = {
                'vendor_id': None,
                'items' : [],
                'total' : 0.00
            }
            product = {
                'product_id': None,
                'quantity': 0
            }

            vendor = i.product.vendor.vendor_id
            if order_list == [] or not any(d['vendor_id'] == vendor for d in order_list):
                order['vendor_id'] = vendor
                product['product_id'] = i.product.product_id
                product['quantity'] = i.quantity
                order['items'] = [product]
                order['total'] = i.product.price * decimal.Decimal(i.quantity)
                order_list.append(order)
            else:
                for d in order_list:
                    if d['vendor_id'] == vendor:
                        product['product_id'] = i.product.product_id
                        product['quantity'] = i.quantity
                        d['items'].append(product)
                        d['total'] = d['total'] + i.product.price * decimal.Decimal(i.quantity)
        first = True
        for d in order_list:
            vendor = Vendor.objects.get(vendor_id=d['vendor_id'])
            fee = VendorShipping.objects.get(vendor=vendor)
            if first:
                form.instance.user = self.request.user
                form.instance.total = d['total'] + fee.rate.rate
                form.instance.shipping_fee = fee.rate
                first = False
            else:
                order = SiteOrder(
                    user=self.request.user, 
                    contact_no=form.instance.contact_no,
                    total= d['total'] + fee.rate.rate,
                    payment_method= form.instance.payment_method,
                    address_line=form.instance.address_line,
                    city=form.instance.city,
                    state=form.instance.state,
                    zip_code= form.instance.zip_code,
                    shipping_fee= fee.rate
                )
                order.save()
                if form.instance.payment_method.title == "Credit Card":
                    transaction = Transaction(order=order)
                    transaction.save()

                for i in d['items']:
                    prod = Product.objects.get(product_id=i['product_id'])
                    item = OrderItem(order=order, product=prod, quantity=i['quantity'])
                    item.save()
                    c_item = CartItem.objects.get(product=prod, user=self.request.user)
                    c_item.delete()

        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        items = CartItem.objects.filter(user=self.request.user)
        for i in items:
            item = OrderItem(order=self.object, product=i.product, quantity=i.quantity)
            item.save()
            i.delete()
        if self.object.payment_method.title == "Credit Card":
            transaction = Transaction(order=self.object)
            transaction.save()
            return reverse("payment", kwargs={'pk':Transaction.objects.get(order=self.object).transaction_id})
        else:
            messages.success(self.request, 'Your order has been received!')
            return reverse("home")

class OrderListView(LoginRequiredMixin, ListView):
    model = SiteOrder

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['title'] = "My Orders"
        orders = SiteOrder.objects.filter(user=self.request.user).order_by('status')
        if orders:
            items = []
            for i in orders:
                items.append(OrderItem.objects.filter(order=i))
            context['orders'] = orders
            context['items'] = items
        return context

class CancelOrderView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SiteOrder
    fields = []

    def test_func(self):
        order = SiteOrder.objects.get(order_id = self.kwargs['pk'])
        return order.user.id == self.request.user.id

    def get_context_data(self, **kwargs):
        context = super(CancelOrderView, self).get_context_data(**kwargs)
        context['title'] = "Cancel Order"
        order = SiteOrder.objects.get(order_id=self.kwargs['pk'])
        context['items'] = OrderItem.objects.filter(order=order)
        return context

    def form_valid(self, form):
        form.instance.status = "Cancelled"
        order = SiteOrder.objects.get(order_id=self.kwargs['pk'])
        items = OrderItem.objects.filter(order=order)
        for i in items:
            product = Product.objects.get(product_id=i.product.product_id)
            product.quantity = product.quantity + i.quantity
            product.save()

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Your order has been cancelled')
        return reverse("my-orders")

@login_required
def ReceiveOrder(request):
    order_id = request.GET.get('order_id')
    order = SiteOrder.objects.get(order_id = order_id)
    if order.user.id == request.user.id:
        order.status = "Received"
        order.save()
    return render(request, 'main/orders/orders.html')

@login_required
def AddReviewPage(request, pk):
    order = SiteOrder.objects.get(order_id=pk)
    if order.user.id == request.user.id:
        if order.status == "Received":
            items = OrderItem.objects.filter(order=order)
            context = {
                'order':order,
                'items':items,
            }
            vendor = VendorReview.objects.filter(author=request.user, vendor=items[0].product.vendor)
            if vendor:
                context.update({'review':vendor.first()})
            return render(request, 'main/orders/reviews/add_review.html', context)
        else:
            messages.error(request, 'This order has not yet been received!')
            return redirect('home')
    else:
        return reverse('home')

class VendorReviewCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = VendorReview
    fields = ['rating', 'description']

    def test_func(self):
        order = SiteOrder.objects.get(order_id = self.kwargs['pk'])
        return order.user.id == self.request.user.id

    def get_context_data(self, **kwargs):
        context = super(VendorReviewCreateView, self).get_context_data(**kwargs)
        context['title'] = "Vendor Review"
        order = SiteOrder.objects.get(order_id=self.kwargs['pk'])
        if order.status == "Received":
            context['received'] = True
        item = OrderItem.objects.filter(order=order).first()
        if VendorReview.objects.filter(author=self.request.user, vendor=item.product.vendor).exists():
            context['review'] = VendorReview.objects.get(author=self.request.user, vendor=item.product.vendor)
        context['order'] = order
        return context

    def form_valid(self, form):
        order = SiteOrder.objects.get(order_id = self.kwargs['pk'])
        if order.status == "Received":
            item = OrderItem.objects.filter(order=order).first()
            vendor = item.product.vendor
            if VendorReview.objects.filter(author=self.request.user, vendor=vendor).exists():
                messages.error(request, 'Vendor review already exists!')
                return redirect('home')
            else:
                form.instance.author = self.request.user
                form.instance.vendor = vendor
                form.instance.order = order
                return super().form_valid(form)
        else:
            messages.error(request, 'This order has not yet been received!')
            return redirect('home')
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Vendor review added!')
        return reverse("vendor-detail-main", kwargs={'slug':self.object.vendor.slug})

class VendorReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = VendorReview
    fields = ['rating', 'description']

    def test_func(self):
        review = VendorReview.objects.get(review_id=self.kwargs['pk'])
        return review.author.id == self.request.user.id or self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(VendorReviewUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Edit Vendor Review"
        return context
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Review updated!')
        return reverse("vendor-detail-main", kwargs={'slug':self.object.vendor.slug})

class VendorReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = VendorReview

    def test_func(self):
        review = VendorReview.objects.get(review_id=self.kwargs['pk'])
        return review.author.id == self.request.user.id or self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(VendorReviewDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Delete Vendor Review"
        return context

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Vendor review has been deleted')
        return reverse('home')

class ProductReviewCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ProductReview
    fields = ['rating', 'description']

    def test_func(self):
        order = SiteOrder.objects.get(order_id = self.kwargs['order_pk'])
        return order.user.id == self.request.user.id

    def get_context_data(self, **kwargs):
        context = super(ProductReviewCreateView, self).get_context_data(**kwargs)
        context['title'] = "Product Review"
        order = SiteOrder.objects.get(order_id=self.kwargs['order_pk'])
        if order.status == "Received":
            context['received'] = True
        if ProductReview.objects.filter(author=self.request.user, product_id=self.kwargs['pk']).exists():
            context['review'] = ProductReview.objects.get(author=self.request.user, product_id=self.kwargs['pk'])
        context['order'] = order
        return context

    def form_valid(self, form):
        order = SiteOrder.objects.get(order_id = self.kwargs['order_pk'])
        if order.status == "Received":
            product = Product.objects.get(product_id=self.kwargs['pk'])
            if ProductReview.objects.filter(author=self.request.user, product=product).exists():
                messages.error(request, 'Product review already exists!')
                return redirect('home')
            else:
                form.instance.author = self.request.user
                form.instance.product = product
                form.instance.order = order
                return super().form_valid(form)
        else:
            messages.error(request, 'This order has not yet been received!')
            return redirect('home')
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Product review added!')
        return reverse("vendor-product", kwargs={'slug':self.object.product.slug})

class ProductReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ProductReview
    fields = ['rating', 'description']

    def test_func(self):
        review = ProductReview.objects.get(review_id=self.kwargs['pk'])
        return review.author.id == self.request.user.id or self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(ProductReviewUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Edit Product Review"
        return context
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Review updated!')
        return reverse("vendor-product", kwargs={'slug':self.object.product.slug})

class ProductReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProductReview

    def test_func(self):
        review = ProductReview.objects.get(review_id=self.kwargs['pk'])
        return review.author.id == self.request.user.id or self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(ProductReviewDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Delete Product Review"
        return context

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Product review has been deleted')
        return reverse('home')




    

    

    