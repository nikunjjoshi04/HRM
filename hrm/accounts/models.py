from django.db import models
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django_fsm import FSMField, transition

# Create your models here.


class Vacancies(models.Model):
    post = models.CharField(max_length=50)
    technologies = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.post


class Candidate(models.Model):
    SHORTLIST = 'shortlist'
    TECHNICAL = 'technical'
    PRACTICAL = 'practical'
    HR = 'hr'
    REJECTED = 'rejected'
    STATUS_TAG = [
        (SHORTLIST, 'Short Listed'),
        (TECHNICAL, 'For Technical Round'),
        (PRACTICAL, 'For Practical Round'),
        (HR, 'For HR Round'),
        (REJECTED, 'Rejected'),
    ]
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField()
    mobile = PhoneNumberField()
    email = models.EmailField()
    token = models.CharField(max_length=30)
    resume = models.FileField()
    applied_for = models.ForeignKey(Vacancies, on_delete=models.CASCADE)
    status = FSMField(default=SHORTLIST, choices=STATUS_TAG)

    def __str__(self):
        return '{} - {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('scheduler:candidate_detail', args=[self.pk])

    @transition(field='interview_type', source=SHORTLIST, target=TECHNICAL)
    def technical_round(self):
        pass

    @transition(field='interview_type', source=TECHNICAL, target=PRACTICAL)
    def practical_round(self):
        pass

    @transition(field='interview_type', source=PRACTICAL, target=HR)
    def hr_round(self):
        pass

    @transition(field='interview_type', source=[SHORTLIST, TECHNICAL, PRACTICAL, HR], target=REJECTED)
    def reject(self):
        pass


class Address(models.Model):
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    primary = models.BooleanField(default=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.state, self.city)


class Questions(models.Model):
    question = models.CharField(max_length=50)

    def __str__(self):
        return self.question


class Evaluation(models.Model):
    NOT_SPECIFIED = 'not_specified'
    UNSATISFACTORY = 'unsatisfactory'
    SATISFACTORY = 'satisfactory'
    AVERAGE = 'average'
    ABOVE_AVERAGE = 'above_average'
    EXCEPTIONAL = 'exceptional'
    QUESTION_TAG = [
        (UNSATISFACTORY, 'Unsatisfactory'),
        (SATISFACTORY, 'satisfactory'),
        (AVERAGE, 'Average'),
        (ABOVE_AVERAGE, 'Above Average'),
        (EXCEPTIONAL, 'Exceptional'),
    ]
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    question_tag = models.CharField(default=NOT_SPECIFIED, choices=QUESTION_TAG, max_length=50)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.question, self.question_tag)
