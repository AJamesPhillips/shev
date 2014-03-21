from django.contrib import admin

from . import models

admin.site.register(models.TeamOrAgency, admin.ModelAdmin)
admin.site.register(models.Person, admin.ModelAdmin)
admin.site.register(models.ShiftType, admin.ModelAdmin)
admin.site.register(models.Outcome, admin.ModelAdmin)
admin.site.register(models.Shift, admin.ModelAdmin)
