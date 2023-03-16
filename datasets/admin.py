from django.contrib import admin
from .models import Dataset, DatasetModel, DatasetField, Protocol, Task, Activity

# Register your models here.
class DatasetAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
admin.site.register(Dataset, DatasetAdmin)

class DatasetModelAdmin(admin.ModelAdmin):
    list_display = ("id", "model_name", "parent_model")
    list_editable = ("parent_model",)
admin.site.register(DatasetModel, DatasetModelAdmin)

admin.site.register(DatasetField)
admin.site.register(Protocol)
admin.site.register(Task)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "dataset", "created_by", "created_at")
admin.site.register(Activity, ActivityAdmin)