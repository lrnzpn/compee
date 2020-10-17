from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView
from admins.funcs import unique_store_slug_generator
from .models import Vendor, ServiceProvider
from .forms import (
    UserRegisterForm, UserUpdateForm, PasswordResetForm, 
    ProviderUpdateForm, VendorUpdateForm, AdminForm
)

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
def ManageProvider(request):
    if request.user.groups.filter(name='Provider').exists():
        user = ServiceProvider.objects.get(user = request.user)
        if request.method == "POST":
            p_form = ProviderUpdateForm(request.POST, instance=user)
            if p_form.is_valid():
                p_form.instance.slug = unique_store_slug_generator(p_form.instance)
                p_form.save()
                messages.success(request, f'Your store details have been updated!')
                return redirect('manage-provider')
        else:
            p_form = ProviderUpdateForm(instance=user)
        context = {
            'p_form': p_form,
            'site_user': user,
            'title': 'Profile'
        }
        return render(request, 'users/profile/provider/manage_provider.html', context)
    else:
        return redirect('home')

@login_required
def ManageVendor(request):
    if request.user.groups.filter(name='Vendor').exists():
        user = Vendor.objects.get(user = request.user)
        if request.method == "POST":
            s_form = VendorUpdateForm(request.POST, instance=user)
            if s_form.is_valid():
                s_form.instance.slug = unique_store_slug_generator(s_form.instance)
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

            if all(v != "" for v in [old, new1, new2]):
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