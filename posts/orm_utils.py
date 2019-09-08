from .models import Post
from accounts.models import Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q


def get_home_posts_list(request):
    current_user = request.user
    following_list = current_user.profile.following.all()

    home_posts = Post.objects\
                    .filter(
                        Q(user=current_user)|
                        Q(user__profile__in=following_list)
    )

    return (home_posts, following_list, current_user)


def get_paginated_posts(request, posts_list):
    paginator = Paginator(posts_list, 10)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return posts


def get_most_popular_posts():
    most_popular_posts = Post.objects.annotate(
            num_comments=Count('comments')).order_by('-num_comments')[:10]
    return most_popular_posts


def get_suggested_friends(request, following_list):
    suggested_friends = Profile.objects.all().\
        exclude(pk__in=following_list).\
        exclude(user=request.user).\
        exclude(user__is_active=False).\
        order_by('created')[:10]
    return suggested_friends
