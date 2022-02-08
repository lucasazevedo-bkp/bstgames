import re

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import forms as auth_forms
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.forms import UserCreationForm, UserChangeForm
from .models import GameGenre, GamePlatform
from users.models import UserAddress

User = get_user_model()


class SignUpForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']
        user.username = user.email
        if commit:
            user.save()
        return user


class LogInForm(auth_forms.AuthenticationForm):
    username = auth_forms.UsernameField(label=_('Email address'), widget=forms.TextInput(attrs={'autofocus': False}))


class SendVerifyEmailForm(forms.Form):
    email = forms.EmailField(label=_('Email address'))
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise ValidationError('Invalid email or password')

        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': False}),
    )


class GameGenreAdminForm(forms.ModelForm):

    class Meta:
        model = GameGenre
        fields = '__all__'
        labels = {
            'gamegenre': 'Genre',
        }


class GamePlatformAdminForm(forms.ModelForm):

    class Meta:
        model = GamePlatform
        fields = '__all__'
        labels = {
            'gameplatform': 'Platform',
        }



class EditProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class EditProfileAddressForm(forms.ModelForm):
    postal_code = forms.CharField(label='Postal code', required=False, max_length=9, min_length=9, help_text='Fill in Postal code to fill in State and Locality automatically.')

    class Meta:
        model = UserAddress
        exclude = ('user',)

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        regex = re.compile(r'^\d{5}-\d{3}$')
        if postal_code and not bool(regex.match(postal_code)):
            raise ValidationError('Invalid Postal code.')
        return postal_code
