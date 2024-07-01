from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

#  создадим собственный класс для формы регистрации
#  сделаем его наследником предустановленного класса UserCreationForm

class CreationForm(UserCreationForm):
    username = forms.CharField(label="Логин")
    email = forms.EmailField(label="Адрес электронной почты", required=True)
    first_name = forms.CharField(label="Имя", required=True)
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        # укажем модель, с которой связана создаваемая форма
        model = User
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ("first_name", "username", "email", "password1", "password2")

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Старый пароль',
        strip=False, 
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    new_password1 = forms.CharField(
        label='Новый пароль',
        strip=False, 
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='Ваш пароль должен содержать не менее 8 символов и не доджен быть похож другие ваши личные данные',
    )
    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        strip=False, 
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Новый пароль',
        strip=False, 
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='Ваш пароль должен содержать не менее 8 символов и не доджен быть похож другие ваши личные данные',
    )
    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        strip=False, 
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    