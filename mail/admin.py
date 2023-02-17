from django.contrib import admin

from blog.models import Blog
from mail.models import Customer, Sending
from users.models import User

admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Customer)
admin.site.register(Sending)


