import decimal
from xhtml2pdf import pisa
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from admins.funcs import updateVendorStatus, get_ref_id, get_wish_ref_id
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView)
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from taggit.models import Tag
from .forms import RenewalForm
from users.models import Vendor, ServiceProvider, VendorReview, ProviderReview
from .models import (
    WishlistItem, SharedWishlist, CartItem, SiteOrder, OrderItem, CompeeCaresRenewal)
from admins.models import (
    Product, ProductCategory, Category, Service, ServiceCategory, ServiceItem, 
    ServiceItemCategory, ProductReview, ServiceReview, VendorShipping, 
    CompeeCaresRate, ProductGuide, DisplayGroup, ProductGroup, Banner, Faq
) 

def SearchBar(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        context = {
            'title':"Search results for " + query,
            'query':query
        }
        queries = query.split(" ")

        products = []
        vendors = []
        services = []
        service_items = []
        providers = []

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

            servs = Service.objects.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(tags__name__icontains=q)).distinct()
            if servs:
                for serv in servs:
                    services.append(serv)

            items = ServiceItem.objects.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(tags__name__icontains=q)).distinct()
            if items:
                for item in items:
                    service_items.append(item)

            s_provs = ServiceProvider.objects.filter(Q(store_name__icontains=q) | Q(provider_info__icontains=q)).distinct()
            if s_provs:
                for prov in s_provs:
                    providers.append(prov)

        context = {'title': 'Search'}
        if products:
            context.update({'products':list(set(products))})
        if vendors:
            context.update({'vendors':list(set(vendors))})

        if services:
            context.update({'services':list(set(services))})
        if service_items:
            context.update({'items':list(set(items))})
        if providers:
            context.update({'providers':list(set(providers))})
        return render(request, 'main/filters/search_result.html', context )

def filterProduct(i_type, item, ratings):
    if i_type == "product":
        if item.vendor.status == "Active":
            if ratings:
                if ProductReview.objects.filter(product=item).exists():
                    rev = ProductReview.objects.get(product=item)
                    return rev.rating in ratings
                else:
                    return 0 in ratings
            else:
                return True
        else:
            return False
    elif i_type == "service":
        if ratings:
            if ServiceReview.objects.filter(service=item).exists():
                rev = ServiceReview.objects.get(service=item)
                return rev.rating in ratings
            else:
                return 0 in ratings
        else:
            return True
    
def SearchFilter(request):
    if request.method == "GET":
        query = request.GET
        products = []
        services = []

        pricemin = ''
        pricemax = ''
        if query['pricemin']:
            pricemin = float(query['pricemin'])
        if query['pricemax']:
            pricemax = float(query['pricemax'])
        
        ratings = []
        if 'rating' in query:
            rating = request.GET.getlist('rating')
            for i in rating:
                ratings.append(int(i))

        if len(query) == 2 or (len(query) == 3 and ratings):
            prods = Product.objects.all()
            servs = Service.objects.all()

            if pricemin and pricemax:
                for prod in prods:
                    if prod.vendor.status == "Active":
                        if pricemin <= prod.price <= pricemax:
                            if filterProduct("product", prod, ratings):
                                products.append(prod)
                for serv in servs:
                    if pricemin <= serv.price <= pricemax:
                        if filterProduct("service", serv, ratings):
                            services.append(serv)
            elif pricemin:
                for prod in prods:
                    if prod.vendor.status == "Active":
                        if pricemin <= prod.price:
                            if filterProduct("product", prod, ratings):
                                products.append(prod)
                for serv in servs:
                    if pricemin <= serv.price:
                        if filterProduct("service", serv, ratings):
                            services.append(serv)
            elif pricemax:
                for prod in prods:
                    if prod.vendor.status == "Active":
                        if pricemax >= prod.price:
                            if filterProduct("product", prod, ratings):
                                products.append(prod)
                for serv in servs:
                    if pricemax >= serv.price:
                        if filterProduct("service", serv, ratings):
                            services.append(serv)
            else:
                for prod in prods:
                    if prod.vendor.status == "Active":
                        if filterProduct("product", prod, ratings):
                            products.append(prod)
                for serv in servs:
                    if filterProduct("service", serv, ratings):
                        services.append(serv)

        else:
            for i in query:
                if i != "pricemin" and i != "pricemax" and i != 'rating':
                    q = query[i]
                    prods = Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(tags__name__icontains=q)).distinct()
                    if prods:
                        if pricemin and pricemax:
                            for prod in prods:
                                if pricemin <= prod.price <= pricemax:
                                    if filterProduct("product", prod, ratings):
                                        products.append(prod)
                        elif pricemin:
                            for prod in prods:
                                if pricemin <= prod.price:
                                    if filterProduct("product", prod, ratings):
                                        products.append(prod)
                        elif pricemax:
                            for prod in prods:
                                if pricemax >= prod.price:
                                    if filterProduct("product", prod, ratings):
                                        products.append(prod)
                        else:
                            for prod in prods:
                                if filterProduct("product", prod, ratings):
                                    products.append(prod)

                    servs = Service.objects.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(tags__name__icontains=q)).distinct()
                    if servs:
                        if pricemin and pricemax:
                            for serv in servs:
                                if pricemin <= serv.price <= pricemax:
                                    if filterProduct("service", serv, ratings):
                                        services.append(serv)
                        elif pricemin:
                            for serv in servs:
                                if pricemin <= serv.price:
                                    if filterProduct("service", serv, ratings):
                                        services.append(serv)
                        elif pricemax:
                            for serv in servs:
                                if pricemax >= serv.price:
                                    if filterProduct("service", serv, ratings):
                                        services.append(serv)
                        else:
                            for serv in servs:
                                if filterProduct("service", serv, ratings):
                                    services.append(serv)   

        context = {'title': 'Search'}
        if products:
            context.update({'products':list(set(products))})
        if services:
            context.update({'services':list(set(services))})
                
        return render(request, 'main/filters/search_result.html', context)

