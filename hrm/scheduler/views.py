from builtins import super
from django.utils import timezone
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from accounts.models import Candidate, Address, Questions, Evaluation
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import ScheduleForm, ApplyForm, AddressForm, EvaluationForm, EvaluationCommentForm
from .models import Schedule
from django.utils.crypto import get_random_string
from django.forms import modelformset_factory, formset_factory
from extra_views import FormSetView
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


class ScheduleDetailView(FormSetView):
    template_name = 'scheduler/schedule_detail.html'
    form_class = EvaluationForm
    # initial = [{'question': 'QUE1'}, {'question': 'QUE2'}]
    factory_kwargs = {'extra': 0, 'max_num': None,
                      'can_order': False, 'can_delete': False}
    comment_form = EvaluationCommentForm

    def formset_valid(self, formset):
        schedule = Schedule.objects.get(id=self.kwargs.get('pk', None))
        for each in formset:
            question = each.cleaned_data.get('question', None)
            question_tag = each.cleaned_data.get('question_tag', None)
            questions_obj = Questions.objects.get(question=question)
            Evaluation.objects.create(
                question=questions_obj,
                candidate=schedule.candidate,
                question_tag=question_tag
            )
        form_comment = self.comment_form(self.request.POST)
        if form_comment.is_valid():
            comment = form_comment.cleaned_data.get('comment', None)
            status = form_comment.cleaned_data.get('status', None)
            schedule.comment = comment
            schedule.status = status
            schedule.save()
        return super(ScheduleDetailView, self).formset_valid(formset)

    def get_success_url(self):
        return reverse('scheduler:schedule_detail', args=[self.kwargs.get('pk', None)])

    def formset_invalid(self, formset):
        print(formset)
        return super(ScheduleDetailView, self).formset_invalid(formset)

    def get_initial(self):
        initial = []
        for each in Questions.objects.all():
            initial.append({'question': each.question})
        return initial

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk', None)
        context = super(ScheduleDetailView, self).get_context_data(**kwargs)
        context['schedule'] = Schedule.objects.get(id=pk)
        context['comment_form'] = self.comment_form
        return context
