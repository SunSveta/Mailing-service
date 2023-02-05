from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic import DeleteView, DetailView
from mail.models import Customer, Sending, Message, Attempt
from django.core.mail import send_mail
import datetime


def home(request):
    return render(request, 'mail/home.html')


class CustomerListView(ListView):
    model = Customer


class CustomerCreateView(CreateView):
    model = Customer
    fields = ('name', 'email', 'comment')
    success_url = reverse_lazy('mail:customer')


class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ('name', 'email', 'comment')
    success_url = reverse_lazy('mail:customer')


class CustomerDetailView(DetailView):
    model = Customer


class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('mail:customer')


class MessageListView(ListView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    fields = ('title', 'text')
    success_url = reverse_lazy('mail:message')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('title', 'text')
    success_url = reverse_lazy('mail:message')


class MessageDetailView(DetailView):
    model = Message


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mail:message')


class SendingListView(ListView):
    model = Sending


class SendingCreateView(CreateView):
    model = Sending
    fields = '__all__'
    success_url = reverse_lazy('mail:sending')


class SendingUpdateView(UpdateView):
    model = Sending
    fields = '__all__'
    success_url = reverse_lazy('mail:sending')


class SendingDetailView(DetailView):
    model = Sending


class SendingDeleteView(DeleteView):
    model = Sending
    success_url = reverse_lazy('mail:sending')


def statistic(request):
    context = {
        'object_list': Attempt.objects.all()
    }
    return render(request, 'mail/statistic.html', context)


def send_customer(request):
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

    return redirect(reverse('mail:sending'))
