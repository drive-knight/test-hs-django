from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm, GetPhone, NewProfile, InviteProfile, ConfCodeForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.views.generic.edit import FormMixin
from django.views.generic.detail import DetailView
from .utils import get_random_string
from django.urls import reverse_lazy
import time


def get_phone(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            form = GetPhone(data=request.POST)
            if form.is_valid():
                request.session['code'] = get_random_string(2)
                request.session['phone'] = form.cleaned_data['phone']
                time.sleep(1)
                return redirect('users:entrance')
        else:
            form = GetPhone()
        return render(request, 'entry.html', {'form': form})
    else:
        return redirect('users:profile', pk=CustomUser.objects.get(phone=request.user).id)


def entrance(request):
    if request.user.is_authenticated:
        return redirect('users:profile', pk=CustomUser.objects.get(phone=request.user).id)
    if request.method == 'POST':
        form = ConfCodeForm(data=request.POST)
        if form.is_valid():
            if form.cleaned_data['code'] == request.session['code']:
                if CustomUser.objects.filter(phone=request.session['phone']).exists():
                    return redirect('users:auth')
                else:
                    return redirect('users:register')
            else:
                messages.error(request, 'Пожалуйста, введите корректный код подтверждения')
    else:
        form = ConfCodeForm()
    return render(request, 'entrance.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('users:profile', pk=CustomUser.objects.get(phone=request.user).id)
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:new-profile')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {"form": form})


def auth(request):
    if request.user.is_authenticated:
        return redirect('users:profile', pk=CustomUser.objects.get(phone=request.user).id)
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            if str(CustomUser.objects.get(phone=form.cleaned_data['username'])) == str(CustomUser.objects.get(
                    phone=request.session['phone'])):
                user = form.get_user()
                login(request, user)
                if CustomUser.objects.filter(phone=form.cleaned_data['username']).values_list('another_invite')[0][
                0] is None \
                    and len(list(CustomUser.objects.filter(phone=form.cleaned_data['username'])
                            .values_list('first_name')[0][0])) == 0:
                    return redirect('users:new-profile')
                else:
                    return redirect('users:profile', pk=CustomUser.objects.get(phone=form.cleaned_data['username']).id)
    else:
        form = UserLoginForm()
    return render(request, 'auth.html', {'form': form})


@login_required(login_url='users:get-phone')
def new_profile(request):
    if len(list(CustomUser.objects.filter(phone=request.user).values_list('first_name'))[0][0]) == 0:
        if request.method == 'POST':
            form = NewProfile(request.POST)
            if form.is_valid():
                CustomUser.objects.filter(phone=request.user).update(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    code_invite=get_random_string(3))
                return redirect('users:profile', pk=CustomUser.objects.get(phone=request.user).id)
        else:
            form = NewProfile()
        return render(request, 'new_profile.html', {'form': form})
    else:
        return redirect('users:profile', pk=CustomUser.objects.get(phone=request.user).id)


def user_logout(request):
    logout(request)
    return redirect('users:get-phone')


class UserProfile(FormMixin, DetailView):
    form_class = InviteProfile
    model = CustomUser
    template_name = 'profile.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.id})

    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.request.user.id)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        if list(CustomUser.objects.filter(pk=self.kwargs['pk']).values_list('another_invite'))[0][0] is None:
            CustomUser.objects.filter(pk=self.kwargs['pk']).update(
                another_invite=form.cleaned_data['another_invite'])
        return super(UserProfile, self).form_valid(form)



