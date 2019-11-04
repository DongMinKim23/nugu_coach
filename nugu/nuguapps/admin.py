from django.contrib import admin
from .models import Main_test, Sub_test, Schedule, Ranked_cut, Care, stretch
# Register your models here.
class MainTestAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'year', 'seq',]
admin.site.register(Main_test, MainTestAdmin)

class SubTestAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'year', 'seq',]
admin.site.register(Sub_test, SubTestAdmin)

class ScheduleTestAdmin(admin.ModelAdmin):
    list_display = ['id', 'month', 'day', 'start_time', 'name', 'check', 'created_at',]
admin.site.register(Schedule, ScheduleTestAdmin)

class RankedCutAdmin(admin.ModelAdmin):
    list_display = ['id','college','grade_cut',]
admin.site.register(Ranked_cut, RankedCutAdmin)

class CareAdmin(admin.ModelAdmin):
    list_display = ['id','symptom','food','sport',]
admin.site.register(Care, CareAdmin)

class stretchAdmin(admin.ModelAdmin):
    list_display = ['id','symptom','action',]
admin.site.register(stretch, stretchAdmin)