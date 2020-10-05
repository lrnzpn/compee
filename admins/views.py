import decimal
from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.models import User, Group
from main.models import SiteOrder, OrderItem, WishlistItem, CartItem, PaymentMethod
from users.models import Vendor, ServiceProvider, VendorReview, ProviderReview
from .models import (
    Product, ServiceItem, Service, Category, ProductCategory, ServiceCategory, ServiceItemCategory,
    ProductReview, ServiceReview, ShippingRate, VendorShipping)
from .forms import (
    ProductCreateForm, AssignCategoryForm, ServiceCreateForm, AssignServiceCategoryForm,
    ServiceItemCreateForm, AssignItemCategoryForm
)
from users.forms import VendorUpdateForm, ProviderCreateForm, AdminForm
from .funcs import unique_product_slug_generator, unique_store_slug_generator, updateVendorStatus

class ProviderListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ServiceProvider
    context_object_name = 'providers'
    paginate_by = 9

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(ProviderListView, self).get_context_data(**kwargs)
        context['title'] = "Dashboard | Services"
        return context

class ProviderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ServiceProvider

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(ProviderDetailView, self).get_context_data(**kwargs)
        context['services'] = Service.objects.filter(provider=self.object).order_by('-date_created')
        context['items'] = ServiceItem.objects.filter(provider=self.object).order_by('-date_created')
        provider = ServiceProvider.objects.get(provider_id=self.kwargs['pk'])
        context['title'] = provider.store_name
        context['reviews'] = ProviderReview.objects.filter(provider=self.object)
        return context

class ProviderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ServiceProvider
    fields = ['store_name', 'provider_info', 'address_line', 'city', 'state', 
                'zip_code', 'contact_no', 'secondary_no', 'image']

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(ProviderUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Provider Edit"
        return context

    def form_valid(self, form):
        form.instance.slug = unique_store_slug_generator(form.instance)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Service Provider information updated!')
        return reverse("provider-detail", kwargs={'pk': self.object.pk})

    
class ProviderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ServiceProvider

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(ProviderDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Provider Delete"
        return context

    def delete(self, *args, **kwargs):
        provider = ServiceProvider.objects.get(provider_id = self.kwargs['pk'])
        user = User.objects.get(id = provider.user.id)
        v_group = Group.objects.get(name='Provider')
        v_group.user_set.remove(user)
        return super(ProviderDeleteView, self).delete(*args, **kwargs)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Service Provider has been removed.')
        return reverse('providers')

class VendorListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Vendor
    context_object_name = 'vendors'
    paginate_by = 9

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(VendorListView, self).get_context_data(**kwargs)
        status = updateVendorStatus()
        if status:
            context['reminder'] = "There are vendors that have not been assigned to a shipping rate."
        context['title'] = "Dashboard | Vendor"
        return context

class VendorDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Vendor

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(VendorDetailView, self).get_context_data(**kwargs)
        vendor = Vendor.objects.get(vendor_id=self.kwargs['pk'])
        context['products'] = Product.objects.filter(vendor=vendor).order_by('-date_created')
        context['title'] = vendor.store_name
        context['reviews'] = VendorReview.objects.filter(vendor=self.object)
        return context

class VendorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vendor
    fields = ['store_name', 'store_info', 'address_line', 'city', 'state', 
                'zip_code', 'contact_no', 'secondary_no', 'image', 'user', 'status']

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(VendorUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Vendor Edit"
        return context

    def form_valid(self, form):
        form.instance.slug = unique_store_slug_generator(form.instance)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Vendor information updated!')
        return reverse("vendor-detail", kwargs={'pk': self.object.pk})

    
class VendorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vendor

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(VendorDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Vendor Delete"
        return context

    def delete(self, *args, **kwargs):
        vendor = Vendor.objects.get(vendor_id = self.kwargs['pk'])
        user = User.objects.get(id = vendor.user.id)
        v_group = Group.objects.get(name='Vendor')
        v_group.user_set.remove(user)
        return super(VendorDeleteView, self).delete(*args, **kwargs)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Vendor has been removed.')
        return reverse('vendors')

@login_required
def ProductCreateView(request, pk=None):
    if request.user.groups.filter(name='Admin').exists():
        if request.method == "POST":
            p_form = ProductCreateForm(request.POST)
            c_form = AssignCategoryForm(request.POST)

            if p_form.is_valid() and c_form.is_valid():
                vendor = Vendor.objects.get(vendor_id=pk)
                new_prod = p_form.save(commit=False)
                new_prod.vendor = vendor
                new_prod.slug = unique_product_slug_generator(new_prod)
                new_prod.save()
                p_form.save_m2m()
                c_form.instance.product = new_prod
                c_form.save()

                messages.success(request, 'New product has been added.')
                return redirect('product-detail', new_prod.slug)
        else:
            p_form = ProductCreateForm()
            c_form = AssignCategoryForm()
        
        context = {
            'p_form': p_form,
            'c_form': c_form,
            'title':'New Product',
        }

        return render(request, 'admins/vendors/products/product_form.html', context)
    else:
        return redirect('home')

class ProductDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Product

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        temp = Product.objects.filter(vendor=self.object.vendor).order_by('-date_created')
        context['products'] = Product.objects.filter(vendor=self.object.vendor).order_by('-date_created').exclude(product_id=self.object.product_id)
        if ProductCategory.objects.get(product=self.object):
            context['category'] = ProductCategory.objects.get(product=self.object)
        context['title'] = self.object.name
        context['reviews'] = ProductReview.objects.filter(product=self.object)
        return context

@login_required
def ProductUpdateView(request, pk=None):
    if request.user.groups.filter(name='Admin').exists():
        product = Product.objects.get(product_id=pk)
        category = ProductCategory.objects.get(product=product)
        if request.method == "POST":
            p_form = ProductCreateForm(request.POST, instance=product)
            c_form = AssignCategoryForm(request.POST, instance=category)

            if p_form.is_valid() and c_form.is_valid():
                p_form.instance.slug = unique_product_slug_generator(p_form.instance)
                new_prod = p_form.save()
                c_form.save()
                messages.success(request, 'Product has been updated.')
                return redirect('product-detail', new_prod.slug)
        else:
            p_form = ProductCreateForm(instance=product)
            c_form = AssignCategoryForm(instance=category)
        
        context = {
            'p_form': p_form,
            'c_form': c_form,
            'title':'Update Product',
        }

        return render(request, 'admins/vendors/products/product_update.html', context)
    else:
        return redirect('home')

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(ProductDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Product Delete"
        return context

    def form_valid(self, form):
        pt = ProductCategory.objects.get(product = self.object)
        if pt:
            for i in pt:
                i.delete()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Product has been deleted.')
        return reverse('vendors')

@login_required
def ServiceItemCreateView(request, pk=None):
    provider = ServiceProvider.objects.get(provider_id=pk)
    if request.user.groups.filter(name='Admin').exists():
        if request.method == "POST":
            i_form = ServiceItemCreateForm(request.POST)
            c_form = AssignItemCategoryForm(request.POST)

            if i_form.is_valid() and c_form.is_valid():
                new_prod = i_form.save(commit=False)
                new_prod.provider = provider
                new_prod.slug = unique_product_slug_generator(new_prod)
                new_prod.save()
                i_form.save_m2m()
                c_form.instance.service_item = new_prod
                c_form.save()

                messages.success(request, 'New service item has been added.')
                return redirect('service-item-detail', new_prod.slug)
        else:
            i_form = ServiceItemCreateForm()
            c_form = AssignItemCategoryForm()
        
        context = {
            'i_form': i_form,
            'c_form': c_form,
            'title':'New Service Item',
        }
        return render(request, 'admins/providers/items/service_item_form.html', context)
    else:
        return redirect('home')


class ServiceItemDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ServiceItem

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(ServiceItemDetailView, self).get_context_data(**kwargs)
        context['items'] = ServiceItem.objects.filter(provider=self.object.provider).order_by('-date_created').exclude(item_id=self.object.item_id)
        if ServiceItemCategory.objects.get(service_item=self.object):
            context['category'] = ServiceItemCategory.objects.get(service_item=self.object)
        context['title'] = self.object.name
        return context

@login_required
def ServiceItemUpdateView(request, pk=None):
    if request.user.groups.filter(name='Admin').exists():
        item = ServiceItem.objects.get(item_id=pk)
        category = ServiceItemCategory.objects.get(service_item=item)
        if request.method == "POST":
            i_form = ServiceItemCreateForm(request.POST, instance=item)
            c_form = AssignItemCategoryForm(request.POST, instance=category)

            if i_form.is_valid() and c_form.is_valid():
                i_form.instance.slug = unique_product_slug_generator(i_form.instance)
                new_prod = i_form.save()
                c_form.save()
                messages.success(request, 'Service Item has been updated.')
                return redirect('service-item-detail', new_prod.slug)
        else:
            i_form = ServiceItemCreateForm(instance=item)
            c_form = AssignItemCategoryForm(instance=category)
        
        context = {
            'i_form': i_form,
            'c_form': c_form,
            'title':'Update Service Item',
        }
        return render(request, 'admins/providers/items/service_item_update.html', context)
    else:
        return redirect('home')

class ServiceItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ServiceItem

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(ServiceItemDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Item Delete"
        return context

    def form_valid(self, form):
        ic = ServiceItemCategory.objects.get(service_item = self.object)
        if ic:
            for i in ic:
                i.delete()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Service item has been deleted.')
        return reverse('providers')

@login_required
def ServiceCreateView(request, pk=None):
    provider = ServiceProvider.objects.get(provider_id=pk)
    if request.user.groups.filter(name='Admin').exists():
        if request.method == "POST":
            s_form = ServiceCreateForm(request.POST)
            c_form = AssignServiceCategoryForm(request.POST)

            if s_form.is_valid() and c_form.is_valid():
                new_prod = s_form.save(commit=False)
                new_prod.provider = provider
                new_prod.slug = unique_product_slug_generator(new_prod)
                new_prod.save()
                s_form.save_m2m()
                c_form.instance.service = new_prod
                c_form.save()

                messages.success(request, 'New service has been added.')
                return redirect('service-detail', new_prod.slug)
        else:
            s_form = ServiceCreateForm()
            c_form = AssignServiceCategoryForm()
        
        context = {
            's_form': s_form,
            'c_form': c_form,
            'title':'New Service',
        }
        return render(request, 'admins/providers/services/service_form.html', context)
    else:
        return redirect('home')


class ServiceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Service

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(ServiceDetailView, self).get_context_data(**kwargs)
        context['services'] = Service.objects.filter(provider=self.object.provider).order_by('-date_created').exclude(service_id=self.object.service_id)
        if ServiceCategory.objects.get(service=self.object):
            context['category'] = ServiceCategory.objects.get(service=self.object)
        context['title'] = self.object.name
        return context

@login_required
def ServiceUpdateView(request, pk=None):
    if request.user.groups.filter(name='Admin').exists():
        service = Service.objects.get(service_id=pk)
        category = ServiceCategory.objects.get(service=service)
        if request.method == "POST":
            s_form = ServiceCreateForm(request.POST, instance=service)
            c_form = AssignServiceCategoryForm(request.POST, instance=category)

            if s_form.is_valid() and c_form.is_valid():
                s_form.instance.slug = unique_product_slug_generator(s_form.instance)
                new_prod = s_form.save()
                c_form.save()
                messages.success(request, 'Service has been updated.')
                return redirect('service-detail', new_prod.slug)
        else:
            s_form = ServiceCreateForm(instance=service)
            c_form = AssignServiceCategoryForm(instance=category)
        
        context = {
            's_form': s_form,
            'c_form': c_form,
            'title':'Update Service',
        }
        return render(request, 'admins/providers/services/service_update.html', context)
    else:
        return redirect('home')

class ServiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Service

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(ServiceDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Service Delete"
        return context

    def form_valid(self, form):
        sc = ServiceCategory.objects.get(service = self.object)
        if sc:
            for i in sc:
                i.delete()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Service has been deleted.')
        return reverse('providers')

class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    context_object_name = 'users'
    paginate_by = 15

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = "Dashboard | Users"
        return context

#users table functions
class VendorCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Vendor
    form_class = VendorUpdateForm

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(VendorCreateView, self).get_context_data(**kwargs)
        context['title'] = "New Store"
        return context

    def form_valid(self, form):
        user = User.objects.get(id = self.kwargs['pk'])
        form.instance.user = user
        form.instance.slug = unique_store_slug_generator(form.instance)
        v_group = Group.objects.get(name='Vendor')
        v_group.user_set.add(user)
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Store created!')
        return reverse("vendor-detail",  kwargs={'pk': self.object.pk})

class ProviderCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ServiceProvider
    form_class = ProviderCreateForm

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(ProviderCreateView, self).get_context_data(**kwargs)
        context['title'] = "New Service Store"
        return context

    def form_valid(self, form):
        user = User.objects.get(id = self.kwargs['pk'])
        form.instance.user = user
        form.instance.slug = unique_store_slug_generator(form.instance)
        v_group = Group.objects.get(name='Provider')
        v_group.user_set.add(user)
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Service Store created!')
        return reverse("provider-detail",  kwargs={'pk': self.object.pk})

@login_required
def GiveAdmin(request,pk):
    if request.user.groups.filter(name='Admin').exists():
        user = User.objects.get(id = pk)
        if request.method == "POST":
            form = AdminForm(request.POST, instance=user)
            if form.is_valid():
                group = Group.objects.get(name='Admin')
                group.user_set.add(user)
                form.save()
                messages.success(request, f'{user.username} is now a site admin')
                return redirect('users')
        else:
            form = AdminForm(request.POST)

        context = {
            'form': form,
            'title': 'Give Admin',
            'user' : user
        }
        return render(request, 'admins/users/roles/make_admin.html', context)
    else:
        return redirect('home')

@login_required
def RemoveAdmin(request,pk):
    if request.user.groups.filter(name='Admin').exists():
        user = User.objects.get(id = pk)
        if request.method == "POST":
            form = AdminForm(request.POST, instance=user)
            if form.is_valid():
                group = Group.objects.get(name='Admin')
                group.user_set.remove(user)
                form.save()
                messages.success(request, f'{user.username} is no longer a site admin')
                return redirect('users')
        else:
            form = AdminForm(request.POST)

        context = {
            'form': form,
            'title': 'Remove Admin',
            'user' : user
        }
        return render(request, 'admins/users/roles/remove_admin.html', context)
    else:
        return redirect('home')

class WishlistView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = WishlistItem
    context_object_name = 'items'
    paginate_by = 6

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['pk'])
        return WishlistItem.objects.filter(user=user)

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(WishlistView, self).get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['pk'])
        context['user'] = user
        context['title'] = user.username + "'s Wishlist"
        return context

class CartView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CartItem
    context_object_name = 'items'
    paginate_by = 6

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['pk'])
        return CartItem.objects.filter(user=user)
    
    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['pk'])
        context['user'] = user
        context['title'] = user.username + "'s Cart"
        return context

def get_sort_orders(request):
    option = request.GET.get('option')
    if option == 'a':
        context = {'orders': SiteOrder.objects.all().order_by('-date_placed') }
    elif option == 'u':
        context = {'orders': SiteOrder.objects.filter(status="Unfulfilled").order_by('-date_placed')  }
    elif option == 'p':
        context = {'orders': SiteOrder.objects.filter(status="Payment Pending").order_by('-date_placed')  }
    elif option == 'o':
        context = {'orders': SiteOrder.objects.filter( Q(status="Unfulfilled") | Q(status="Payment Pending") | Q(status="Shipped") ).order_by('-date_placed') }
    elif option == 'c':
        context = {'orders': SiteOrder.objects.filter( Q(status="Received") | Q(status="Cancelled") ).order_by('-date_placed') }
    return render(request, 'admins/orders/orders.html', context)

class OrderListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = SiteOrder
    context_object_name = 'orders'
    paginate_by = 6

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['title'] = "Dashboard | Orders"
        return context

class OrderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = SiteOrder

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = "Dashboard | Order"
        context['items'] = OrderItem.objects.filter(order=self.object)
        open_status = ['Unfulfilled', 'Payment Pending']
        if self.object.status in open_status:
            context['is_open'] = True
        return context

class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SiteOrder
    fields = ['status', 'contact_no', 'address_line', 'city', 'state', 'zip_code', 'payment_method', 'shipping_fee']

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Order Edit"
        return context

    def form_valid(self, form):
        order = SiteOrder.objects.get(order_id=self.object.order_id)
        item = OrderItem.objects.get(order=order)
        if item.product:
            form.instance.total = form.instance.total - order.shipping_fee.rate
            form.instance.total = form.instance.total + form.instance.shipping_fee.rate
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Order information updated!')
        return reverse("order-detail", kwargs={'pk': self.object.pk})

class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SiteOrder

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(OrderDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Delete Order"
        return context

    def delete(self, *args, **kwargs):
        order = SiteOrder.objects.get(order_id=self.kwargs['pk'])
        open_status = ['Unfulfilled', 'Payment Pending', 'Shipped']
        if order.status in open_status:
            items = OrderItem.objects.filter(order=order)
            for i in items:
                if i.product:
                    prod = Product.objects.get(product_id=i.product.product_id)
                    prod.item_stock = prod.item_stock + i.quantity
                    prod.save()
                i.delete()
        return super(OrderDeleteView, self).delete(*args, **kwargs)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Order has been deleted.')
        return reverse('orders')

class OrderItemCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = OrderItem
    fields = ['product', 'quantity']

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(OrderItemCreateView, self).get_context_data(**kwargs)
        context['title'] = "Dashboard | Edit Order Items"
        context['items'] = OrderItem.objects.filter(order_id=self.kwargs['pk'])
        order = SiteOrder.objects.get(order_id=self.kwargs['pk'])
        context['order'] = order
        open_status = ['Unfulfilled', 'Payment Pending']
        if order.status in open_status:
            context['is_open'] = True
        return context

    def form_valid(self, form):
        order = SiteOrder.objects.get(order_id=self.kwargs['pk'])
        if OrderItem.objects.filter(product=form.instance.product, order=order).exists():
            messages.error(self.request,'This product has already been added!')
            return self.render_to_response(self.get_context_data(form=form))
        else:
            form.instance.order = order
            quantity = form.instance.quantity
            prod = Product.objects.get(product_id=form.instance.product.product_id)
            if prod.item_stock >= quantity:
                if quantity > 5:
                    messages.error(self.request,'Maximum of 5 items per product!')
                    return self.render_to_response(self.get_context_data(form=form))
                elif quantity < 1:
                    messages.error(self.request,'Please add at least 1 item of the selected product!')
                    return self.render_to_response(self.get_context_data(form=form))
                else:
                    prod.item_stock = prod.item_stock-quantity
                    prod.save()
                    order.total = order.total + prod.price * decimal.Decimal(quantity)
                    order.save()
                    return super().form_valid(form)
            else:
                messages.error(self.request,'This product does not have enough in stock!')
                return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Product has been added!')
        return reverse("order-update-items", kwargs={'pk': self.kwargs['pk']})

class OrderItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = OrderItem
    fields = ['quantity']

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(OrderItemUpdateView, self).get_context_data(**kwargs)
        context['title'] =  "Dashboard | Edit Order Items"
        open_status = ['Unfulfilled', 'Payment Pending']
        if self.object.order.status in open_status:
            context['is_open'] = True
        return context

    def form_valid(self, form):
        closed_status = ['Shipped', 'Received', 'Cancelled']
        if self.object.order.status in closed_status:
            messages.error(self.request, 'You can no longer update items from closed orders!')
            return self.render_to_response(self.get_context_data(form=form))
        else:
            new = form.instance.quantity
            item = OrderItem.objects.get(id=self.object.id)
            order = item.order
            if new == item.quantity:
                return super().form_valid(form)
            elif new > 5:
                messages.error(self.request, 'Maximum of 5 items per product!')
                return self.render_to_response(self.get_context_data(form=form))
            else:
                if self.object.product:
                    product = Product.objects.get(product_id=self.object.product.product_id)
                    if item.quantity > new:
                        dec = item.quantity - new
                        product.item_stock = product.item_stock + dec
                        product.save()
                        order.total = order.total - product.price * decimal.Decimal(dec)
                        order.save()
                        return super().form_valid(form)
                    elif item.quantity < new:
                        add = new - item.quantity
                        if product.item_stock < add:
                            messages.error(self.request, 'This product does not have enough items in stock!')
                            return self.render_to_response(self.get_context_data(form=form))
                        else:
                            product.item_stock = product.item_stock - add
                            product.save()
                            order.total = order.total + product.price * decimal.Decimal(add)
                            order.save()
                            return super().form_valid(form)
                else:
                    service = Service.objects.get(service_id=self.object.service.service_id)
                    if item.quantity > new:
                        dec = item.quantity - new
                        order.total = order.total - service.price * decimal.Decimal(dec)
                        order.save()
                        return super().form_valid(form)
                    elif item.quantity < new:
                        add = new - item.quantity
                        order.total = order.total + service.price * decimal.Decimal(add)
                        order.save()
                        return super().form_valid(form)
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Product quantity updated!')
        return reverse("order-update-items", kwargs={'pk': self.object.order.order_id})

class OrderItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = OrderItem

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(OrderItemDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Dashboard | Delete Item"
        return context

    def delete(self, *args, **kwargs):
        closed_status = ['Shipped', 'Received', 'Cancelled']
        item = OrderItem.objects.get(id=self.kwargs['pk'])
        order = SiteOrder.objects.get(order_id=item.order.order_id)
        if order in closed_status:
            messages.error(self.request, 'You can no longer update items from closed orders!')
            return redirect('orders')
        else:
            item = OrderItem.objects.get(id=self.kwargs['pk'])
            if item.product:
                prod = Product.objects.get(product_id=item.product.product_id)
                prod.item_stock = prod.item_stock + item.quantity
                prod.save()
            else:
                prod = Service.objects.get(service_id=item.service.service_id)
            order.total = order.total - prod.price * decimal.Decimal(item.quantity)
            order.save()
            return super(OrderItemDeleteView, self).delete(*args, **kwargs)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Order item has been deleted.')
        item = OrderItem.objects.get(id=self.kwargs['pk'])
        return reverse('order-detail', kwargs={'pk':item.order.order_id})

def Settings(request):
    return render(request, 'admins/settings/settings.html', {'title':"Settings | Dashboard"})

class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    fields = ['name']

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = "New Category"
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        if Category.objects.filter(name=form.cleaned_data['name']).exists():
            messages.error(self.request,'This category already exists!')
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Category created!')
        return reverse("category-create")

class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['name']

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Update Category"
        return context

    def form_valid(self, form):
        category = Category.objects.get(name=form.cleaned_data['name'])
        if category and category != self.object:
            messages.error(self.request,'This category already exists!')
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Category updated!')
        return reverse("category-create")

class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(CategoryDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Category Delete"
        return context

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Category has been deleted.')
        return reverse('category-create')

class PaymentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = PaymentMethod
    fields = ['title', 'details']

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(PaymentCreateView, self).get_context_data(**kwargs)
        context['title'] = "Edit Payment Methods"
        context['payments'] = PaymentMethod.objects.all()
        return context

    def form_valid(self, form):
        if PaymentMethod.objects.filter(title=form.cleaned_data['title']).exists():
            messages.error(self.request,'This payment method already exists!')
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Payment method added!')
        return reverse("payment-methods")

class PaymentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PaymentMethod
    fields = ['title', 'details']

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(PaymentUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Update Payment Method"
        return context

    def form_valid(self, form):
        payment = PaymentMethod.objects.filter(title=form.cleaned_data['title'])
        if payment and payment != self.object:
            messages.error(self.request,'This payment method already exists!')
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Payment method updated!')
        return reverse("payment-methods")

class PaymentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PaymentMethod

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(PaymentDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Delete Payment Method"
        return context

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Payment method has been deleted.')
        return reverse('payment-methods')

class ShippingRateCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ShippingRate
    fields = ['name', 'rate']

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(ShippingRateCreateView, self).get_context_data(**kwargs)
        context['title'] = "Edit Shipping Rates"
        context['rates'] = ShippingRate.objects.all()
        vendors = Vendor.objects.all()
        for v in vendors:
            if VendorShipping.objects.filter(vendor=v).exists():
                vendors = vendors.exclude(vendor_id=v.vendor_id)
        context['u_vendors'] = vendors
        return context

    def form_valid(self, form):
        if ShippingRate.objects.filter(name=form.cleaned_data['name'], rate=form.cleaned_data['rate']).exists():
            messages.error(self.request,'This shipping rate already exists!')
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Shipping rate added!')
        return reverse("shipping-rates")

class ShippingRateUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ShippingRate
    fields = ['name','rate']

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(ShippingRateUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Update Shipping Rate"
        return context

    def form_valid(self, form):
        rate = ShippingRate.objects.get(name=form.cleaned_data['name'], rate=form.cleaned_data['rate'])
        if rate and rate != self.object:
            messages.error(self.request,'This shipping rate already exists!')
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Shipping rate updated!')
        return reverse("shipping-rates")

class ShippingRateDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ShippingRate

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(ShippingRateDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Delete Shipping Rate"
        return context

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Shipping rate has been deleted.')
        return reverse('shipping-rates')

class ShippingVendorsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = VendorShipping
    context_object_name = 'r_vendors'
    paginate_by = 6

    def get_queryset(self):
        rate = ShippingRate.objects.get(id=self.kwargs['pk'])
        return VendorShipping.objects.filter(rate=rate)

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(ShippingVendorsListView, self).get_context_data(**kwargs)
        context['title'] = "Shipping Rate Vendors | Dashboard"
        rate = ShippingRate.objects.get(id=self.kwargs['pk'])
        context['rate'] = rate
        r_vendors = VendorShipping.objects.filter(rate=rate)
        vendors = Vendor.objects.all()
        for i in r_vendors:
            vendors = vendors.exclude(vendor_id=i.vendor.vendor_id)
        for i in vendors:
            if VendorShipping.objects.filter(vendor=i).exists():
                vendors = vendors.exclude(vendor_id=i.vendor_id)
        context['vendors'] = vendors
        return context

class AssignVendortoRate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = VendorShipping
    fields = []
    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(AssignVendortoRate, self).get_context_data(**kwargs)
        context['title'] = "Add Vendor to Rate"
        context['rate'] = ShippingRate.objects.get(id=self.kwargs['pk'])
        context['vendor'] = Vendor.objects.get(vendor_id=self.kwargs['vendor_pk'])
        return context

    def form_valid(self, form):
        vendor = Vendor.objects.get(vendor_id=self.kwargs['vendor_pk'])
        rate = ShippingRate.objects.get(id=self.kwargs['pk'])
        if VendorShipping.objects.filter(vendor=vendor).exists():
            messages.error(self.request,'This vendor is already assigned to a rate!')
            return self.render_to_response(self.get_context_data(form=form))
        else:
            form.instance.vendor = vendor
            form.instance.rate = rate
            return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Vendor added to rate!')
        return reverse("rate-vendors", kwargs={'pk': self.object.rate.id} )

class ShippingVendorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = VendorShipping

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(ShippingVendorDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Remove Vendor from Rate"
        return context

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'This vendor will no longer use this rate.')
        return reverse('rate-vendors',kwargs={'pk':self.kwargs['rate_pk']})