from django.core.management import BaseCommand

from mail.send_msg import send_customer


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_customer()
