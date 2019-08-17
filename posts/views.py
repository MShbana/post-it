from .forms import PostForm, CommentForm
from .models import Post, Comment
from .orm_utils import (
    get_home_posts_list,
    get_paginated_posts,
    get_most_popular_posts,
    get_suggested_friends
)
from accounts.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView


class Home(TemplateView):

    template_name = 'posts/home.html'

    def get(self, request):
        post_form = PostForm()
        comment_form = CommentForm()

        posts_list, following_list, _ = get_home_posts_list(request)
        posts = get_paginated_posts(request, posts_list)
        args = {
            'posts': posts,
            'most_popular_posts': get_most_popular_posts(),
            'post_form': post_form,
            'comment_form': comment_form,
            'suggested_friends': get_suggested_friends(
                                    request, following_list),
        }
        return render(request, self.template_name, args)


@require_POST
@login_required
def new_post(request):
    post_form = PostForm(request.POST)
    post_data = {}

    if post_form.is_valid():
        post = post_form.save(commit=False)
        post.user = request.user
        post.save()

        post_data = {
            'pk': post.pk,
            'form_is_valid': True,
            'post': render_to_string(
                'posts/_post_base.html',
                {
                    'post': post,
                    'comment_form': CommentForm()
                },
                request=request
            ),
            'comments_count': render_to_string(
                'posts/_comments_count_base.html',
                {
                    'comments_count': post.comments.count()
                },
                request=request
            )
        }
    else:
        post_data['form_is_valid'] = False

    return JsonResponse(post_data)


@require_POST
@login_required
def new_comment(request):
    post_id = request.POST.get('id', None)
    post = get_object_or_404(Post, pk=post_id)

    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

        comments = post.comments.all()
        comment_data = {
            'pk': comment.pk,
            'form_is_valid': True,
            'comments': render_to_string(
                'posts/_comments_base.html',
                {
                    'post': post,
                    'comments': comments
                },
                request=request
            ),
            'comments_count': render_to_string(
                'posts/_comments_count_base.html',
                {
                    'comments_count': comments.count
                },
                request=request
            )
        }
    else:
        comment_data['form_is_valid'] = False

    return JsonResponse(comment_data)


@login_required
def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

            messages.success(request, 'Your comment has been added.')
            return redirect('posts:view_post', post.slug)
    else:
        comment_form = CommentForm()

    args = {
        'post': post,
        'comment_form': comment_form,
        'comments_count': post.comments.count()
    }
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
            messages.success(
                request, 'Your post has been successfully updated.'
            )
            return redirect('posts:view_post', post.slug)
    else:
        form = PostForm(instance=post)

    args = {'post': post, 'form': form}
    return render(request, 'posts/edit_post.html', args)


@require_POST
@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    absolute_url = request.build_absolute_uri(
        reverse('posts:view_post', args=[post.slug])
    )

    if request.user != post.user:
        raise PermissionDenied()

    post.delete()
    messages.success(request, 'Your post has been successfully deleted.')

    referer_url = request.META.get('HTTP_REFERER', '/')
    if referer_url == absolute_url:
        return redirect('posts:home')

    return HttpResponseRedirect(referer_url)


@require_POST
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.author:
        raise PermissionDenied()

    comment.delete()
    messages.success(request, 'Your comment has been successfully deleted.')

    referer_url = request.META.get('HTTP_REFERER', '/')

    return HttpResponseRedirect(referer_url)


@login_required
def edit_commnet(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.author:
        raise PermissionDenied()

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'Your comment has been on {comment.post.title} successfully updated.'
            )
            return redirect('posts:view_post', comment.post.slug)

    else:
        form = CommentForm(instance=comment)

    args = {'comment': comment, 'form': form}
    return render(request, 'posts/edit_comment.html', args)
