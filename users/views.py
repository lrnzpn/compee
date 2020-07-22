from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, SiteUserUpdateForm, PasswordResetForm
from .models import SiteUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

def Register(request): 
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new = form.save()
            usr = SiteUser(account=new)
            usr.save()
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
def ManageStore(request):
    user = SiteUser.objects.get(account = request.user)
    if request.method == "POST":
        s_form = SiteUserUpdateForm(request.POST, instance=user)

        if s_form.is_valid():
            s_form.save()
            messages.success(request, f'Your account details have been updated!')
            return redirect('manage-store')
    else:
        s_form = SiteUserUpdateForm(instance=user)

    context = {
        's_form': s_form,
        'site_user': user,
        'title': 'Profile'
    }
    
    return render(request, 'users/profile/manage_store.html', context)

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