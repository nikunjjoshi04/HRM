from django.db import models
from accounts.models import Candidate
from django.contrib.auth.models import User

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

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    hr = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hr')
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interviewer')
    schedule_time = models.DateTimeField()
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(default=NOT_SPECIFY, choices=STATUS_TAG, max_length=50)

    def __str__(self):
        return '{} - {}'.format(self.candidate, self.status)



