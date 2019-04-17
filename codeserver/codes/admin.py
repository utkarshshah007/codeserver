from django.contrib import admin

from .models import Bundle, Ticket, Scanner, Redemption

# Register your models here.
admin.site.register(Bundle)
admin.site.register(Ticket)
admin.site.register(Scanner)
admin.site.register(Redemption)
