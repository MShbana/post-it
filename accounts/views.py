from .tokens import account_activation_token
from .forms import UserRegisterationForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string


@login_required
def view_account(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    user = profile.user

    posts_list = user.posts.all()
    paginator = Paginator(posts_list, 10)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    args = {'user': user, 'posts': posts}
    return render(request, 'accounts/view_account.html', args)


@login_required
def view_update_account(request):
    user = request.user

    if request.method == 'POST':
        user_form = UserUpdateForm(data=request.POST, instance=user, user=user)
        profile_form = ProfileUpdateForm(data=request.POST, files=request.FILES, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account Information has been updated.')
            return redirect('accounts:view_update_account')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=user.profile)

    args = {'user': user, 'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'accounts/view_update_account.html', args)


def register(request):
    if request.user.is_authenticated:
        return redirect('posts:home')

    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your Post It account.'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Your account has been successfully created.')
            return render(request, 'accounts/account_created.html')
    else:
        form = UserRegisterationForm()

    args = {'form': form}
    return render(request, 'accounts/register.html', args)


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been successfully activated.')
        return render(request, 'accounts/account_verified.html')
    else:
        messages.warning(request, 'Activation Link is invalid.')
        return render(request, 'accounts/account_verification_failed.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password has been successfully updated.')
            return redirect('posts:home')
    else:
        form = PasswordChangeForm(user=request.user)

    args = {'form': form}
    return render(request, 'accounts/change_password.html', args)
