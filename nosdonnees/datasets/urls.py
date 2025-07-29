from django.urls import path
from . import views

app_name = 'datasets'

urlpatterns = [
    # Pages publiques
    path('', views.home, name='home'),
    path('datasets/', views.dataset_list, name='dataset_list'),
    path('datasets/<int:pk>/', views.dataset_detail, name='dataset_detail'),
    path('datasets/<int:pk>/download/', views.dataset_download, name='dataset_download'),
    path('domains/', views.domain_list, name='domain_list'),
    path('domains/<int:pk>/', views.domain_detail, name='domain_detail'),
    
    # Authentification
    path('register/', views.register, name='register'),
    
    # Dashboard et gestion
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.dataset_upload, name='dataset_upload'),
    
    # Admin
    path('admin/validation/<int:pk>/', views.admin_validation, name='admin_validation'),
    
    # API
    path('api/search/', views.api_search_datasets, name='api_search'),
    path('api/stats/', views.api_dataset_stats, name='api_stats'),
] 