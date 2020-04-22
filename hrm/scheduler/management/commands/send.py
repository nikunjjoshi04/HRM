from django.core.management.base import BaseCommand, CommandError
from accounts.models import Candidate
from django.utils import timezone


class Command(BaseCommand):
    help = 'Type the help text here'

    def handle(self, *args, **options):
        c = Candidate.objects.get(id=3)
        last_name = c.last_name
        print(last_name)
        la = int(last_name)
        la += 1
        print(la)
        c.last_name = str(la)
        c.save()
        self.stdout.write('This was extremely simple!!!')