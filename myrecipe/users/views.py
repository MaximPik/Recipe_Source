from django.shortcuts import render, redirect
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView

#  импортируем CreateView, чтобы создать ему наследника
from django.views.generic import CreateView

#  функция reverse_lazy позволяет получить URL по параметру "name" функции path()
#  берём, тоже пригодится
from django.urls import reverse_lazy

#  импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm, CustomPasswordChangeForm, CustomSetPasswordForm

class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login") #  где login — это параметр "name" в path()
    template_name = "signup.html"


def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html')

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    