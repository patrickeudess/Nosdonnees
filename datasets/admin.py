from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, Domain, Dataset, DatasetVersion, DownloadLog, Comment


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'organization', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email', 'organization']
    ordering = ['-created_at']


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'dataset_count']
    search_fields = ['name', 'description']
    ordering = ['name']
    
    def dataset_count(self, obj):
        return obj.datasets.filter(status='published').count()
    dataset_count.short_description = 'Bases publiées'


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'domain', 'status', 'file_format', 
        'download_count', 'view_count', 'submitted_at'
    ]
    list_filter = [
        'status', 'domain', 'file_format', 'language', 
        'submitted_at', 'validated_at'
    ]
    search_fields = ['title', 'description', 'author', 'source', 'tags']
    readonly_fields = ['download_count', 'view_count', 'file_size']
    ordering = ['-submitted_at']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('title', 'description', 'short_description', 'author', 'source')
        }),
        ('Classification', {
            'fields': ('domain', 'tags', 'country', 'language')
        }),
        ('Fichier', {
            'fields': ('file', 'file_format', 'file_size', 'creation_date')
        }),
        ('Statut et validation', {
            'fields': ('status', 'submitted_by', 'submitted_at', 'validated_by', 'validated_at', 'rejection_reason')
        }),
        ('Statistiques', {
            'fields': ('download_count', 'view_count', 'row_count', 'column_count'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Nouvelle base
            obj.submitted_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(DatasetVersion)
class DatasetVersionAdmin(admin.ModelAdmin):
    list_display = ['dataset', 'version_number', 'created_at']
    list_filter = ['created_at']
    search_fields = ['dataset__title']
    ordering = ['-created_at']


@admin.register(DownloadLog)
class DownloadLogAdmin(admin.ModelAdmin):
    list_display = ['dataset', 'user', 'ip_address', 'downloaded_at']
    list_filter = ['downloaded_at']
    search_fields = ['dataset__title', 'user__username', 'ip_address']
    ordering = ['-downloaded_at']
    readonly_fields = ['dataset', 'user', 'ip_address', 'user_agent', 'downloaded_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['dataset', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['dataset__title', 'user__username', 'content']
    ordering = ['-created_at']
    readonly_fields = ['dataset', 'user', 'created_at'] 