from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import User
import os

from .models import Dataset, Domain, UserProfile, Comment, DownloadLog
from .forms import (
    DatasetUploadForm, DatasetSearchForm, CommentForm, 
    UserRegistrationForm, DatasetUpdateForm, AdminValidationForm
)


def is_admin(user):
    """Vérifie si l'utilisateur est admin"""
    try:
        return user.userprofile.role == 'admin'
    except UserProfile.DoesNotExist:
        return False


def is_contributor(user):
    """Vérifie si l'utilisateur est contributeur"""
    try:
        return user.userprofile.role in ['contributor', 'admin']
    except UserProfile.DoesNotExist:
        return False


def home(request):
    """Page d'accueil"""
    # Statistiques
    total_datasets = Dataset.objects.filter(status='published').count()
    total_downloads = Dataset.objects.filter(status='published').aggregate(
        total=Count('download_count')
    )['total'] or 0
    total_users = User.objects.count()
    
    # Bases les plus populaires
    popular_datasets = Dataset.objects.filter(status='published').order_by('-download_count')[:6]
    
    # Domaines les plus actifs
    active_domains = Domain.objects.annotate(
        dataset_count=Count('datasets', filter=Q(datasets__status='published'))
    ).filter(dataset_count__gt=0).order_by('-dataset_count')[:5]
    
    context = {
        'total_datasets': total_datasets,
        'total_downloads': total_downloads,
        'total_users': total_users,
        'popular_datasets': popular_datasets,
        'active_domains': active_domains,
    }
    return render(request, 'datasets/home.html', context)


def dataset_list(request):
    """Liste des bases de données avec filtres"""
    datasets = Dataset.objects.filter(status='published')
    
    # Formulaire de recherche
    search_form = DatasetSearchForm(request.GET)
    if search_form.is_valid():
        q = search_form.cleaned_data.get('q')
        domain = search_form.cleaned_data.get('domain')
        file_format = search_form.cleaned_data.get('file_format')
        country = search_form.cleaned_data.get('country')
        date_from = search_form.cleaned_data.get('date_from')
        date_to = search_form.cleaned_data.get('date_to')
        
        if q:
            datasets = datasets.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(tags__icontains=q) |
                Q(author__icontains=q)
            )
        
        if domain:
            datasets = datasets.filter(domain=domain)
        
        if file_format:
            datasets = datasets.filter(file_format=file_format)
        
        if country:
            datasets = datasets.filter(country__icontains=country)
        
        if date_from:
            datasets = datasets.filter(creation_date__gte=date_from)
        
        if date_to:
            datasets = datasets.filter(creation_date__lte=date_to)
    
    # Pagination
    paginator = Paginator(datasets, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Domaines pour le filtre
    domains = Domain.objects.all()
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'domains': domains,
    }
    return render(request, 'datasets/dataset_list.html', context)


def dataset_detail(request, pk):
    """Détail d'une base de données"""
    dataset = get_object_or_404(Dataset, pk=pk)
    
    # Incrémenter le compteur de vues
    dataset.increment_view()
    
    # Formulaire de commentaire
    comment_form = CommentForm()
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.dataset = dataset
            comment.user = request.user
            comment.save()
            messages.success(request, 'Commentaire ajouté avec succès!')
            return redirect('dataset_detail', pk=pk)
    
    # Commentaires
    comments = dataset.comments.all()
    
    context = {
        'dataset': dataset,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'datasets/dataset_detail.html', context)


