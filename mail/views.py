from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic import DeleteView, DetailView
from mail.models import Customer, Sending, Message
from django.core.mail import send_mail


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
