from django.contrib import admin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from mood_tracking1.mood.forms import ChangeUserRoleForm
from mood_tracking1.mood.models import Activity_event, UserProfile, Friend, ConsultingSession, MoodComparison, UserRole


class ActivityEventAdmin(admin.ModelAdmin):
    list_display = ('type', 'event', 'time', 'user_id')
    list_filter = ('type', 'event')
    search_fields = ('event', )
    ordering = ('-time',)

    fields = ('type', 'event', 'user_id')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', )

class FriendAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'friend_id', 'added_time')
    list_filter = ('added_time',)
    ordering = ('-added_time',)

class ConsultingSessionAdmin(admin.ModelAdmin):
    list_display = ('Client_name', 'start_time', 'end_time', 'user')
    search_fields = ('Client_name', )

class MoodComparisonAdmin(admin.ModelAdmin):
    list_display = ('title', 'your_mood', 'compared_mood', 'your_user_id' )
    search_fields = ('title', )

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    filter_horizontal = ('permissions',)





admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(Activity_event, ActivityEventAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(ConsultingSession, ConsultingSessionAdmin)
admin.site.register(MoodComparison, MoodComparisonAdmin)
