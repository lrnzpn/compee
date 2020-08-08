from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.template.defaultfilters import slugify
from users.models import Vendor, Buyer
from .models import Product, Category, ProductCategory, BuyerProduct, BuyerProductCategory
from .forms import ProductCreateForm, AssignCategoryForm, BuyerProductCreateForm, AssignBuyerCategoryForm
from users.forms import VendorUpdateForm, BuyerCreateForm, AdminForm
from django.contrib.auth.models import User, Group
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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
    if request.user.groups.filter(name='Admin').exists():
        if request.method == "POST":
            p_form = BuyerProductCreateForm(request.POST)
            c_form = AssignBuyerCategoryForm(request.POST)

            if p_form.is_valid() and c_form.is_valid():
                buyer = Buyer.objects.get(buyer_id=pk)
                new_prod = p_form.save(commit=False)
                new_prod.buyer = buyer
                new_prod.slug = slugify(new_prod.name)
                new_prod.save()
                p_form.save_m2m()
                c_form.instance.product = new_prod
                c_form.save()

                messages.success(request, 'New product has been added.')
                return redirect('buyer-product-detail', new_prod.slug)
        else:
            p_form = ProductCreateForm()
            c_form = AssignCategoryForm()
        
        context = {
            'p_form': p_form,
            'c_form': c_form,
            'title':'New Product',
            'is_seller': False
        }

        return render(request, 'admins/products/product_form.html', context)
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
    if request.user.groups.filter(name='Admin').exists():
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
                return redirect('buyer-product-detail', new_prod.slug)
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

class BuyerProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BuyerProduct

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

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
        return reverse('buyers')

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
        return render(request, 'admins/users/make_admin.html', context)
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
        return render(request, 'admins/users/remove_admin.html', context)
    else:
        return redirect('home')

