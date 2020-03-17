from django import forms
from accounts.models import Candidate, Address
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

    def save(self, commit=True):
        instance = super(ScheduleForm, self).save(commit=False)
        instance.candidate_id = self.pk
        instance.hr = self.user
        instance.save()
        return super(ScheduleForm, self).save(commit=commit)


# class EvaluationForm(forms.Form)


class ApplyForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name', 'birth_date', 'mobile', 'email', 'applied_for']

    def __init__(self, *args, **kwargs):
        super(ApplyForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": 'form-control py-2'})


class AddressForm(forms.ModelForm):
    file = forms.ImageField(
        required=False,
        widget=forms.FileInput()
    )

    class Meta:
        model = Address
        fields = ['state', 'city', 'street', 'landmark', 'primary']
        widgets = {
            'state': forms.TextInput(attrs={'class': 'form-control py-2'}),
            'city': forms.TextInput(attrs={'class': 'form-control py-2'}),
            'street': forms.TextInput(attrs={'class': 'form-control py-2'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control py-2'}),
            'primary': forms.CheckboxInput(attrs={'class': 'form-control py-2'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
        self.fields['file'].widget.attrs.update(
            {
                'class': 'form-control py-2',
                'accept': 'image/*'
            }
        )
