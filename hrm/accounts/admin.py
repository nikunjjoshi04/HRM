from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Vacancies)
admin.site.register(Address)
admin.site.register(Questions)
admin.site.register(Evaluation)


class AddressInline(admin.StackedInline):
    model = Address
    extra = 2


class CandidateAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Status', {'fields': ['status']}),
        ('Info', {'fields': ['first_name', 'last_name', 'birth_date']}),
        ('Contact', {'fields': ['email', 'mobile']}),
        ('Other', {'fields': ['token', 'resume', 'applied_for']}),
    ]
    inlines = [AddressInline]


admin.site.register(Candidate, CandidateAdmin)
