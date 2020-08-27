import decimal
from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)

from django.contrib.auth.models import User, Group
from main.models import SiteOrder, OrderItem, WishlistItem, CartItem
from users.models import Vendor, Buyer, VendorReview
from .models import Product, Category, ProductCategory, BuyerProduct, BuyerProductCategory, ProductReview

from .forms import ProductCreateForm, AssignCategoryForm, BuyerProductCreateForm, AssignBuyerCategoryForm
from users.forms import VendorUpdateForm, BuyerCreateForm, AdminForm


class BuyerListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Buyer
    context_object_name = 'buyers'
    paginate_by = 6

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(BuyerListView, self).get_context_data(**kwargs)
        context['title'] = "Dashboard | Buyer"
        return context

class BuyerDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Buyer

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(BuyerDetailView, self).get_context_data(**kwargs)
        context['products'] = BuyerProduct.objects.filter(buyer=self.object).order_by('-date_created')
        buyer = Buyer.objects.get(buyer_id=self.kwargs['pk'])
        context['title'] = buyer.store_name
        context['is_seller'] = False
        return context

class BuyerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Buyer
    fields = ['store_name', 'store_info', 'address_line', 'city', 'state', 
                'zip_code', 'contact_no', 'secondary_no', 'image', 'user']

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(BuyerUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Buyer Edit"
        return context

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.store_name)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Buyer information updated!')
        return reverse("buyer-detail", kwargs={'pk': self.object.pk})

    
class BuyerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Buyer

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(BuyerDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Buyer Delete"
        return context

    def delete(self, *args, **kwargs):
        buyer = Buyer.objects.get(buyer_id = self.kwargs['pk'])
        user = User.objects.get(id = buyer.user.id)
        v_group = Group.objects.get(name='Buyer')
        v_group.user_set.remove(user)
        return super(BuyerDeleteView, self).delete(*args, **kwargs)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Buyer has been removed.')
        return reverse('buyers')

class VendorListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Vendor
    context_object_name = 'vendors'
    paginate_by = 6

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(VendorListView, self).get_context_data(**kwargs)
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
        context['is_seller'] = True
        context['reviews'] = VendorReview.objects.filter(vendor=self.object)
        return context

class VendorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vendor
    fields = ['store_name', 'store_info', 'address_line', 'city', 'state', 
                'zip_code', 'contact_no', 'secondary_no', 'image', 'user']

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(VendorUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Vendor Edit"
        return context

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.store_name)
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
        if Category.objects.filter(name=form.cleaned_data['name']).exists():
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
                new_prod.slug = slugify(new_prod.name)
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
            'is_seller' : True
        }

        return render(request, 'admins/products/product_form.html', context)
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
        context['is_seller'] = True
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
                p_form.instance.slug = slugify(p_form.instance.name)
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
            'is_seller' : True
        }

        return render(request, 'admins/products/product_update.html', context)
    else:
        return redirect('home')

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(ProductDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Product Delete"
        context['is_seller'] = True
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
def BuyerProductCreateView(request, pk=None):
    buyer = Buyer.objects.get(buyer_id=pk)
    is_admin = request.user.groups.filter(name='Admin').exists() 
    if is_admin or buyer.user.id == request.user.id:
        if request.method == "POST":
            p_form = BuyerProductCreateForm(request.POST)
            c_form = AssignBuyerCategoryForm(request.POST)

            if p_form.is_valid() and c_form.is_valid():
                new_prod = p_form.save(commit=False)
                new_prod.buyer = buyer
                new_prod.slug = slugify(new_prod.name)
                new_prod.save()
                p_form.save_m2m()
                c_form.instance.product = new_prod
                c_form.save()

                messages.success(request, 'New product has been added.')
                if is_admin:
                    return redirect('buyer-product-detail', new_prod.slug)
                else:
                    return redirect('buyer-product', new_prod.slug)
        else:
            p_form = BuyerProductCreateForm()
            c_form = AssignBuyerCategoryForm()
        
        context = {
            'p_form': p_form,
            'c_form': c_form,
            'title':'New Product',
            'is_seller': False
        }
        if is_admin:
            return render(request, 'admins/products/product_form.html', context)
        else:
            return render(request,'main/buyers/products/buyer_product_form.html', context)
    else:
        return redirect('home')


class BuyerProductDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = BuyerProduct

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(BuyerProductDetailView, self).get_context_data(**kwargs)
        context['products'] = BuyerProduct.objects.filter(buyer=self.object.buyer).order_by('-date_created').exclude(product_id=self.object.product_id)
        if BuyerProductCategory.objects.get(product=self.object):
            context['category'] = BuyerProductCategory.objects.get(product=self.object)
        context['title'] = self.object.name
        context['is_seller'] = False
        return context

@login_required
def BuyerProductUpdateView(request, pk=None):
    product = BuyerProduct.objects.get(product_id=pk)
    is_admin = request.user.groups.filter(name='Admin').exists()
    if is_admin or product.buyer.user.id == request.user.id:
        product = BuyerProduct.objects.get(product_id=pk)
        category = BuyerProductCategory.objects.get(product=product)
        if request.method == "POST":
            p_form = BuyerProductCreateForm(request.POST, instance=product)
            c_form = AssignBuyerCategoryForm(request.POST, instance=category)

            if p_form.is_valid() and c_form.is_valid():
                p_form.instance.slug = slugify(p_form.instance.name)
                new_prod = p_form.save()
                c_form.save()
                messages.success(request, 'Buyer product has been updated.')
                if is_admin:
                    return redirect('buyer-product-detail', new_prod.slug)
                else:
                    return redirect('buyer-product', new_prod.slug)
        else:
            p_form = ProductCreateForm(instance=product)
            c_form = AssignCategoryForm(instance=category)
        
        context = {
            'p_form': p_form,
            'c_form': c_form,
            'title':'Update Product',
            'is_seller' : True
        }
        if is_admin:
            return render(request, 'admins/products/product_update.html', context)
        else:
            context.update({'is_owner':True})
            return render(request, 'main/buyers/products/buyer_product_update.html', context)
    else:
        return redirect('home')

class BuyerProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BuyerProduct

    def test_func(self):
        product=BuyerProduct.objects.get(product_id=self.kwargs['pk'])
        return self.request.user.groups.filter(name='Admin').exists() or product.buyer.user.id == self.request.user.id

    def get_context_data(self, **kwargs):
        context = super(BuyerProductDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Product Delete"
        context['is_seller'] = False
        return context

    def form_valid(self, form):
        pt = BuyerProductCategory.objects.get(product = self.object)
        if pt:
            for i in pt:
                i.delete()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Buyer product has been deleted.')
        if self.request.user.groups.filter(name='Admin').exists():
            return reverse('buyers')
        else:
            return reverse('buyers-main')

class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    context_object_name = 'users'
    paginate_by = 6

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
        form.instance.slug = slugify(form.instance.store_name)
        v_group = Group.objects.get(name='Vendor')
        v_group.user_set.add(user)
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Store created!')
        return reverse("vendor-detail",  kwargs={'pk': self.object.pk})

class BuyerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Buyer
    form_class = BuyerCreateForm

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(BuyerCreateView, self).get_context_data(**kwargs)
        context['title'] = "New Buyer Store"
        return context

    def form_valid(self, form):
        user = User.objects.get(id = self.kwargs['pk'])
        form.instance.user = user
        form.instance.slug = slugify(form.instance.store_name)
        v_group = Group.objects.get(name='Buyer')
        v_group.user_set.add(user)
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Buyer Store created!')
        return reverse("buyer-detail",  kwargs={'pk': self.object.pk})

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
    paginate_by = 6

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(WishlistView, self).get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['pk'])
        context['user'] = user
        context['title'] = user.username + "'s Wishlist"
        context['items'] = WishlistItem.objects.filter(user=user)
        return context

class CartView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CartItem
    context_object_name = 'items'
    paginate_by = 6
    
    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['pk'])
        context['user'] = user
        context['title'] = user.username + "'s Cart"
        context['items'] = CartItem.objects.filter(user=user)
        return context

