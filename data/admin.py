from django.contrib import admin
from .models import Parent, Child1, Child2

# Register your models here.

class IdAdmin(admin.ModelAdmin):
    list_display = ("id",)

admin.site.register(Parent, IdAdmin)
admin.site.register(Child1, IdAdmin)
admin.site.register(Child2, IdAdmin)