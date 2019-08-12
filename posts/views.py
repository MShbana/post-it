from .forms import PostForm, CommentForm
from .models import Post
from accounts.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from itertools import chain
from operator import attrgetter



class Home(TemplateView):
    
    template_name = 'posts/home.html'

    def get(self, request):
        form = PostForm()

        following_list = request.user.profile.following.all()
        following_posts_list = Post.objects.filter(user__profile__in=following_list)
        user_posts_list = Post.objects.filter(user=request.user)
        posts_list = sorted(
            chain(following_posts_list, user_posts_list),
            key=attrgetter('date_posted'),
            reverse=True)

        paginator = Paginator(posts_list, 10)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        most_popular_posts = Post.objects.annotate(
            num_comments=Count('comments')).order_by('-num_comments')[:10]

        suggested_friends = Profile.objects.all().exclude(pk__in=following_list).exclude(user=request.user).order_by('-created')[:10]

        args = {
            'posts': posts,
            'most_popular_posts': most_popular_posts,
            'form': form,
            'suggested_friends': suggested_friends,
            'following_list': following_list
        }
        return render(request, self.template_name, args)

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Your post has been successfully created.')
            return redirect('posts:home')

        args = {'form': form}
        return render(request, self.template_name, args)


@login_required
def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect('posts:view_post', post.slug)
    else:
        form = CommentForm()

    args = {'post': post, 'form': form}
    return render(request, 'posts/view_post.html', args)


@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.user:
        raise PermissionDenied()

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been successfully updated.')
            return redirect('posts:view_post', post.slug)
    else:
        form = PostForm(instance=post)

    args = {'post': post, 'form': form}
    return render(request, 'posts/edit_post.html', args)


@require_POST
@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    absolute_url = request.build_absolute_uri(reverse('posts:view_post', args=[post.slug]))

    if request.user != post.user:
        raise PermissionDenied()

    post.delete()
    messages.success(request, 'Your post has been successfully deleted.')

    referer_url = request.META.get('HTTP_REFERER', '/')
    if referer_url == absolute_url:
        return redirect('posts:home')

    return HttpResponseRedirect(referer_url)
