from .forms import PostCreationForm
from .models import Post
from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    
    template_name = 'posts/home.html'

    def get(self, request):
        form = PostCreationForm()
        posts = Post.objects.all()
        args = {'posts': posts, 'form': form}
        return render(request, self.template_name, args)
