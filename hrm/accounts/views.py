from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import reverse
from django.conf import settings

# Create your views here.


class HomeView(TemplateView):
    template_name = 'registration/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data()
        return context


class LoginView(LoginView):

    def get_success_url(self):
        url = self.get_redirect_url()
        print(self.request.user.is_staff)
        if self.request.user.is_staff:
            return url or reverse('scheduler:candidate_list')
        else:
            return url or reverse('scheduler:')
