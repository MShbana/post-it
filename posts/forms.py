from .models import Post
from crispy_forms.helper import FormHelper
from django import forms


class PostCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['title'].widget.attrs['placeholder'] = 'Your Post Title'
        self.fields['body'].widget.attrs['placeholder'] = 'Your Post'


    class Meta:
        model = Post
        fields = ('title', 'body')