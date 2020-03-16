from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from accounts.models import Candidate
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import ScheduleForm
from .models import Schedule


# Create your views here.


class List(PermissionRequiredMixin, ListView):
    permission_required = None
    login_url = 'accounts:login'
    permission_denied_message = 'Not Allow...!!!'
    model = None
    template_name = None


class Detail(PermissionRequiredMixin, DetailView):
    permission_required = None
    login_url = 'accounts:login'
    permission_denied_message = 'Not Allow...!!!'
    model = None
    template_name = None


class CandidateListView(List):
    permission_required = ['accounts.view_candidate']
    login_url = 'accounts:login'
    permission_denied_message = 'Not Allow...!!!'
    model = Candidate
    template_name = 'scheduler/candidate_list.html'


class CandidateDetailView(Detail, FormView):
    permission_required = [
        'accounts.view_candidate',
        'accounts.change_candidate',
    ]
    login_url = 'accounts:login'
    permission_denied_message = 'Not Allow...!!!'
    model = Candidate
    template_name = 'scheduler/candidate_detail.html'
    form_class = ScheduleForm
    success_url = reverse_lazy('scheduler:candidate_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CandidateDetailView, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs.get('pk', None)
        kwargs['user'] = self.request.user
        print(kwargs['pk'])
        return kwargs


class ScheduleListView(PermissionRequiredMixin, ListView):
    permission_required = ['accounts.view_candidate']
    login_url = 'accounts:login'
    permission_denied_message = 'Not Allow...!!!'
    model = Schedule
    template_name = 'scheduler/interviewer_candidate_list.html'
