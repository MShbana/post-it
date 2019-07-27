from .forms import UserRegisterationForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect


@login_required
def view_account(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    args = {'user': profile.user}
    return render(request, 'accounts/view_account.html', args)


@login_required
def view_account_info(request):
    args = {'user': request.user }
    return render(request, 'accounts/view_account_info.html', args)


def register(request):
    if request.user.is_authenticated:
        return redirect('home:home')

    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created. Your are able to login now.')
            return redirect('home:home')
    else:
        form = UserRegisterationForm()

    args = {'form': form}
    return render(request, 'accounts/register.html', args)
