from django.core.management.base import BaseCommand, CommandError
from aion.models import AccountManager

class Command(BaseCommand):
    help = 'Checks and sets accounts if they should be expired.'

#    def add_arguments(self, parser):
#        parser.add_argument('poll_id', nargs='+', type=int)cf6d038c13e9

    def handle(self, *args, **options):
        AccountHandler = AccountManager()
        AccountHandler.check_accounts()
        
        
#schedule task for windows
    # type at cmd: At 16:22:00PM /every:M,T,W,TH,F,SA,SU python manage.py checkaccounts
