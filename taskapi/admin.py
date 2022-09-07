from django.contrib import admin
from taskapi.models import *

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserCreationForm


from django.contrib.contenttypes.admin import GenericTabularInline

class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm

    list_display = ('email', 'username','role')
    list_filter = ('role',)
    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        ('Permissions', {'fields': ('role',)}),
    )

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
    
    def save_model(self, request, obj, form, change):
        print('Saving the Task from Admin Panel: ', obj)
        print('Team is:  ', obj.team)
        for member in obj.team.team_members.all():
            print("Member: ",member)
        # obj.save()
        super().save_model(request,obj,form,change)

    # changing which fields are displyed on add or change form 
    def get_fields(self, request, obj):
        if obj :
            fields = ('name','team','status','completed_at')
        else:
            fields = ('name','team','status')
        return fields    


class TeamAdmin(admin.ModelAdmin):
    inlines = [TaskInline,]
    filter_horizontal = ('team_members',)


admin.site.register(User,UserAdmin)
admin.site.register(Task,TaskAdmin)
admin.site.register(Team,TeamAdmin)

