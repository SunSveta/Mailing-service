from mail.models import Sending, Customer


def count_sending_all(*args, **kwargs):

    return Sending.objects.all().count()


def count_active_sending(*args, **kwargs):
    return Sending.objects.filter(status='created').count()


def count_customer_all(*args, **kwargs):
    return Customer.objects.all().count()