from dataclasses import fields

from django import forms
from accounts.models import Candidate, Address, Questions, Evaluation
from .models import Schedule
from django.contrib.auth.models import User


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


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['question', 'schedule_time']
        # widgets = {
        #     'interviewer': forms.Select(attrs={'class': 'form-control py-2'}),
        #     'schedule_time': forms.DateTimeInput(attrs={'class': 'form-control py-2'}),
        # }


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