def Home(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories,
        'banner': Banner.objects.all().first()
    }
    q_groups = DisplayGroup.objects.filter(enabled=True)
    if q_groups:
        groups = []
        for i in q_groups:
            products = ProductGroup.objects.filter(group=i)
            group = {
                'title':i.title,
                'products':products
            }
            groups.append(group)
        context.update({'groups':groups})
    return render(request, 'main/pages/home.html', context)

def About(request):
    context = {
        'title': 'About Us'
    }
    return render(request, 'main/pages/about.html', context)

def Contact(request):
    context = {
        'title': 'Contact Us'
    }
    return render(request, 'main/pages/contact.html', context)

def CompeeConcierge(request):
    context = {
        'title': 'Compee Concierge', 
        'guides' : ProductGuide.objects.all()[:3],
        'faqs': Faq.objects.all()
    }
    return render(request, 'main/pages/concierge/concierge.html', context)

def CompeeCares(request):
    context = {
        'title': 'Compee Cares'
    }
    return render(request, 'main/pages/cares.html', context)

class ProductGuideListView(ListView):
    model = ProductGuide
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(ProductGuideListView, self).get_context_data(**kwargs)
        context['title'] = "Product Guides"
        return context

class ProductGuideDetailView(DetailView):
    model = ProductGuide

    def get_context_data(self, **kwargs):
        context = super(ProductGuideDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Product Guides | {self.object.title}'
        return context

class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['title'] = "All Categories"
        return context

def TagProductsListView(request, name):
    tag = get_object_or_404(Tag, name=name)

    products = Product.objects.filter(tags=tag)
    for p in products:
        if p.vendor.status == "Inactive":
            products = products.exclude(product_id=p.product_id)
    
    services = Service.objects.filter(tags=tag)
    items = ServiceItem.objects.filter(tags=tag)

    context = {
        'products' : products,
        'services':services,
        'items':items,
        'tag' : tag,
        'title' : f"Search for '{tag}'"
    }
    return render(request, 'main/filters/tag_detail.html', context )

def CategoryProductsListView(request, name):
    category = Category.objects.get(name=name)
    product_cats = ProductCategory.objects.filter(category=category)
    for p in product_cats:
        if p.product.vendor.status == "Inactive":
            product_cats = product_cats.exclude(product=p.product)
    service_cats = ServiceCategory.objects.filter(category=category)
    # service_item_cats = ServiceItemCategory.objects.filter(category=category)

    products = []
    for i in product_cats:
        products.append(i.product)
    services = []
    for i in service_cats:
        services.append(i.service)
    # items = []
    # for i in service_item_cats:
    #     items.append(i.service_item)

    context = {
        'products' : products,
        'services' : services,
        # 'items' : items,
        'category' : category,
        'title' : f"Search for '{category}'"
    }
    return render(request, 'main/filters/category_detail.html', context)

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
        vendors = Vendor.objects.filter(status="Active")
        final = []
        for i in vendors:
            vendor = {
                'vendor': i.vendor_id,
                'categories': []
            }
            products = Product.objects.filter(vendor=i)
            for j in products:
                cat = ProductCategory.objects.get(product=j)
                if cat.category not in vendor['categories']:
                    vendor['categories'].append(cat.category)
            final.append(vendor)
        context['vendor_cats'] = final[:4]
        context['vendor_cats_end'] = final[4:]
        return context

class VendorDetailView(DetailView):
    model = Vendor
    
    def get_context_data(self, **kwargs):
        context = super(VendorDetailView, self).get_context_data(**kwargs)
        vendor = Vendor.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(vendor=vendor)
        context['products'] = products.order_by('-date_created')
        context['title'] = vendor.store_name
        context['categories'] = Category.objects.all()
        d1 = self.object.date_joined
        d2 = timezone.now()
        months = (d2-d1).days/30
        days = int((months-int(months))*30)
        context['join_date'] = f'{int(months)} months and {days} days ago'
        revs = VendorReview.objects.filter(vendor=self.object)
        if revs:
            context['reviews'] = revs
            context['review_count'] = len(revs)
        if self.object.status == "Inactive":
            context['inactive'] = True

        categories = []
        for j in products:
            cat = ProductCategory.objects.get(product=j)
            if cat.category not in categories:
                categories.append(cat.category)
        context['vendor_cats'] = categories
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
            context['reviews'] = ProductReview.objects.filter(product=self.object)

            if ProductCategory.objects.filter(product=self.object).exists():
                context['category'] = ProductCategory.objects.get(product=self.object)
            
            if self.request.user.is_authenticated:
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
        'title' : f"Prices for '{name}'"
    }
    return render(request, 'main/filters/price_comparison.html', context)

