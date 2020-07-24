from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from users.models import Vendor
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

class VendorDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Vendor

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

class VendorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vendor
    fields = ['store_name', 'store_info', 'address_line', 'city', 'state', 
                'zip_code', 'contact_no', 'secondary_no', 'image', 'user']
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Vendor information updated!')
        return reverse("vendor-detail", kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()
    
class VendorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vendor

    def delete(self, *args, **kwargs):
        vendor = Vendor.objects.get(vendor_id = self.kwargs['pk'])
        user = User.objects.get(id = vendor.user.id)
        v_group = Group.objects.get(name='Vendor')
        v_group.user_set.remove(user)
        return super(VendorDeleteView, self).delete(*args, **kwargs)

    def get_success_url(self, **kwargs):
        messages.success(self.request, 'Vendor has been removed.')
        return reverse('vendors')
    
    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()




