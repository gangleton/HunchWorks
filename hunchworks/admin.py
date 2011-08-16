import models
from django.contrib import admin

### EXAMPLE ###
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'email')
#     search_fields = ('first_name', 'last_name')
 
# admin.site.register(Publisher)
# admin.site.register(Author, AuthorAdmin)


admin.site.register(models.HwHunch)
admin.site.register(models.HwUser)
admin.site.register(models.HwSkill)
admin.site.register(models.HwSkillConnections)