class ProviderListView(ListView):
    model = ServiceProvider
    context_object_name = 'providers'
    paginate_by = 12
    
    def get_context_data(self, **kwargs):
        context = super(ProviderListView, self).get_context_data(**kwargs)
        context['title'] = "Services"
        context['categories'] = Category.objects.all()
        providers = ServiceProvider.objects.all()
        final = []
        for i in providers:
            provider = {
                'provider': i.provider_id,
                'categories': []
            }
            services = Service.objects.filter(provider=i)
            for j in services:
                cat = ServiceCategory.objects.get(service=j)
                if cat.category not in provider['categories']:
                    provider['categories'].append(cat.category)
            final.append(provider)
        context['service_cats'] = final[:4]
        context['service_cats_end'] = final[4:]
        return context

class ProviderDetailView(DetailView):
    model = ServiceProvider

    def get_context_data(self, **kwargs):
        context = super(ProviderDetailView, self).get_context_data(**kwargs)
        provider = ServiceProvider.objects.get(slug=self.kwargs['slug'])
        services = Service.objects.filter(provider=provider)
        items = ServiceItem.objects.filter(provider=provider)
        context['services'] = services.order_by('-date_created')
        context['items'] = items.order_by('-date_created')
        context['title'] = provider.store_name
        context['categories'] = Category.objects.all()
        context['reviews'] = ProviderReview.objects.filter(provider=self.object)

        categories = []
        for j in services:
            cat = ServiceCategory.objects.get(service=j)
            if cat.category not in categories:
                categories.append(cat.category)
        context['service_cats'] = categories
        return context

class ServiceItemDetailView(DetailView):
    model = ServiceItem
    
    def get_context_data(self, **kwargs):
        context = super(ServiceItemDetailView, self).get_context_data(**kwargs)
        context['items'] = ServiceItem.objects.filter(provider=self.object.provider).order_by('-date_created').exclude(item_id=self.object.item_id)
        if ServiceItemCategory.objects.filter(service_item=self.object).exists():
            context['category'] = ServiceItemCategory.objects.get(service_item=self.object)
        context['title'] = self.object.name
        context['categories'] = Category.objects.all()
        return context

class ServiceDetailView(DetailView):
    model = Service
    
    def get_context_data(self, **kwargs):
        context = super(ServiceDetailView, self).get_context_data(**kwargs)
        context['services'] = Service.objects.filter(provider=self.object.provider).order_by('-date_created').exclude(service_id=self.object.service_id)
        if ServiceCategory.objects.filter(service=self.object).exists():
            context['category'] = ServiceCategory.objects.get(service=self.object)
        context['title'] = self.object.name
        context['categories'] = Category.objects.all()
        return context

def VendorProductsListView(request, vendor):
    if Vendor.objects.filter(slug=vendor).exists():
        vendor = Vendor.objects.get(slug=vendor)
        if vendor.status == "Active":
            context = {
                'products' : Product.objects.filter(vendor=vendor),
                'vendor': vendor,
                'title' : f"{vendor.store_name} | All Products",
            }
        else:
            return redirect('home')
    elif ServiceProvider.objects.filter(slug=vendor).exists():
        provider = ServiceProvider.objects.get(slug=vendor)
        context = {
            'services' : Service.objects.filter(provider=provider),
            'items' : ServiceItem.objects.filter(provider=provider),
            'provider': provider,
            'title' : f"{provider.store_name} | All Products",
        }
    return render(request, 'main/filters/vendor_products.html', context)

