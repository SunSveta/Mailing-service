from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DetailView

from users.forms import CustomUserCreationForm, CustomLoginForm, CustomPasswordResetForm
from users.models import User
from users.services import set_verify_token_and_send_mail, generate_password_and_end_mail


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = CustomLoginForm


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:register_success')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            set_verify_token_and_send_mail(self.object)
        return super().form_valid(form)


class UsersListView(ListView):
    model = User
    template_name = 'users/user_list.html'



class CreateSuccessView(TemplateView):
    template_name = 'users/create_success.html'


class VerifySuccessView(TemplateView):
    template_name = 'users/verify_success.html'

def verify_email(request, token):
    current_user = User.objects.filter(token=token).first()
    if current_user:
        now = datetime.now(pytz.timezone(settings.TIME_ZONE))
        if now > current_user.token_expired:
            current_user.delete()
            return render(request, 'users/verify_token_expired.html')

        current_user.is_active = True
        current_user.token = None
        current_user.token_expired = None
        current_user.save()
        return redirect('users:login')

    return render(request, 'users/verify_failed.html')


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')
    email_template_name = 'users/email_reset.html'
    from_email = settings.EMAIL_HOST_USER


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/reset_done.html'


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/reset_complete.html'


def simple_reset_password(request):
    if request.method == 'POST':
        current_user = User.objects.filter(email=request.POST.get('email')).first()
        if current_user:
            generate_password_and_end_mail(current_user)
    return render(request, 'users/simple_reset.html')


def confirm_new_generated_password(request):
    current_user = User.objects.filter(email=request.GET.get('email')).first()
    current_user.password = current_user.my_password
    current_user.my_password = None
    current_user.save()

    return redirect(...)

@permission_required('users.change_status')
def user_status_change(request, pk):

    current_user = get_object_or_404(User, pk=pk)
    if current_user.is_superuser:
        return HttpResponseForbidden()
    if current_user.is_active:
        current_user.is_active = False
    else:
        current_user.is_active = True
    current_user.save()

    return redirect(request.META.get('HTTP_REFERER'))