@login_required
def dataset_download(request, pk):
    """Téléchargement d'une base de données"""
    dataset = get_object_or_404(Dataset, pk=pk, status='published')
    
    # Incrémenter le compteur de téléchargements
    dataset.increment_download()
    
    # Enregistrer le téléchargement
    DownloadLog.objects.create(
        dataset=dataset,
        user=request.user if request.user.is_authenticated else None,
        ip_address=request.META.get('REMOTE_ADDR', ''),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    # Retourner le fichier
    file_path = dataset.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    
    messages.error(request, 'Fichier non trouvé.')
    return redirect('dataset_detail', pk=pk)


@login_required
@user_passes_test(is_contributor)
def dataset_upload(request):
    """Upload d'une nouvelle base de données"""
    if request.method == 'POST':
        form = DatasetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.submitted_by = request.user
            
            # Définir le statut selon le rôle
            if request.user.userprofile.role == 'admin':
                dataset.status = 'published'
                dataset.validated_by = request.user
                dataset.validated_at = timezone.now()
            else:
                dataset.status = 'pending'
            
            # Calculer la taille du fichier
            if dataset.file:
                dataset.file_size = dataset.file.size
            
            dataset.save()
            
            messages.success(request, 'Base de données soumise avec succès!')
            return redirect('dashboard')
    else:
        form = DatasetUploadForm()
    
    context = {
        'form': form,
    }
    return render(request, 'datasets/dataset_upload.html', context)


@login_required
def dashboard(request):
    """Tableau de bord utilisateur"""
    user_profile = request.user.userprofile
    
    if user_profile.role == 'admin':
        # Dashboard admin
        pending_datasets = Dataset.objects.filter(status='pending')
        recent_datasets = Dataset.objects.all().order_by('-created_at')[:10]
        stats = {
            'total_datasets': Dataset.objects.count(),
            'published_datasets': Dataset.objects.filter(status='published').count(),
            'pending_datasets': pending_datasets.count(),
            'total_users': User.objects.count(),
        }
        
        context = {
            'user_profile': user_profile,
            'pending_datasets': pending_datasets,
            'recent_datasets': recent_datasets,
            'stats': stats,
        }
        return render(request, 'datasets/admin_dashboard.html', context)
    
    elif user_profile.role == 'contributor':
        # Dashboard contributeur
        my_datasets = Dataset.objects.filter(submitted_by=request.user)
        
        context = {
            'user_profile': user_profile,
            'my_datasets': my_datasets,
        }
        return render(request, 'datasets/contributor_dashboard.html', context)
    
    else:
        # Dashboard visiteur
        recent_datasets = Dataset.objects.filter(status='published').order_by('-created_at')[:5]
        
        context = {
            'user_profile': user_profile,
            'recent_datasets': recent_datasets,
        }
        return render(request, 'datasets/visitor_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def admin_validation(request, pk):
    """Validation admin d'une base de données"""
    dataset = get_object_or_404(Dataset, pk=pk)
    
    if request.method == 'POST':
        form = AdminValidationForm(request.POST, instance=dataset)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.validated_by = request.user
            dataset.validated_at = timezone.now()
            dataset.save()
            
            messages.success(request, 'Base de données validée avec succès!')
            return redirect('dashboard')
    else:
        form = AdminValidationForm(instance=dataset)
    
    context = {
        'dataset': dataset,
        'form': form,
    }
    return render(request, 'datasets/admin_validation.html', context)


def register(request):
    """Inscription utilisateur"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Compte créé avec succès! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'datasets/register.html', context)


def domain_list(request):
    """Liste des domaines"""
    domains = Domain.objects.annotate(
        dataset_count=Count('datasets', filter=Q(datasets__status='published'))
    ).order_by('name')
    
    context = {
        'domains': domains,
    }
    return render(request, 'datasets/domain_list.html', context)


def domain_detail(request, pk):
    """Détail d'un domaine avec ses bases de données"""
    domain = get_object_or_404(Domain, pk=pk)
    datasets = domain.datasets.filter(status='published')
    
    # Pagination
    paginator = Paginator(datasets, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'domain': domain,
        'page_obj': page_obj,
    }
    return render(request, 'datasets/domain_detail.html', context)


# API Views pour AJAX
def api_search_datasets(request):
    """API de recherche AJAX"""
    q = request.GET.get('q', '')
    if q:
        datasets = Dataset.objects.filter(
            status='published',
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(tags__icontains=q)
        )[:10]
        
        results = []
        for dataset in datasets:
            results.append({
                'id': dataset.id,
                'title': dataset.title,
                'description': dataset.short_description or dataset.description[:100],
                'url': dataset.get_absolute_url(),
            })
        
        return JsonResponse({'results': results})
    
    return JsonResponse({'results': []})


def api_dataset_stats(request):
    """API des statistiques"""
    if request.user.is_authenticated and request.user.userprofile.role == 'admin':
        stats = {
            'total_datasets': Dataset.objects.count(),
            'published_datasets': Dataset.objects.filter(status='published').count(),
            'pending_datasets': Dataset.objects.filter(status='pending').count(),
            'total_downloads': Dataset.objects.aggregate(
                total=Count('download_count')
            )['total'] or 0,
        }
        return JsonResponse(stats)
    
    return JsonResponse({'error': 'Unauthorized'}, status=403) 