def VendorCategoryProductsListView(request, vendor, category):
    category = Category.objects.get(name=category)
    if Vendor.objects.filter(slug=vendor).exists():
        vendor = Vendor.objects.get(slug=vendor)
        product_cats = ProductCategory.objects.filter(category=category)
        products = []
        for p in product_cats:
            if p.product.vendor == vendor:
                products.append(p.product)
        context = {
            'products' : products,
            'category' : category,
            'vendor' : vendor,
            'title' : f"Search for '{category}' in {vendor.store_name} ",
        }
    elif ServiceProvider.objects.filter(slug=vendor).exists():
        provider = ServiceProvider.objects.get(slug=vendor)
        service_cats = ServiceCategory.objects.filter(category=category)
        service_item_cats = ServiceItemCategory.objects.filter(category=category)
        services = []
        for i in service_cats:
            if i.service.provider == provider:
                services.append(i.service)
        items = []
        for i in service_item_cats:
            if i.service_item.provider == provider:
                items.append(i.service_item)
        context = {
            'services' : services,
            'items' : items,
            'category' : category,
            'title' : f"Search for '{category}' in {provider.store_name} ",
        }
    return render(request, 'main/vendors/vendor_category.html', context)


@login_required
def AddToWishlist(request):
    p_id = request.GET.get('id')
    p_type = request.GET.get('type')
    if p_type == "product":
        product = Product.objects.get(product_id=p_id)
        if WishlistItem.objects.filter(user=request.user, product=product).exists():
            messages.error(request, 'This item is already in your wishlist!')
        else:
            item = WishlistItem(user=request.user, product=product)
            item.save()
            messages.success(request, 'Item added to wishlist!')
    else:
        service = Service.objects.get(service_id=p_id)
        if WishlistItem.objects.filter(user=request.user, service=service).exists():
            messages.error(request, 'This item is already in your wishlist!')
        else:
            item = WishlistItem(user=request.user, service=service)
            item.save()
            messages.success(request, 'Item added to wishlist')
    return render(request, 'main/user/wishlist/wishlist.html')

@login_required
def WishlistView(request):
    if request.method == "POST":
        data = request.POST
        if data['submit-btn'] == "pdf":
            request.session['note'] = data['w-message']
            return redirect('share-wishlist-pdf')
        else:
            if SharedWishlist.objects.filter(user=request.user).exists():
                s_list = SharedWishlist.objects.get(user=request.user)
                s_list.note = data['w-message']
                s_list.save()
            else:
                n_id = get_wish_ref_id()
                while SharedWishlist.objects.get(ref_id=n_id).exists():
                    n_id = get_wish_ref_id()

                s_list = SharedWishlist(
                        user=request.user, 
                        ref_id=n_id, 
                        note=data['w-message']
                    )
                s_list.save()
            return redirect('share-wishlist', s_list.ref_id)
    context = {
        'title': request.user.username + "'s Wishlist",
        'items': WishlistItem.objects.filter(user=request.user)
    }
    return render(request, 'main/user/wishlist/wishlist.html', context)

class SharedWishlistView(DetailView):
    model = SharedWishlist

    def get_context_data(self, **kwargs):
        context = super(SharedWishlistView, self).get_context_data(**kwargs)
        context['title'] = self.object.user.username + "'s Wishlist"
        context['items'] = WishlistItem.objects.filter(user=self.object.user)
        if self.object.user == self.request.user:
            context['own'] = True
        return context

@login_required
def wishlist_render_pdf_view(request):
    user = User.objects.get(username=request.user)
    items = WishlistItem.objects.filter(user=user)
    context = {
        'items': items,
        'user':user.username
    }
    if 'note' in request.session.keys():
        note = request.session.get('note')
        del request.session['note']
        context.update({'note':note})

    response = HttpResponse(content_type='application/pdf')
    #if download:
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #if display:
    response['Content-Disposition'] = f'filename="{request.user}_wishlist.pdf"'
    template = get_template('main/user/wishlist/user_wishlist.html')
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

class WishlistItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = WishlistItem

    def test_func(self):
        item = WishlistItem.objects.get(id=self.kwargs['pk'])
        return self.request.user == item.user or self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(WishlistItemDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Delete Wishlist Item"
        return context

    def get_success_url(self, **kwargs):
        if self.request.user.groups.filter(name='Admin').exists():
            messages.success(self.request, 'Item has been removed from their wishlist')
            return reverse("user-wishlist", kwargs={'pk':self.kwargs['pk']})
        else:
            messages.success(self.request, 'Item has been removed from your wishlist')
            return reverse('wishlist')

@login_required
def AddToCart(request):
    p_id = request.GET.get('id')
    p_type = request.GET.get('type')
    quantity = request.GET.get('quantity')
    if quantity == None:
        quantity = 1
    else:
        quantity = int(quantity)

    if p_type == "product":
        product = Product.objects.get(product_id=p_id)
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

    elif p_type == "service":
        service = Service.objects.get(service_id=p_id)
        if CartItem.objects.filter(user=request.user, service=service).exists():
            item = CartItem.objects.get(user=request.user, service=service)
            if item.quantity == 5:
                messages.error(request, 'Product cap reached!')
                return render(request, 'main/user/cart/cart.html')
            else:
                temp = item.quantity + quantity
                if temp > 5:
                    item.quantity = 5
                else:
                    item.quantity = temp
                date_added = timezone.now()
        else:
            if quantity > 5:
                quantity = 5
            item = CartItem(user=request.user, service=service, quantity=quantity)
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
        context['title'] = self.request.user.username + "'s Cart"
        vendors = []
        fees = []
        subtotal = decimal.Decimal(0.00)
        total = decimal.Decimal(0.00)
        for i in CartItem.objects.filter(user=self.request.user):
            if i.product:
                if i.product.vendor.vendor_id not in vendors:
                    vendor = Vendor.objects.get(vendor_id=i.product.vendor.vendor_id)
                    if VendorShipping.objects.filter(vendor=vendor).exists():
                        fees.append(VendorShipping.objects.get(vendor=vendor))
                    vendors.append(i.product.vendor.vendor_id)
                subtotal = subtotal + i.product.price
            else:
                subtotal = subtotal + i.service.price
        
        if vendors == []:
            context['s_only'] = True

        if len(vendors) == len(fees):
            context['fees'] = fees
        else:
            messages.error(self.request, 'At least one of the selected vendors have not set a shipping rate.')

        for i in fees:
            total = total + i.rate.rate
        context['subtotal'] = subtotal
        context['total'] = total + subtotal
        return context

class CartItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CartItem
    fields = ['quantity']

    def test_func(self):
        item = CartItem.objects.get(id=self.kwargs['pk'])
        return self.request.user.id == item.user.id

    def get_context_data(self, **kwargs):
        context = super(CartItemUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Edit Cart Item"
        return context
    
    def form_valid(self, form):
        new = form.instance.quantity
        if self.object.product:
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
        else:
            item = CartItem.objects.get(service=self.object.service, user=self.request.user)
            if new == item.quantity:
                return super().form_valid(form)
            elif new > 5:
                messages.error(self.request, 'Maximum of 5 items per product!')
                return self.render_to_response(self.get_context_data(form=form))
            else:
                if item.quantity > new:
                    dec = item.quantity - new
                elif item.quantity < new:
                    add = new - item.quantity 
                form.instance.date_added = timezone.now()
                return super().form_valid(form)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Cart item updated!')
        return reverse("cart")

class CartItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CartItem

    def test_func(self):
        item = CartItem.objects.get(id=self.kwargs['pk'])
        return self.request.user == item.user or self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(CartItemDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Delete Cart Item"
        return context
    
    def delete(self, *args, **kwargs):
        item = CartItem.objects.get(id=self.kwargs['pk'])
        if item.product:
            item = CartItem.objects.get(id=self.kwargs['pk'])
            product.item_stock = product.item_stock + item.quantity
            product.save()
        return super(CartItemDeleteView, self).delete(*args, **kwargs)

    def get_success_url(self, **kwargs):
        if self.request.user.groups.filter(name='Admin').exists():
            messages.success(self.request, 'Item has been removed from their cart')
            item = CartItem.objects.get(id=self.kwargs['pk'])
            return reverse("user-cart", kwargs={'pk':item.user.id})
        else:
            messages.success(self.request, 'Item has been removed from your cart')
            return reverse('cart')

@login_required
def CompeeCaresForm(request):
    items = CartItem.objects.filter(user=request.user,service__isnull=True )
    if items:
        if request.method == "POST":
            for i in request.POST:
                if i != "csrfmiddlewaretoken":
                    item_id = int(i[6:])
                    item = items.get(id=item_id)
                    item.c_cares = True
                    item.save()
                    items = items.exclude(id=item_id)
            for i in items:
                i.c_cares = False
                i.save()
            return redirect('checkout')
            
        context = {
            'title': "Checkout | Compee Cares",
            'items':items
        }

        return render(request, 'main/orders/compee_cares.html', context)
    else:
        return reverse('home')
        
class Checkout(LoginRequiredMixin, CreateView):
    model = SiteOrder
    fields = ['contact_no', 'address_line', 'city', 'state', 'zip_code', 'payment_method']

    def get_context_data(self, **kwargs):
        context = super(Checkout, self).get_context_data(**kwargs)
        context['title'] = "Checkout"
        items = CartItem.objects.filter(user=self.request.user)
        context['items'] = items
        items = items.filter(c_cares=True)
        cc_total = decimal.Decimal(0.00)
        if items:
            cc_total = decimal.Decimal(len(items))* CompeeCaresRate.objects.all().first().rate
            context['cc_total'] = cc_total
            context['cc_count'] = len(items)

        vendors = []
        providers = []
        fees = []
        subtotal = decimal.Decimal(0.00)
        total = decimal.Decimal(0.00)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
        for i in CartItem.objects.filter(user=self.request.user):
            if i.product:
                if i.product.vendor.vendor_id not in vendors:
                    vendor = Vendor.objects.get(vendor_id=i.product.vendor.vendor_id)
                    if VendorShipping.objects.filter(vendor=vendor).exists():
                        fees.append(VendorShipping.objects.get(vendor=vendor))
                    vendors.append(i.product.vendor.vendor_id)
                subtotal = subtotal + i.product.price
            else:
                if i.service.provider.provider_id not in providers:
                    provider = ServiceProvider.objects.get(provider_id=i.service.provider.provider_id)
                    providers.append(i.service.provider.provider_id)
                subtotal = subtotal + i.service.price
        
        if vendors == []:
            context['s_only'] = True
        
        if len(fees) > 1:
            context['multiple'] = True

        if len(vendors) == len(fees):
            context['fees'] = fees
        else:
            messages.error(self.request, 'At least one of the selected vendors have not set a shipping rate.')

        for i in fees:
            total = total + i.rate.rate
        context['subtotal'] = subtotal
        context['total'] = total + subtotal + cc_total
        return context

    def form_valid(self, form):
        items = CartItem.objects.filter(user=self.request.user)
        order_list = []
        service_order_list = []
        for i in items:
            order = {
                'vendor_id': None,
                'items' : [],
                'total' : 0.00
            }
            product = {
                'product_id': None,
                'quantity': 0,
                'c_cares': False
            }
            c_cares = CompeeCaresRate.objects.all().first().rate

            if i.product:
                vendor = i.product.vendor.vendor_id
                if order_list == [] or not any(d['vendor_id'] == vendor for d in order_list):
                    order['vendor_id'] = vendor
                    product['product_id'] = i.product.product_id
                    product['quantity'] = i.quantity
                    product['c_cares'] = i.c_cares
                    order['items'] = [product]
                    if i.c_cares == True:
                        order['total'] = i.product.price * decimal.Decimal(i.quantity) + c_cares
                    else:
                        order['total'] = i.product.price * decimal.Decimal(i.quantity)
                    order_list.append(order)
                else:
                    for d in order_list:
                        if d['vendor_id'] == vendor:
                            product['product_id'] = i.product.product_id
                            product['quantity'] = i.quantity
                            product['c_cares'] = i.c_cares
                            d['items'].append(product)
                            d['total'] = d['total'] + i.product.price * decimal.Decimal(i.quantity)
                            if i.c_cares == True:
                                d['total'] = d['total'] + i.product.price * decimal.Decimal(i.quantity) + c_cares
                            else:
                                d['total'] = d['total'] + i.product.price * decimal.Decimal(i.quantity)
            else:
                provider = i.service.provider.provider_id
                if service_order_list == [] or not any(d['vendor_id'] == provider for d in service_order_list):
                    order['vendor_id'] = provider
                    product['product_id'] = i.service.service_id
                    product['quantity'] = i.quantity
                    order['items'] = [product]
                    order['total'] = i.service.price * decimal.Decimal(i.quantity)
                    service_order_list.append(order)
                else:
                    for d in service_order_list:
                        if d['vendor_id'] == provider:
                            product['product_id'] = i.service.service_id
                            product['quantity'] = i.quantity
                            d['items'].append(product)
                            d['total'] = d['total'] + i.service.price * decimal.Decimal(i.quantity)
        if order_list != []:
            first = True
            for d in order_list:
                vendor = Vendor.objects.get(vendor_id=d['vendor_id'])
                fee = VendorShipping.objects.get(vendor=vendor)
                if first:
                    form.instance.user = self.request.user
                    form.instance.total = d['total'] + fee.rate.rate
                    form.instance.shipping_fee = fee.rate
                    form.instance.ref_id = get_ref_id()
                    if form.instance.payment_method.title != "Cash On Delivery":
                        form.instance.status = "Payment Pending"
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
                        shipping_fee= fee.rate,
                        ref_id = get_ref_id()
                    )
                    if form.instance.payment_method.title != "Cash On Delivery":
                        order.status = "Payment Pending"
                    order.save()

                    for i in d['items']:
                        prod = Product.objects.get(product_id=i['product_id'])
                        item = OrderItem(order=order, product=prod, quantity=i['quantity'], c_cares=i['c_cares'])
                        item.save()
                        c_item = CartItem.objects.get(product=prod, user=self.request.user)
                        c_item.delete()

            for d in service_order_list:
                provider = ServiceProvider.objects.get(provider_id=d['vendor_id'])
                order = SiteOrder(
                    user=self.request.user, 
                    contact_no=form.instance.contact_no,
                    total= d['total'],
                    payment_method= form.instance.payment_method,
                    address_line=form.instance.address_line,
                    city=form.instance.city,
                    state=form.instance.state,
                    zip_code= form.instance.zip_code,
                    ref_id = get_ref_id()
                )
                if form.instance.payment_method.title != "Cash On Delivery":
                    order.status = "Payment Pending"
                order.save()
                for i in d['items']:
                    serv = Service.objects.get(service_id=i['product_id'])
                    item = OrderItem(order=order, service=serv, quantity=i['quantity'], c_cares=i['c_cares'])
                    item.save()
                    c_item = CartItem.objects.get(service=serv, user=self.request.user)
                    c_item.delete()
        else:
            first = True
            for d in service_order_list:
                provider = ServiceProvider.objects.get(provider_id=d['vendor_id'])
                if first:
                    form.instance.user = self.request.user
                    form.instance.total = d['total']
                    form.instance.ref_id = get_ref_id()
                    if form.instance.payment_method.title != "Cash On Delivery":
                        form.instance.status = "Payment Pending"
                    first = False
                else:
                    order = SiteOrder(
                        user=self.request.user, 
                        contact_no=form.instance.contact_no,
                        total= d['total'],
                        payment_method= form.instance.payment_method,
                        address_line=form.instance.address_line,
                        city=form.instance.city,
                        state=form.instance.state,
                        zip_code= form.instance.zip_code,
                        ref_id = get_ref_id()
                    )
                    if form.instance.payment_method.title != "Cash On Delivery":
                        order.status = "Payment Pending"
                    order.save()

                    for i in d['items']:
                        serv = Service.objects.get(service_id=i['product_id'])
                        item = OrderItem(order=order, service=serv, quantity=i['quantity'],c_cares=i['c_cares'])
                        item.save()
                        c_item = CartItem.objects.get(serivce=serv, user=self.request.user)
                        c_item.delete()

        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        items = CartItem.objects.filter(user=self.request.user)
        for i in items:
            if i.product:
                item = OrderItem(order=self.object, product=i.product, quantity=i.quantity,c_cares=i.c_cares)
            else:
                item = OrderItem(order=self.object, service=i.service, quantity=i.quantity)
            item.save()
            i.delete()
        if self.object.payment_method.title == "Paypal or Debit/Credit Card":
            return reverse("credit-payment", kwargs={'pk':self.object.ref_id})
        elif self.object.payment_method.title == "Cash on Delivery":
            messages.success(self.request, 'Your order has been received!')
            return reverse("my-orders")
        else:
            return reverse("other-payment", kwargs={'pk':self.object.ref_id})

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

class OrderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = SiteOrder

    def test_func(self):
        order = SiteOrder.objects.get(order_id = self.kwargs['pk'])
        return order.user == self.request.user
    
    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Order Details'
        items = OrderItem.objects.filter(order=self.object)
        context['items'] = items
        if items.filter(c_cares=True).exists():
            context['cares'] = True
            d1 = self.object.date_placed
            d2 = timezone.now()
            context['days'] = abs((d2-d1).days)
        return context

@login_required
def RequestRenewal(request,pk):
    order = SiteOrder.objects.get(ref_id=pk)
    if order.user == request.user:
        if request.method == "POST":
            form = RenewalForm(order,request.POST)
            if form.is_valid():
                form.instance.order = order
                form.save()
                messages.success(request, 'Your request for renewal has been sent.')
                return redirect('home')
        else:
            form = RenewalForm(order)

        context={
            'title':'Request Renewal',
            'form':form
        }
        return render(request, 'main/orders/cc_renewal.html', context)
    else:
        return reverse('home')

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
            if i.product:
                product = Product.objects.get(product_id=i.product.product_id)
                product.quantity = product.item_stock + i.quantity
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
                'title':'Add Review',
                'order':order,
                'items':items,
            }
            if items[0].product:
                vendor = VendorReview.objects.filter(author=request.user, vendor=items[0].product.vendor)
                if vendor:
                    context.update({'v_review':vendor.first()})
            else:
                context.update({'is_service':True})
                provider = ProviderReview.objects.filter(author=request.user, provider=items[0].service.provider)
                if provider:
                    context.update({'p_review':provider.first()})
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

class ProviderReviewCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ProviderReview
    fields = ['rating', 'description']

    def test_func(self):
        order = SiteOrder.objects.get(order_id = self.kwargs['pk'])
        return order.user.id == self.request.user.id

    def get_context_data(self, **kwargs):
        context = super(ProviderReviewCreateView, self).get_context_data(**kwargs)
        context['title'] = "Provider Review"
        context['provider'] = True
        order = SiteOrder.objects.get(order_id=self.kwargs['pk'])
        if order.status == "Received":
            context['received'] = True
        item = OrderItem.objects.filter(order=order).first()
        if ProviderReview.objects.filter(author=self.request.user, provider=item.service.provider).exists():
            context['review'] = ProviderReview.objects.get(author=self.request.user, provider=item.service.provider)
        context['order'] = order
        return context

    def form_valid(self, form):
        order = SiteOrder.objects.get(order_id = self.kwargs['pk'])
        if order.status == "Received":
            item = OrderItem.objects.filter(order=order).first()
            provider = item.service.provider
            if ProviderReview.objects.filter(author=self.request.user, provider=provider).exists():
                messages.error(request, 'Provider review already exists!')
                return redirect('home')
            else:
                form.instance.author = self.request.user
                form.instance.provider = provider
                form.instance.order = order
                return super().form_valid(form)
        else:
            messages.error(request, 'This order has not yet been received!')
            return redirect('home')
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Provider review added!')
        return reverse("provider-detail-main", kwargs={'slug':self.object.provider.slug})

class ProviderReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ProviderReview
    fields = ['rating', 'description']

    def test_func(self):
        review = ProviderReview.objects.get(review_id=self.kwargs['pk'])
        return review.author.id == self.request.user.id or self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(ProviderReviewUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Edit Provider Review"
        context['provider'] = True
        return context
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Review updated!')
        return reverse("provider-detail-main", kwargs={'slug':self.object.provider.slug})

class ProviderReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProviderReview

    def test_func(self):
        review = ProviderReview.objects.get(review_id=self.kwargs['pk'])
        return review.author.id == self.request.user.id or self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(ProviderReviewDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Delete Provider Review"
        context['provider'] = True
        return context

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Provider review has been deleted')
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
        context['product'] = Product.objects.get(product_id=self.kwargs['pk'])
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

class ServiceReviewCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ServiceReview
    fields = ['rating', 'description']

    def test_func(self):
        order = SiteOrder.objects.get(order_id = self.kwargs['order_pk'])
        return order.user.id == self.request.user.id

    def get_context_data(self, **kwargs):
        context = super(ServiceReviewCreateView, self).get_context_data(**kwargs)
        context['title'] = "Service Review"
        order = SiteOrder.objects.get(order_id=self.kwargs['order_pk'])
        context['service'] = Service.objects.get(order_id=self.kwargs['pk'])
        if order.status == "Received":
            context['received'] = True
        if ServiceReview.objects.filter(author=self.request.user, service_id=self.kwargs['pk']).exists():
            context['review'] = ServiceReview.objects.get(author=self.request.user, service_id=self.kwargs['pk'])
        context['order'] = order
        return context

    def form_valid(self, form):
        order = SiteOrder.objects.get(order_id = self.kwargs['order_pk'])
        if order.status == "Received":
            service = Service.objects.get(service_id=self.kwargs['pk'])
            if ServiceReview.objects.filter(author=self.request.user, service=service).exists():
                messages.error(request, 'Service review already exists!')
                return redirect('home')
            else:
                form.instance.author = self.request.user
                form.instance.service = service
                form.instance.order = order
                return super().form_valid(form)
        else:
            messages.error(request, 'This order has not yet been received!')
            return redirect('home')
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Service review added!')
        return reverse("service-product", kwargs={'slug':self.object.service.slug})

class ServiceReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ServiceReview
    fields = ['rating', 'description']

    def test_func(self):
        review = ServiceReview.objects.get(review_id=self.kwargs['pk'])
        return review.author.id == self.request.user.id or self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(ServiceReviewUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Edit Service Review"
        context['service'] = True
        return context
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Review updated!')
        return reverse("service-product", kwargs={'slug':self.object.service.slug})

class ServiceReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ServiceReview

    def test_func(self):
        review = ServiceReview.objects.get(review_id=self.kwargs['pk'])
        return review.author.id == self.request.user.id or self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(ServiceReviewDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Delete Service Review"
        context['service'] = True
        return context

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Service review has been deleted')
        return reverse('home')




    

    

    