from django.contrib import admin
from monitoring_app.models import UserProfile
from monitoring_app.models import Machine
from monitoring_app.models import Call

# Register your models here.
admin.site.register(Call)
admin.site.register(Machine)
admin.site.register(UserProfile)
