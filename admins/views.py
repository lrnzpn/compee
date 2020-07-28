from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from users.models import Vendor
from .models import Product, Term, ProductTerm
from .forms import ProductCreateForm, AssignCategoryForm
from django.contrib.auth.models import User, Group
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

@login_required
def MainDashboard(request):
    if request.user.groups.filter(name='Admin').exists():
        return render(request, 'admins/dashboard.html')
    else:
        return redirect('home')

class VendorListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Vendor
    context_object_name = 'vendors'
    paginate_by = 6

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(VendorListView, self).get_context_data(**kwargs)
        context['title'] = "Vendors | Dashboard"
        return context

class VendorDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Vendor

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
    def get_context_data(self, **kwargs):
        context = super(VendorDetailView, self).get_context_data(**kwargs)
        vendor = Vendor.objects.get(vendor_id=self.kwargs['pk'])
        context['products'] = Product.objects.filter(vendor=vendor).order_by('-date_created')
        context['title'] = "Shop Name"
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

class TermCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Term
    fields = ['name', 'term_type']

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(TermCreateView, self).get_context_data(**kwargs)
        context['title'] = "New Term"
        context['terms'] = Term.objects.all().order_by('term_type')
        return context

    def form_valid(self, form):
        if Term.objects.filter(name=form.cleaned_data['name'], term_type=form.cleaned_data['term_type']).exists():
            messages.error(self.request,'A term of this type already exists!')
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Term created!')
        return reverse("term-create")

class TermUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Term
    fields = ['name', 'term_type']

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(TermUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Update Term"
        return context

    def form_valid(self, form):
        if Term.objects.filter(name=form.cleaned_data['name'], term_type=form.cleaned_data['term_type']).exists():
            messages.error(self.request,'A term of this type already exists!')
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Term updated!')
        return reverse("term-create")

class TermDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Term

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def get_context_data(self, **kwargs):
        context = super(TermDeleteView, self).get_context_data(**kwargs)
        context['title'] = "Term Delete"
        return context

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Term has been deleted.')
        return reverse('term-create')

@login_required
def ProductCreateView(request, pk=None):
    if request.user.groups.filter(name='Admin').exists():
        if request.method == "POST":
            p_form = ProductCreateForm(request.POST)
            c_form = AssignCategoryForm(request.POST)

            if p_form.is_valid() and c_form.is_valid():
                vendor = Vendor.objects.get(vendor_id=pk)
                p_form.instance.vendor = vendor
                new_prod = p_form.save()
                c_form.instance.product = new_prod
                c_form.save()

                messages.success(request, 'New product has been added.')
                return redirect('product-detail', new_prod.product_id)
        else:
            p_form = ProductCreateForm()
            c_form = AssignCategoryForm()
        
        context = {
            'p_form': p_form,
            'c_form': c_form,
            'title':'New Product'
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
        context['products'] = Product.objects.filter(vendor=self.object.vendor).order_by('-date_created')
        context['category'] = ProductTerm.objects.filter(product=self.object)
        context['title'] = "Product Name"
        return context

@login_required
def ProductUpdateView(request, pk=None):
    if request.user.groups.filter(name='Admin').exists():
        product = Product.objects.get(product_id=pk)
        category = ProductTerm.objects.filter(product=product).first()
        if request.method == "POST":
            p_form = ProductCreateForm(request.POST, instance=product)
            c_form = AssignCategoryForm(request.POST, instance=category)

            if p_form.is_valid() and c_form.is_valid():
                p_form.save()
                c_form.save()
                messages.success(request, 'Product has been updated.')
                return redirect('product-detail', pk)
        else:
            p_form = ProductCreateForm(instance=product)
            c_form = AssignCategoryForm(instance=category)
        
        context = {
            'p_form': p_form,
            'c_form': c_form,
            'title':'Update Product'
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
        return context

    def form_valid(self, form):
        pt = ProductTerm.objects.filter(product = self.object)
        if pt:
            for i in pt:
                i.delete()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Product has been deleted.')
        return reverse('vendors')