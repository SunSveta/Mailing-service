from django.urls import path

from mail.apps import MailConfig
from mail.views import CustomerDetailView, CustomerDeleteView, statistic, HomePageView
from mail.views import CustomerListView, CustomerCreateView, CustomerUpdateView
from mail.views import MessageListView, MessageCreateView, MessageUpdateView, MessageDetailView, MessageDeleteView
from mail.views import SendingCreateView, SendingListView, SendingUpdateView, SendingDeleteView, SendingDetailView

app_name = MailConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('customer/', CustomerListView.as_view(), name='customer'),
    path('customer/create/', CustomerCreateView.as_view(), name='create'),
    path('customer/update/<int:pk>', CustomerUpdateView.as_view(), name='update'),
    path('customer/detail/<int:pk>', CustomerDetailView.as_view(), name='detail'),
    path('customer/delete/<int:pk>', CustomerDeleteView.as_view(), name='delete'),
    path('message/', MessageListView.as_view(), name='message'),
    path('message/mes_create/', MessageCreateView.as_view(), name='mes_create'),
    path('message/mes_update/<int:pk>', MessageUpdateView.as_view(), name='mes_update'),
    path('message/mes_detail/<int:pk>', MessageDetailView.as_view(), name='mes_detail'),
    path('message/mes_delete/<int:pk>', MessageDeleteView.as_view(), name='mes_delete'),
    path('sending/', SendingListView.as_view(), name='sending'),
    path('sending/sen_create/', SendingCreateView.as_view(), name='sen_create'),
    path('sending/sen_update/<int:pk>', SendingUpdateView.as_view(), name='sen_update'),
    path('sending/sen_detail/<int:pk>', SendingDetailView.as_view(), name='sen_detail'),
    path('sending/sen_delete/<int:pk>', SendingDeleteView.as_view(), name='sen_delete'),
    path('statistic/', statistic, name='statistic')
 ]