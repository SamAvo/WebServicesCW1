from django.contrib import admin
from .models import Module, Professor, User, ModuleInstance, Rating


# Register your models here.
admin.site.register(Module)
admin.site.register(Professor)
admin.site.register(User)
admin.site.register(ModuleInstance)
admin.site.register(Rating)

