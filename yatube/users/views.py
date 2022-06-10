from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from .forms import CreationForm
from core.views import registrarion_send_mail


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:main')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)

        registrarion_send_mail(form.cleaned_data.get('email'), username)
        return HttpResponseRedirect(self.get_success_url())


class Login(LoginView):
    template_name = 'users/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        next = self.request.META.get('HTTP_REFERER', '/')
        if (
            not next == 'https://dedau.pythonanywhere.com/auth/logout/'
            and not next == 'https://dedau.pythonanywhere.com/auth/login/'):
            context["next"] = next
        return context
