from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import re


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('phone',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('phone',)


class InviteProfile(forms.ModelForm):
    another_invite = forms.CharField(label='Инвайт-код', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('another_invite',)

    def clean_another_invite(self):
        another_invite = self.cleaned_data['another_invite']
        if re.match(r"^\+?1?\d{6}$", another_invite):
            raise ValidationError('Инвайт не может состоять только из цифр')
        if re.match(r"^\+?1?[a-zA-Z]{6}$", another_invite):
            raise ValidationError('Инвайт не может состоять только из букв')
        if re.match(r"^\+?1?[а-яА-Я]{6}$", another_invite):
            raise ValidationError('Инвайт не может содержать кириллицу')
        return another_invite


class UserRegisterForm(UserCreationForm):
    phone = forms.CharField(label='Телефон', error_messages={'invalid': 'Пожалуйста, введите корректный номер телефона'}, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    class Meta:
        model = CustomUser
        fields = ('phone', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    error_messages = {
        "invalid_login": _(
            "Пожалуйста введите корректный номер телефона и пароль. Если вы ошиблись номером "
            "нужно получить код подтверждения снова"
        ),
        "inactive": _("Этот аккаунт не активен."),
    }


class ConfCodeForm(forms.Form):
    code = forms.CharField(required=True, label='Код подтверждения', error_messages={'invalid': 'Ошибка кода подтверждения'}, widget=forms.TextInput(attrs={'class': 'form-control'}))


class GetPhone(forms.Form):
    phoneRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone = forms.CharField(validators=[phoneRegex], label='Телефон', widget=forms.TextInput(attrs={'class': 'form-control'}))


class UserConf(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


class NewProfile(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name')
