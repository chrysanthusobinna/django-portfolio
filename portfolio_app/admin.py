from django.contrib import admin
from .models import (
    Education,
    Certification,
    Portfolio,
    Contact,
    About,
    Employment,
    Template,
    UserTemplate,
    Skill,
)


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_file', 'tag', 'is_active', 'created_at')
    list_filter = ('is_active', 'tag', 'created_at')
    search_fields = ('name', 'template_file', 'description')
    list_editable = ('is_active', 'tag')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'template_file', 'description')
        }),
        ('Display Settings', {
            'fields': ('image_path', 'tag', 'is_active')
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserTemplate)
class UserTemplateAdmin(admin.ModelAdmin):
    list_display = ('user', 'template', 'selected_at')
    list_filter = ('template', 'selected_at')
    search_fields = ('user__username', 'user__email', 'template__name')
    readonly_fields = ('selected_at',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skills')
    search_fields = ('user__username',)
