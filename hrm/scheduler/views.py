from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from accounts.models import Candidate, Address
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import ScheduleForm, ApplyForm, AddressForm
from .models import Schedule
from django.utils.crypto import get_random_string
from django.forms import modelformset_factory, formset_factory
from .utils import URL
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.


class Apply(FormView):
    form_class = ApplyForm
    template_name = 'scheduler/apply.html'

    def form_valid(self, form):
        token = get_random_string(length=8)
        instance = form.save(commit=False)
        instance.token = token
        instance.save()
        self.success_url = reverse('scheduler:verify', args=[token])
        # data = URL.encryption(self, pk=instance.order.id)
        # print("B_SEND :-  ", data)
        # msg = 'http://127.0.0.1:8000/scheduler/verify/' + str(data)
        # email = 'nikunj.joshi@trootech.com'
        # email1 = instance.order.customer.email
        # send_mail("Customer Test", msg, settings.EMAIL_HOST_USER, [email, email1], fail_silently=False)
        return super(Apply, self).form_valid(form=form)


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
    permission_required = [
        'scheduler.change_schedule',
        'scheduler.view_schedule'
    ]
    login_url = 'accounts:login'
    permission_denied_message = 'Not Allow...!!!'
    model = Schedule
    template_name = 'scheduler/interviewer_schedule_list.html'


class ScheduleDetailView(Detail, FormView):
    permission_required = [
        'scheduler.change_schedule',
        'scheduler.view_schedule'
    ]
    login_url = 'accounts:login'
    permission_denied_message = 'Not Allow...!!!'
    model = Schedule
    template_name = 'scheduler/interviewer_schedule_detail.html'
    form_class = ScheduleForm
    success_url = reverse_lazy('scheduler:interviewer_schedule_detail')


class VerifyView(FormView):
    # AddressFormSet = formset_factory(form=AddressForm, extra=2)
    form_class = AddressForm
    template_name = 'scheduler/verify.html'
    success_url = reverse_lazy('accounts:home')

    def form_valid(self, form):
        # print(self.kwargs['token'])
        # token = self.kwargs.get('token', None)
        # candidate = Candidate.objects.get(token=token)


        return super(VerifyView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        token = self.kwargs.get('token', None)
        context = super(VerifyView, self).get_context_data(**kwargs)
        context['candidate'] = Candidate.objects.get(token=token)
        return context
