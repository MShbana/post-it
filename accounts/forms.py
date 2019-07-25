from django import forms
from django.contrib.auth.forms import UserCreationForm
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
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered. Please choose another one.")
        return email
