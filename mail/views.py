from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.views.generic import DeleteView, DetailView

from blog.models import Blog
from mail.models import Customer, Sending, Message, Attempt
from django.core.mail import send_mail
import datetime

from mail.services import count_sending_all, count_active_sending, count_customer_all


class HomePageView(TemplateView):
    template_name = 'mail/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['blog'] = Blog.objects.all().order_by('?')[:3]
        context_data['count_all_mail'] = count_sending_all()
        context_data['count_active_mail'] = count_active_sending()
        context_data['customer'] = count_customer_all()
        return context_data

class CustomerListView(ListView):
    model = Customer

    def get_queryset(self):
        return Customer.objects.filter(created_user=self.request.user)


class CustomerCreateView(CreateView):
    model = Customer
    fields = ('name', 'email', 'comment')
    success_url = reverse_lazy('mail:customer')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.created_user = self.request.user
            self.object.save()
        return super().form_valid(form)


class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ('name', 'email', 'comment')
    success_url = reverse_lazy('mail:customer')

    def get_queryset(self):
        return Customer.objects.filter(created_user=self.request.user)


class CustomerDetailView(DetailView):
    model = Customer
    def get_queryset(self):
        return Customer.objects.filter(created_user=self.request.user)


class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('mail:customer')

    def get_queryset(self):
        return Customer.objects.filter(created_user=self.request.user)


class MessageListView(ListView):
    model = Message

    def get_queryset(self):
        return Message.objects.filter(created_user=self.request.user)


class MessageCreateView(CreateView):
    model = Message
    fields = ('title', 'text')
    success_url = reverse_lazy('mail:message')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.created_user = self.request.user
            self.object.save()
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('title', 'text')
    success_url = reverse_lazy('mail:message')

    def get_queryset(self):
        return Message.objects.filter(created_user=self.request.user)


class MessageDetailView(DetailView):
    model = Message

    def get_queryset(self):
        return Message.objects.filter(created_user=self.request.user)


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mail:message')
    def get_queryset(self):
        return Message.objects.filter(created_user=self.request.user)


class SendingListView(ListView):
    model = Sending

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('mail.view_sending'):
            return queryset

        return queryset.filter(created_user=self.request.user)


class SendingCreateView(CreateView):
    model = Sending
    fields = '__all__'
    success_url = reverse_lazy('mail:sending')
    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.created_user = self.request.user
            self.object.save()
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     form = context_data.get('form')
    #     return context_data

class SendingUpdateView(UpdateView):
    model = Sending
    fields = '__all__'
    success_url = reverse_lazy('mail:sending')

    def get_queryset(self):
        return Sending.objects.filter(created_user=self.request.user)


class SendingDetailView(DetailView):
    model = Sending
    def get_queryset(self):
        return Sending.objects.filter(created_user=self.request.user)

class SendingDeleteView(DeleteView):
    model = Sending
    success_url = reverse_lazy('mail:sending')
    def get_queryset(self):
        return Sending.objects.filter(created_user=self.request.user)


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

@permission_required('mail.cancel_sending')
def cancel_sending(request, pk):

    current_sending = get_object_or_404(Sending, pk=pk)
    if current_sending:
        current_sending.state_mail = Sending.CANCELED
        current_sending.save()
    return redirect(request.META.get('HTTP_REFERER'))