from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect


@login_required
def view_account(request, slug):
    user_profile = get_object_or_404(UserProfile, slug=slug)
    args = {'user': user_profile.user}
    return render(request, 'accounts/view_account.html', args)


@login_required
def view_account_info(request, slug):
    user_profile = get_object_or_404(UserProfile, slug=slug)
    args = {'user': user_profile.user}
    return render(request, 'accounts/view_account_info.html', args)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:home')
    else:
        form = UserCreationForm()

    args = {'form': form}
    return render(request, 'accounts/register.html', args)