from django.contrib import admin
from .models import (
    Education,
    Certification,
    Portfolio,
    ContactMethod,
    About,
    Employment,
    Template,
    UserTemplate,
    Skill,
    UserProfile,
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


@admin.register(ContactMethod)
class ContactMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_type', 'value', 'label')
    list_filter = ('contact_type',)
    search_fields = ('user__username', 'value', 'label')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'address')
    search_fields = ('user__username', 'country', 'address')
