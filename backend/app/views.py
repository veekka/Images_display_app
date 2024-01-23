from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.viewsets import ModelViewSet
from .forms import *
from .models import *
from .serializers import ImageSerializer


class AppHomeView(ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImageSerializer


class ImagesApp(ListView):
    model = Images
    template_name = 'app/indexVue.html'

    def get_context_data(self, **kwargs):
        context = super(ImagesApp, self).get_context_data(**kwargs)
        context['title'] = 'Images'
        return context


@login_required(login_url='login')
def upload_images(request):
    if request.method == 'POST':
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False) #add for DRF
            image.user_id = request.user.id #add for DRF
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = AddImageForm

    return render(request, 'app/add_image.html', {'form': form})


class UpdateImage(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = 'next'

    model = Images
    template_name = 'app/image_edit.html'
    fields = ['photo', 'description', 'slug']
    success_url = '/'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.user == self.request.user:
            raise PermissionDenied
        return obj

    # def get_success_url(self):
    #     return self.object.get_absolute_url()


class DeleteImage(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    redirect_field_name = 'next'

    model = Images
    template_name = 'app/image_delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.user == self.request.user:
            raise PermissionDenied
        return obj


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'app/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'app/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Log in'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class UserPasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "app/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Change password'
        return context

    def get_success_url(self):
        return reverse_lazy('home')
