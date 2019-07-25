from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ExtraFieldsRequiredMixin(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

class UserRegisterationForm(ExtraFieldsRequiredMixin, UserCreationForm):

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("The email is already registered. Please choose another one.")
        return email
