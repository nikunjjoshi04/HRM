import json
from django.core.serializers import serialize
from builtins import super
from django.utils import timezone
from django.shortcuts import render, reverse, HttpResponseRedirect, redirect
from django.urls import reverse_lazy
from accounts.models import Candidate, Address, Questions
from django.views.generic import TemplateView, DetailView, ListView, FormView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import ScheduleForm, ApplyForm, AddressForm, EvaluationForm, EvaluationCommentForm
from .models import Schedule, Evaluation
from django.utils.crypto import get_random_string
from django.forms import modelformset_factory, formset_factory
from extra_views import FormSetView
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator

# Create your views here.


class Apply(FormView):
    form_class = ApplyForm
    template_name = 'scheduler/apply.html'
    success_url = None

    def form_valid(self, form):
        token = get_random_string(length=8)
        instance = form.save(commit=False)
        instance.token = token
        instance.save()
        self.success_url = reverse('scheduler:success_apply', args=[token])
        msg = 'http://127.0.0.1:8000/scheduler/verify/' + str(token)
        email = 'nikunjjoshi04@gmail.com'
        send_mail("Apply Test", msg, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        return super(Apply, self).form_valid(form=form)


class SuccessApply(TemplateView):
    template_name = 'scheduler/success_apply.html'

    def get_context_data(self, **kwargs):
        context = super(SuccessApply, self).get_context_data(**kwargs)
        context['candidate'] = Candidate.objects.get(token=self.kwargs.get('token', None))
        return context


class VerifyView(FormView):
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


@method_decorator(xframe_options_exempt, name='get')
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

    def form_valid(self, form):
        interview_type = form.cleaned_data['interview_type']
        candidate = Candidate.objects.get(id=self.kwargs.get('pk', None))
        if interview_type == Candidate.TECHNICAL:
            candidate.technical_round()
        elif interview_type == Candidate.PRACTICAL:
            candidate.practical_round()
        elif interview_type == Candidate.HR:
            candidate.hr_round()
        else:
            candidate.status = Candidate.SHORTLIST
        candidate.save()
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CandidateDetailView, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs.get('pk', None)
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('scheduler:candidate_detail', args=[self.kwargs.get('pk', None)])

    def get_context_data(self, **kwargs):
        context = super(CandidateDetailView, self).get_context_data(**kwargs)
        context['hrs'] = User.objects.filter(is_staff=True, is_superuser=False)
        context['interviewer'] = User.objects.filter(is_staff=False, is_superuser=False)
        return context


class InterviewerDashboardView(PermissionRequiredMixin, ListView):
    permission_required = [
        'scheduler.change_schedule',
        'scheduler.view_schedule'
    ]
    login_url = 'accounts:login'
    permission_denied_message = 'Not Allow...!!!'
    model = Schedule
    template_name = 'scheduler/interviewer_dashboard.html'


class ScheduleDetailView(View):
    def get(self, request, pk):
        schedule = Schedule.objects.get(id=self.kwargs.get('pk', None))
        if schedule.interview_type == Schedule.TECHNICAL:
            print(schedule.interview_type)
            return redirect(reverse('scheduler:technical_view', args=[self.kwargs.get('pk', None)]))
        else:
            print(schedule.interview_type)
            return redirect(reverse('scheduler:practical_view', args=[self.kwargs.get('pk', None)]))


class PracticalView(Detail, FormView):
    permission_required = [
        'scheduler.change_schedule',
        'scheduler.view_schedule'
    ]
    login_url = 'accounts:login'
    permission_denied_message = 'Not Allow...!!!'
    model = Schedule
    template_name = 'scheduler/practical_schedule_detail.html'
    form_class = EvaluationCommentForm

    def form_valid(self, form):
        comment = form.cleaned_data['comment']
        status = form.cleaned_data['status']
        schedule = Schedule.objects.get(id=self.kwargs.get('pk', None))
        schedule.comment = comment
        schedule.status = status
        if status == Schedule.REJECTED:
            schedule.candidate.status = Candidate.REJECTED
            schedule.candidate.save()
        if schedule.interview_type == Schedule.HR and status == Schedule.SELECTED:
            schedule.candidate.select()
            schedule.candidate.save()
        schedule.save()
        return super(PracticalView, self).form_valid(form)

    def get_success_url(self):
        return reverse('scheduler:schedule_detail', args=[self.kwargs.get('pk', None)])


class TechnicalView(FormSetView):
    template_name = 'scheduler/technical_schedule_detail.html'
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
                schedule=schedule,
                question_tag=question_tag
            )
        form_comment = self.comment_form(self.request.POST)
        if form_comment.is_valid():
            comment = form_comment.cleaned_data.get('comment', None)
            status = form_comment.cleaned_data.get('status', None)
            schedule.comment = comment
            schedule.status = status
            if status == Schedule.REJECTED:
                schedule.candidate.status = Candidate.REJECTED
                schedule.candidate.save()
            schedule.save()
        return super(TechnicalView, self).formset_valid(formset)

    def get_success_url(self):
        return reverse('scheduler:schedule_detail', args=[self.kwargs.get('pk', None)])

    def formset_invalid(self, formset):
        print(formset)
        return super(TechnicalView, self).formset_invalid(formset)

    def get_initial(self):
        initial = []
        for each in Questions.objects.all():
            initial.append({'question': each.question})
        return initial

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk', None)
        context = super(TechnicalView, self).get_context_data(**kwargs)
        try:
            context['schedule'] = Schedule.objects.get(id=pk)
        except Exception as e:
            context['schedule'] = None
            print('Error Is :- ', e, type(e))
        context['comment_form'] = self.comment_form
        return context


class ScheduleDeleteView(DeleteView):
    model = Schedule

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        candidate = self.object.candidate
        self.object.delete()
        try:
            status = candidate.candidate_schedule.last().interview_type
        except AttributeError:
            status = Candidate.SHORTLIST
        candidate.status = status
        candidate.save()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse('scheduler:candidate_detail', args=[self.kwargs.get('candidate_id', None)])


class Search(View):

    def get(self, request, *args, **kwargs2):
        q = request.GET.get('q', None)
        data = Candidate.objects.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(email__icontains=q) |
            Q(mobile__icontains=q)
        )
        lst = list(data.values('id', 'first_name', 'last_name', 'mobile', 'email'))
        return JsonResponse({'data': lst})