def get_sort_orders(request):
    option = request.GET.get('option')
    if option == 'a':
        context = {'orders': SiteOrder.objects.all().order_by('-date_placed') }
    elif option == 'u':
        context = {'orders': SiteOrder.objects.filter(status="Unfulfilled").order_by('-date_placed')  }
    elif option == 'p':
        context = {'orders': SiteOrder.objects.filter(status="Pending").order_by('-date_placed')  }
    elif option == 'o':
        context = {'orders': SiteOrder.objects.filter( Q(status="Unfulfilled") | Q(status="Pending") | Q(status="Shipped") ).order_by('-date_placed') }
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
        open_status = ['Unfulfilled', 'Pending']
        if self.object.status in open_status:
            context['is_open'] = True
        return context

class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SiteOrder
    fields = ['status', 'contact_no', 'address_line', 'city', 'state', 'zip_code', 'payment_method']

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Order Edit"
        return context

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
        open_status = ['Unfulfilled', 'Pending', 'Shipped']
        if order.status in open_status:
            items = OrderItem.objects.filter(order=order)
            for i in items:
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
        open_status = ['Unfulfilled', 'Pending']
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
        open_status = ['Unfulfilled', 'Pending']
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
            item = OrderItem.objects.get(product=self.object.product, order=self.object.order)
            order = item.order
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

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Product quantity updated!')
        return reverse("order-update-items", kwargs={'pk': self.kwargs['order_pk']})

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
        order = SiteOrder.objects.get(order_id=self.kwargs['order_pk'])
        if order in closed_status:
            messages.error(self.request, 'You can no longer update items from closed orders!')
            return redirect('orders')
        else:
            item = OrderItem.objects.get(product_id=self.kwargs['product_pk'], order_id=self.kwargs['order_pk'])
            prod = Product.objects.get(product_id=self.kwargs['product_pk'])
            prod.item_stock = prod.item_stock + item.quantity
            prod.save()
            order.total = order.total - prod.price * decimal.Decimal(item.quantity)
            order.save()
            return super(OrderItemDeleteView, self).delete(*args, **kwargs)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Order item has been deleted.')
        return reverse('order-detail', kwargs={'pk':self.kwargs['order_pk']})