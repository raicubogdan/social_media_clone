from django.contrib import admin
from . import models

# "TabularInLine" class allows us to edit models on the same page as the parent model
class GroupMemberInLine(admin.TabularInline): 
    model = models.GroupMember

admin.site.register(models.Group)

