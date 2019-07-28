from .models import Post, Comment
from django import forms


class PostCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = False
        self.fields['body'].label = False
        self.fields['title'].widget.attrs['placeholder'] = 'Your Post Title'
        self.fields['body'].widget.attrs['placeholder'] = 'Your Post'

    class Meta:
        model = Post
        fields = ('title', 'body')


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].label = False
        self.fields['body'].widget.attrs['placeholder'] = 'Leave your comment here...'

    class Meta:
        model = Comment
        fields = ('body', )
