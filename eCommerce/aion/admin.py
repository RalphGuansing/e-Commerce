from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(User_Details)
admin.site.register(Address_Details)
admin.site.register(Cart)
admin.site.register(Order)


class LogsAdmin(admin.ModelAdmin):
	list_display = ('user','date','action')

admin.site.register(Logs, LogsAdmin)

