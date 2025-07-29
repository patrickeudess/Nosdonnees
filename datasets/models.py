from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import os


class UserProfile(models.Model):
    """Profil utilisateur étendu avec rôle"""
    ROLE_CHOICES = [
        ('visitor', 'Visiteur'),
        ('contributor', 'Contributeur'),
        ('admin', 'Administrateur'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='visitor')
    bio = models.TextField(blank=True, null=True)
    organization = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


class Domain(models.Model):
    """Domaines thématiques des bases de données"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # Pour les icônes CSS
    
    class Meta:
        verbose_name = "Domaine"
        verbose_name_plural = "Domaines"
    
    def __str__(self):
        return self.name


class Dataset(models.Model):
    """Base de données"""
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('pending', 'En attente de validation'),
        ('published', 'Publié'),
        ('rejected', 'Rejeté'),
    ]
    
    FORMAT_CHOICES = [
        ('csv', 'CSV'),
        ('xlsx', 'Excel'),
        ('json', 'JSON'),
        ('xml', 'XML'),
        ('sql', 'SQL'),
        ('other', 'Autre'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    
    # Métadonnées
    source = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    creation_date = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)
    
    # Fichier et format
    file = models.FileField(
        upload_to='datasets/',
        validators=[FileExtensionValidator(allowed_extensions=['csv', 'xlsx', 'json', 'xml', 'sql', 'zip'])]
    )
    file_format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    file_size = models.PositiveIntegerField(help_text="Taille en bytes", blank=True, null=True)
    
    # Classification
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='datasets')
    tags = models.CharField(max_length=500, blank=True, help_text="Mots-clés séparés par des virgules")
    country = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=10, default='fr')
    
    # Statut et validation
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_datasets')
    submitted_at = models.DateTimeField(auto_now_add=True)
    validated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='validated_datasets', blank=True, null=True)
    validated_at = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True)
    
    # Statistiques
    download_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    
    # Métadonnées techniques
    row_count = models.PositiveIntegerField(blank=True, null=True)
    column_count = models.PositiveIntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Base de données"
        verbose_name_plural = "Bases de données"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        """Retourne la liste des tags"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def get_file_size_mb(self):
        """Retourne la taille du fichier en MB"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0
    
    def increment_download(self):
        """Incrémente le compteur de téléchargements"""
        self.download_count += 1
        self.save(update_fields=['download_count'])
    
    def increment_view(self):
        """Incrémente le compteur de vues"""
        self.view_count += 1
        self.save(update_fields=['view_count'])


class DatasetVersion(models.Model):
    """Versions des bases de données"""
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    file = models.FileField(upload_to='datasets/versions/')
    changelog = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['dataset', 'version_number']
        ordering = ['-version_number']
    
    def __str__(self):
        return f"{self.dataset.title} v{self.version_number}"


class DownloadLog(models.Model):
    """Journal des téléchargements"""
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='download_logs')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='downloads', blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-downloaded_at']
    
    def __str__(self):
        return f"{self.dataset.title} - {self.downloaded_at}"


class Comment(models.Model):
    """Commentaires sur les bases de données"""
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Commentaire de {self.user.username} sur {self.dataset.title}" 