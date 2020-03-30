from django.db import models
from accounts.models import Candidate, Questions
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.


class Schedule(models.Model):
    NOT_SPECIFY = 'not_specify'
    SELECTED = 'selected'
    REJECTED = 'rejected'
    STATUS_TAG = [
        (NOT_SPECIFY, 'Not Specify'),
        (SELECTED, 'Selected'),
        (REJECTED, 'Rejected'),
    ]
    TECHNICAL = 'technical'
    PRACTICAL = 'practical'
    HR = 'hr'
    INTERVIEW_TYPE = [
        (TECHNICAL, 'Technical Round'),
        (PRACTICAL, 'Practical Round'),
        (HR, 'HR Round'),
    ]

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidate_schedule')
    hr = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hr')
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interviewer')
    schedule_time = models.DateTimeField()
    interview_type = models.CharField(max_length=50, choices=INTERVIEW_TYPE)
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(default=NOT_SPECIFY, choices=STATUS_TAG, max_length=50)

    def __str__(self):
        return '{} - {}'.format(self.candidate, self.status)

    def get_absolute_url(self):
        return reverse('scheduler:schedule_detail', args=[self.pk])


class Evaluation(models.Model):
    NOT_SPECIFIED = 'not_specified'
    UNSATISFACTORY = 'unsatisfactory'
    SATISFACTORY = 'satisfactory'
    AVERAGE = 'average'
    ABOVE_AVERAGE = 'above_average'
    EXCEPTIONAL = 'exceptional'
    QUESTION_TAG = [
        (NOT_SPECIFIED, 'Not Specified'),
        (UNSATISFACTORY, 'Unsatisfactory'),
        (SATISFACTORY, 'satisfactory'),
        (AVERAGE, 'Average'),
        (ABOVE_AVERAGE, 'Above Average'),
        (EXCEPTIONAL, 'Exceptional'),
    ]
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    question_tag = models.CharField(default=NOT_SPECIFIED, choices=QUESTION_TAG, max_length=50)

    def __str__(self):
        return '{} - {}'.format(self.question, self.question_tag)
