from django import forms

from forms_mixins import StyleFormMixin
from mail.models import Customer, Sending, Message


class CustomerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Customer
        #exclude = ['user_create', ]

class SendingForm(StyleFormMixin, forms.ModelForm):
    STATUSES = (
        ('completed', 'завершена'),
        ('created', 'создана'),
        ('launched', 'запущена'),
    )
    status = forms.ChoiceField(choices=STATUSES, )

    class Meta:
        model = Sending
        #exclude = ['user_create', ]

class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        #exclude = ['user_create', ]