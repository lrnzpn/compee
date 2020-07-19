from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, SiteUserUpdateForm
from .models import SiteUser
from django.contrib.auth.decorators import login_required

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
def Profile(request):
    user = SiteUser.objects.get(account = request.user)
    if request.method == "POST":
        s_form = SiteUserUpdateForm(request.POST, instance=user)
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid() and s_form.is_valid():
            u_form.save()
            s_form.save()
            messages.success(request, f'Your account details have been updated!')
            return redirect('profile')
    else:
        s_form = SiteUserUpdateForm(instance=user)
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
        's_form': s_form,
        'site_user': user,
        'title': 'Profile'
    }
    
    return render(request, 'users/profile.html', context)