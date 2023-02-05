import datetime
from django.conf import settings
from django.core.mail import send_mail
from mail.models import Sending, Attempt


def send_customer(*args, **kwargs):
    sending_item = Sending.objects.all()
    for i in sending_item:
        if (
                i.status == Sending.CREATED or i.status == Sending.LAUNCHED) and i.start_date == datetime.date.today() and i.finish_date >= datetime.date.today() and i.send_time >= datetime.datetime.now().time():
            i.status = Sending.LAUNCHED
            i.save()

            try:
                res = send_mail(
                    subject=i.sending_msg.title,
                    message=i.sending_msg.text,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[i.customer_lst.email],
                    fail_silently=False
                )
                if res:
                    i.status = Sending.COMPLETED
                    i.save()
                Attempt.objects.create(
                    attempt_status=i.status,
                    answer=200,
                )

            except Exception as err:
                Attempt.objects.create(
                    attempt_status=i.status,
                    answer=err,
                )