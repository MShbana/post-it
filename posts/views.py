from .forms import PostCreationForm
from .models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView


class Home(TemplateView):
    
    template_name = 'posts/home.html'

    def get(self, request):
        form = PostCreationForm()

        posts_list = Post.objects.all()
        paginator = Paginator(posts_list, 10)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        args = {'posts': posts, 'form': form}
        return render(request, self.template_name, args)

    def post(self, request):
        form = PostCreationForm(request.POST)
        if form.is_valid():
            saved_post = form.save(commit=False)
            saved_post.user = request.user
            saved_post.save()
            return redirect('posts:home')

        args = {'form': form}
        return render(request, self.template_name, args)


@login_required
def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    args = {'post': post}
    return render(request, 'posts/view_post.html', args)


@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.user:
        raise PermissionDenied()

    if request.method == 'POST':
        form = PostCreationForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been successfully updated.')
            return redirect('posts:view_post', post.slug)
    else:
        form = PostCreationForm(instance=post)

    args = {'post': post, 'form': form}
    return render(request, 'posts/edit_post.html', args)


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.user:
        raise PermissionDenied()

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been successfully deleted.')
        return redirect('posts:home')

    args = {'post': post}
    return render(request, 'posts/delete_post_confirm.html', args)
