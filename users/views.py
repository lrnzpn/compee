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
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from admins.funcs import unique_store_slug_generator

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
                form.instance.slug = unique_store_slug_generator(form.instance)
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
                b_form.instance.slug = unique_store_slug_generator(b_form.instance)
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