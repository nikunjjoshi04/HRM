from dataclasses import fields
import datetime
from django.utils import timezone
from django import forms
from accounts.models import Candidate, Address, Questions, Evaluation
from .models import Schedule
from django.contrib.auth.models import User
from django.forms import modelformset_factory, formset_factory, BaseFormSet


class ScheduleForm(forms.ModelForm):
    interview_type = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control py-2'
            }
        )
    )

    class Meta:
        model = Schedule
        fields = ['interviewer', 'schedule_time']
        widgets = {
            'interviewer': forms.Select(attrs={'class': 'form-control py-2'}),
            'schedule_time': forms.DateTimeInput(attrs={'class': 'form-control py-2'}),
        }

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        self.user = kwargs.pop('user', None)
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['interviewer'].queryset = User.objects.filter(is_staff=False)
        self.fields['interview_type'].choices = Candidate.STATUS_TAG[1:]

    def save(self, commit=True):
        instance = super(ScheduleForm, self).save(commit=False)
        instance.candidate_id = self.pk
        instance.hr = self.user
        instance.save()
        return super(ScheduleForm, self).save(commit=commit)


class EvaluationCommentForm(forms.Form):
    status = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control py-2'
            }
        )
    )
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control py-2',
                'rows': '5'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(EvaluationCommentForm, self).__init__(*args, **kwargs)
        self.fields['status'].choices = Schedule.STATUS_TAG


class EvaluationForm(forms.Form):
    question = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control py-2',
                'readonly': True
            }
        )
    )
    question_tag = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(EvaluationForm, self).__init__(*args, **kwargs)
        self.fields['question_tag'].choices = Evaluation.QUESTION_TAG


class BaseEvaluationFormSet(BaseFormSet):

        def clean(self):
            if any(self.errors):
                return
            titles = []
            for form in self.forms:
                if self.can_delete and self._should_delete_form(form):
                    continue
                print(form.cleaned_data)
                title = form.cleaned_data.get('title')
                if title in titles:
                    raise forms.ValidationError("Articles in a set must have distinct titles.")
                titles.append(title)


class ApplyForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name', 'birth_date', 'mobile', 'email', 'applied_for']

    def __init__(self, *args, **kwargs):
        super(ApplyForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": 'form-control py-2'})


class AddressForm(forms.ModelForm):
    file = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control py-2',
                'accept': '.pdf, .docx'
            }
        )
    )

    experience = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control py-2'
            }
        )
    )

    class Meta:
        model = Address
        fields = ['state', 'city', 'street', 'landmark']
        widgets = {
            'state': forms.TextInput(attrs={'class': 'form-control py-2'}),
            'city': forms.TextInput(attrs={'class': 'form-control py-2'}),
            'street': forms.TextInput(attrs={'class': 'form-control py-2'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control py-2'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
        self.fields['experience'].choices = Candidate.EXPERIENCE_CHOICE
