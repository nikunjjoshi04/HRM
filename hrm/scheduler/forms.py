from django import forms
from accounts.models import Candidate
from .models import Schedule
from django.contrib.auth.models import User


class ScheduleForm(forms.ModelForm):
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
        print(self.pk)
        print(self.user)

    def save(self, commit=True):
        instance = super(ScheduleForm, self).save(commit=False)
        instance.candidate_id = self.pk
        instance.hr = self.user
        instance.save()
        return super(ScheduleForm, self).save(commit=commit)