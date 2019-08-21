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
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import TemplateView
from notifications.signals import notify


class Home(TemplateView):

    template_name = 'posts/home.html'

    def get(self, request):
        post_form = PostForm()
        comment_form = CommentForm()
        form = PostForm()

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

@require_GET
@login_required
def view_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()

    args = {
        'post': post,
        'comment_form': comment_form,
        'comments_count': post.comments.count()
    }
    return render(request, 'posts/view_post.html', args)


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
    post_id = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=post_id)
    comment_form = CommentForm(request.POST)
    
    current_user = request.user
    post_author = post.user

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        comments = post.comments.all()
        comments_count = comments.count()

        comment_data = {
            'pk': comment.pk,
            'form_is_valid': True,
            'post_id': post.id,
            'comments_count': render_to_string(
                'posts/_comments_count_base.html',
                {
                    'comments_count': comments_count
                },
                request=request
            ),
            'comment': render_to_string(
                'posts/_comment_base.html',
                {
                    'comment': comment,
                },
                request=request
            )
        }
        if current_user != post_author:
            notify.send(
                sender=request.user,
                recipient=post.user,
                verb=f'commented on your post',
                target=post,
                action_object=comment,
                level='info',
                public=False,
            )
    else:
        comment_data['form_is_valid'] = False

    return JsonResponse(comment_data)


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.user:
        raise PermissionDenied()

    if request.method == 'POST':
        edit_post_form = PostForm(request.POST, instance=post)
        if edit_post_form.is_valid():
            edit_post_form.save()

            data = {
                'post': render_to_string(
                    'posts/_post_editable_content.html',
                    {
                        'post': post,
                    },
                    request=request
                ),
                'form_is_valid': True
            }
        else:
            data = {
                'form_is_valid': False
            }
    else:
        edit_post_form = PostForm(instance=post)
        data = {
            'edit_post_form': render_to_string(
                'posts/_edit_post_form_base.html',
                {
                    'post': post,
                    'edit_post_form': edit_post_form
                },
                request=request,
            )
        }
    return JsonResponse(data)

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.author:
        raise PermissionDenied()

    if request.method == 'POST':
        edit_comment_form = CommentForm(request.POST, instance=comment)
        if edit_comment_form.is_valid():
            edit_comment_form.save()
            data = {
                'comment': render_to_string(
                    'posts/_comment_editable_content.html',
                    {
                        'comment': comment
                    },
                    request=request
                ),
                'form_is_valid': True
            }
        else:
            data = {
                'form_is_valid': False
            }
    else:
        edit_comment_form = CommentForm(instance=comment)
        data = {
            'edit_comment_form': render_to_string(
                'posts/_edit_comment_form_base.html',
                {
                    'comment': comment,
                    'edit_comment_form': edit_comment_form
                },
                request=request,
            )
        }
    return JsonResponse(data)

@require_GET
@login_required
def cancel_edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    data = {
        'post': render_to_string(
            'posts/_post_editable_content.html',
            {
                'post': post
            },
            request=request
        )
    }
    return JsonResponse(data)

@require_GET
@login_required
def cancel_edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    data = {
        'comment': render_to_string(
            'posts/_comment_editable_content.html',
            {
                'comment': comment
            },
            request=request
        )
    }
    return JsonResponse(data)


@require_POST
@login_required
def delete_post(request):
    pk = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.user:
        raise PermissionDenied()

    data = {}
    absolute_url = request.build_absolute_uri(
        reverse('posts:view_post', args=[post.pk])
    )
    referer_url = request.META.get('HTTP_REFERER', '/')
    if referer_url == absolute_url:
        data = {
            'redirect': reverse('posts:home')
        }
    post.delete()
    return JsonResponse(data)


@require_POST
@login_required
def delete_comment(request):
    pk = request.POST.get('pk', None)
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user != comment.author:
        raise PermissionDenied()

    comment.delete()
    comments_count = post.comments.count()

    data = {
        'comments_count': render_to_string(
                'posts/_comments_count_base.html',
                {
                    'comments_count': comments_count
                },
                request=request
            ),
        'post_id': post.pk
    }
    if comments_count == 0:
        data.update({
            'empty_comments': render_to_string(
                'posts/_comments_base.html',
                {
                    'comments': post.comments.all(),
                    'post': post,
                },
                request=request
            )
        })
    return JsonResponse(data)

@require_POST
@login_required
def like_post(request):
    current_user = request.user
    post_id = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=post_id)

    if post.likes.filter(id=current_user.id).exists():
        post.likes.remove(current_user)
    else:
        post.likes.add(current_user)
        
        if current_user != post.user:
            notify.send(
                sender=current_user,
                recipient=post.user,
                verb='liked your post',
                target=post,
                level='primary',
                public=False
            )

    data = {
        'likes': render_to_string(
            'posts/_like_base.html',
            {
                'post': post
            },
            request=request
        ),
        'likes_count': post.total_likes,
        'form_is_valid': True
    }
    return JsonResponse(data)