from django.contrib import admin
from taskapi.models import *

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# setting view site url to our api root
admin.site.site_url = '/api/'

# for customizing the admin interface of UserAdmin
class UserAdmin(BaseUserAdmin):

    list_display = ('username', 'email','role')
    list_filter = ('role',)
    
    # when exisiting user is edited
    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        ('Permissions', {'fields': ('role',)}),
    )

    # when new user is created
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2')}
         ),('Permissions', {'fields': ('role',)}),
    )
    search_fields = ('email','username')
    filter_horizontal = ()

# to show all tasks in the Team detail admin view
class TaskInline(admin.TabularInline):
    model = Task
    fk_name = "team"
    exclude = ['team_members']
    # to set a how many extra lines we need in our inline form
    extra = 0

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name','team','started_at','status','completed_at')
    list_filter = ('status','team')
    
    # dynamically changing which fields are displyed on add or change form 
    def get_fields(self, request, obj):
        if obj :
            fields = ('name','team','status','completed_at')
        else:
            fields = ('name','team','status')
        return fields    


class TeamAdmin(admin.ModelAdmin):
    inlines = [TaskInline,]
    list_display = ('name','team_leader')

    # for manytomany field interface
    filter_horizontal = ('team_members',)


admin.site.register(User,UserAdmin)
admin.site.register(Task,TaskAdmin)
admin.site.register(Team,TeamAdmin)

