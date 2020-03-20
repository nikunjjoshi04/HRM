from builtins import super
from django.utils import timezone
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from accounts.models import Candidate, Address, Questions, Evaluation
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import ScheduleForm, ApplyForm, AddressForm, EvaluationForm, EvaluationCommentForm, BaseEvaluationFormSet
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


class VerifyView(FormView):
    # AddressFormSet = formset_factory(form=AddressForm, extra=2)
    form_class = AddressForm
    template_name = 'scheduler/verify.html'

    def form_valid(self, form):
        experience = form.cleaned_data['experience']
        candidate = Candidate.objects.get(token=self.kwargs.get('token', None))
        resume = self.request.FILES['file']
        candidate.resume = resume
        candidate.experience = experience
        candidate.save()
        form.instance.candidate = candidate
        form.save()
        return super(VerifyView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(VerifyView, self).get_context_data(**kwargs)
        context['candidate'] = Candidate.objects.get(token=self.kwargs.get('token', None))
        return context

    def get_success_url(self):
        return reverse('scheduler:profile', args=[self.kwargs.get('token', None)])


class ProfileView(TemplateView):
    template_name = 'scheduler/candidate_profile.html'

    def get_context_data(self, **kwargs):
        kwargs = super(ProfileView, self).get_context_data()
        kwargs['candidate'] = Candidate.objects.get(token=self.kwargs.get('token', None))
        return kwargs


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


class HRDashboardView(TemplateView):
    permission_required = ['accounts.view_candidate']
    login_url = 'accounts:login'
    permission_denied_message = 'Not Allow...!!!'
    model = Candidate
    template_name = 'scheduler/hr_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(HRDashboardView, self).get_context_data()
        context['candidates'] = Candidate.objects.all()
        context['schedules'] = Schedule.objects.select_related('candidate').all()
        return context


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
    # success_url = reverse_lazy('scheduler:hr_dashboard')

    def form_valid(self, form):
        interview_type = form.cleaned_data['interview_type']
        print(interview_type)
        candidate = Candidate.objects.get(id=self.kwargs.get('pk', None))
        if interview_type == Candidate.TECHNICAL:
            candidate.technical_round()
        elif interview_type == Candidate.PRACTICAL:
            candidate.practical_round()
        elif interview_type == Candidate.HR:
            candidate.hr_round()
        elif interview_type == Candidate.REJECTED:
            candidate.reject()
        else:
            candidate.status = Candidate.SHORTLIST
        candidate.save()
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CandidateDetailView, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs.get('pk', None)
        kwargs['user'] = self.request.user
        print(kwargs['pk'])
        return kwargs

    def get_success_url(self):
        return reverse('scheduler:candidate_detail', args=[self.kwargs.get('pk', None)])


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
    EvaluationFormSet = formset_factory(EvaluationForm, formset=BaseEvaluationFormSet, extra=0)
    formset = EvaluationFormSet(
        initial=[
            {
                'question': "{}".format(i),
            }for i in Questions.objects.all()
        ]
    )
    login_url = 'accounts:login'
    permission_denied_message = 'Not Allow...!!!'
    model = Schedule
    template_name = 'scheduler/schedule_detail.html'
    form_class = EvaluationCommentForm

    def form_valid(self, form):
        print(form.cleaned_data)
        print(self.formset)
        if self.formset.is_valid():
            print('valid')
            print('valid')
            for each in self.formset.ordered_forms:
                print(each.cleaned_data)
        return super(ScheduleDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ScheduleDetailView, self).get_context_data()
        context['questions'] = Questions.objects.all()
        context['question_tag'] = Evaluation.QUESTION_TAG
        context['evaluation_form'] = self.formset
        return context

    def get_success_url(self):
        return reverse('scheduler:schedule_detail', args=[self.kwargs.get('pk', None)])