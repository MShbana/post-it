from .models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class ExtraFieldsRequiredMixin(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True



class UserRegisterationForm(ExtraFieldsRequiredMixin, UserCreationForm):

    REGEX_PATTERN = RegexValidator(r'^[a-zA-Z]+$', 'Enter a valid name.')

    email = forms.EmailField(help_text='Required.')
    first_name = forms.CharField(max_length=20,
                                 validators=[REGEX_PATTERN],
                                 help_text="Required. Non-spaced English Characters.")
    last_name = forms.CharField(max_length=20,
                                validators=[REGEX_PATTERN],
                                help_text="Required. Non-spaced English Characters.")
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user with this email is already registered.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username


class UserUpdateForm(ExtraFieldsRequiredMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(UserUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_user_username = self.instance.username
        if User.objects.filter(email__iexact=email).exclude(username__iexact=current_user_username).exists():
            raise forms.ValidationError('A user with this email is already registered.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        current_user_email = self.instance.email
        if User.objects.filter(username__iexact=username).exclude(email__iexact=current_user_email).exists():
            raise forms.ValidationError('This username is already taken.')
        return username


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('city', 'country', 'linkedin', 'gender', 'image')
        widgets = {
            'image': forms.FileInput(),
        }
