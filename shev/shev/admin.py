from django.contrib import admin

from . import models

class ShiftInline(admin.TabularInline):
    model = models.Shift
    extra = 1

class DayAdmin(admin.ModelAdmin):
    inlines = (ShiftInline,)

admin.site.register(models.TeamOrAgency, admin.ModelAdmin)
admin.site.register(models.Person, admin.ModelAdmin)
admin.site.register(models.ShiftType, admin.ModelAdmin)
admin.site.register(models.Outcome, admin.ModelAdmin)
admin.site.register(models.Shift, admin.ModelAdmin)
admin.site.register(models.Day, DayAdmin)
