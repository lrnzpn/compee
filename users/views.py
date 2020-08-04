from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import (
    UserRegisterForm, UserUpdateForm, PasswordResetForm, 
    BuyerUpdateForm, BuyerCreateForm, BuyerDeleteForm,
    VendorUpdateForm, AdminForm
)
from .models import Vendor, Buyer
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def Register(request): 
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}!')
                return redirect('home')
        else:
            form = UserRegisterForm()

        context = {
            'form': form,
            'title': 'Sign Up'
        }
        return render(request, 'users/register.html', context)

@login_required
def BecomeBuyer(request):
    if request.user.groups.filter(name='Buyer').exists():
        return redirect('home')
    else:
        if request.method == "POST":
            form = BuyerCreateForm(request.POST)
            if form.is_valid():
                form.instance.user = request.user
                form.instance.slug = slugify(form.instance.store_name)
                b_group = Group.objects.get(name='Buyer')
                b_group.user_set.add(request.user)
                form.save()
                messages.success(request, f'Successfully registered as a public buyer!')
                return redirect('manage-buyer')
        else:
            form = BuyerCreateForm()

        context = {
            'form': form,
            'title': 'Buyer Sign Up'
        }
        return render(request, 'users/profile/buyer/buyer_form.html', context)

@login_required
def ManageBuyer(request):
    if request.user.groups.filter(name='Buyer').exists():
        user = Buyer.objects.get(user = request.user)
        if request.method == "POST":
            b_form = BuyerUpdateForm(request.POST, instance=user)
            if b_form.is_valid():
                b_form.instance.slug = slugify(b_form.instance.store_name)
                b_form.save()
                messages.success(request, f'Your store details have been updated!')
                return redirect('manage-buyer')
        else:
            b_form = BuyerUpdateForm(instance=user)
        context = {
            'b_form': b_form,
            'site_user': user,
            'title': 'Profile'
        }
        return render(request, 'users/profile/buyer/manage_buyer.html', context)
    else:
        return redirect('home')

def DeleteBuyer(request):
    if request.user.groups.filter(name='Buyer').exists():
        user = Buyer.objects.get(user = request.user)
        if request.method == "POST":
            b_form = BuyerDeleteForm(request.POST, instance=user)
            if b_form.is_valid():
                user.delete()
                b_group = Group.objects.get(name='Buyer')
                b_group.user_set.remove(request.user)
                messages.success(request, f'Buyer profile deleted.')
                return redirect('manage-account')
        else:
            b_form = BuyerDeleteForm(instance=user)
        context = {
            'b_form': b_form,
            'title': 'Delete Buyer Profile'
        }
        return render(request, 'users/profile/buyer/buyer_confirm_delete.html', context)
    else:
        return redirect('home')


@login_required
def ManageVendor(request):
    if request.user.groups.filter(name='Vendor').exists():
        user = Vendor.objects.get(user = request.user)
        if request.method == "POST":
            s_form = VendorUpdateForm(request.POST, instance=user)
            if s_form.is_valid():
                s_form.instance.slug = slugify(s_form.instance.store_name)
                s_form.save()
                messages.success(request, f'Your store details have been updated!')
                return redirect('manage-vendor')
        else:
            s_form = VendorUpdateForm(instance=user)
        context = {
            's_form': s_form,
            'site_user': user,
            'title': 'Profile'
        }
        return render(request, 'users/profile/manage_vendor.html', context)
    else:
        return redirect('home')

@login_required
def ManageAccount(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        pass_form = PasswordResetForm(request.POST, instance=request.user)

        if u_form.is_valid() and pass_form.is_valid():
            u_form.save()

            old = pass_form.cleaned_data['oldpassword']
            new1 = pass_form.cleaned_data['newpassword1']
            new2 = pass_form.cleaned_data['newpassword2']

            if all(v is not "" for v in [old, new1, new2]):
                username = request.user.username
                user = authenticate(username=username, password=old)
                if user is not None:
                    user.set_password(new1)
                    user.save()
                    messages.success(request, f'Password has been changed! Please login again.')
                    return redirect('login')
                else:
                    messages.error(request, f'Please enter the correct password. Note that the field may be case-senstive.')
                    return redirect('manage-account')
                    
            messages.success(request, f'Your account details have been updated!')
            return redirect('manage-account')
        else:
            messages.error(request, f'There was an error in your input.')
            return redirect('manage-account')
    else:
        u_form = UserUpdateForm(instance=request.user)
        pass_form = PasswordResetForm(instance=request.user)

    context = {
        'u_form': u_form,
        'pass_form': pass_form,
        'title': 'Profile'
    }
    
    return render(request, 'users/profile/manage_account.html', context)

#admin functions
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