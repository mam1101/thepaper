from django.contrib import admin

from paper import models


class PaperItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.PaperItem, PaperItemAdmin)

