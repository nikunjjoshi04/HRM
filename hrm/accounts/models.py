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
        return '{} {}'.format(self.post, self.technologies)


class Candidate(models.Model):
    SHORTLIST = 'shortlist'
    TECHNICAL = 'technical'
    PRACTICAL = 'practical'
    HR = 'hr'
    REJECTED = 'rejected'
    SELECTED = 'selected'
    STATUS_TAG = [
        (SHORTLIST, 'Short Listed'),
        (TECHNICAL, 'For Technical Round'),
        (PRACTICAL, 'For Practical Round'),
        (HR, 'For HR Round'),
        (REJECTED, 'Rejected'),
        (SELECTED, 'Selected'),
    ]
    EXPERIENCE_CHOICE = [
        ('2', '0 - 1'),
        ('1 - 2', '1 - 2'),
        ('2 - 3', '2 - 3'),
        ('3 - Above', '3 - Above'),
    ]
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField()
    mobile = PhoneNumberField()
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=30, null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    applied_for = models.ForeignKey(Vacancies, on_delete=models.CASCADE)
    status = FSMField(default=SHORTLIST, choices=STATUS_TAG)
    experience = models.CharField(default='0 - 1', choices=EXPERIENCE_CHOICE, max_length=20)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('scheduler:candidate_detail', args=[self.pk])

    @transition(field='status', source=SHORTLIST, target=TECHNICAL)
    def technical_round(self):
        pass

    @transition(field='status', source=TECHNICAL, target=PRACTICAL)
    def practical_round(self):
        pass

    @transition(field='status', source=PRACTICAL, target=HR)
    def hr_round(self):
        pass

    @transition(field='status', source=HR, target=SELECTED)
    def select(self):
        pass

    @transition(field='status', source=[SHORTLIST, TECHNICAL, PRACTICAL, HR], target=REJECTED)
    def reject(self):
        pass


class Address(models.Model):
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='address')

    def __str__(self):
        return '{} - {}'.format(self.state, self.city)


class Questions(models.Model):
    question = models.CharField(max_length=50)

    def __str__(self):
        return self.question
