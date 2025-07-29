#!/usr/bin/env python
"""
Script d'initialisation de la base de données pour Nosdonnées
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nosdonnees.settings')
django.setup()

# Imports après la configuration Django
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User
from datasets.models import Domain, UserProfile

def create_superuser():
    """Créer un superutilisateur admin"""
    try:
        user = User.objects.create_user(
            username='admin',
            email='admin@nosdonnees.fr',
            password='admin123',
            first_name='Administrateur',
            last_name='Nosdonnées',
            is_staff=True,
            is_superuser=True
        )
        
        # Créer le profil utilisateur
        UserProfile.objects.create(
            user=user,
            role='admin',
            organization='Nosdonnées',
            bio='Administrateur principal de la plateforme'
        )
        
        print("✅ Superutilisateur créé avec succès!")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Email: admin@nosdonnees.fr")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du superutilisateur: {e}")

def create_domains():
    """Créer les domaines par défaut"""
    domains_data = [
        {
            'name': 'Santé',
            'description': 'Bases de données liées à la santé publique, la médecine, les épidémies, etc.',
            'icon': 'fas fa-heartbeat'
        },
        {
            'name': 'Éducation',
            'description': 'Données sur l\'éducation, les écoles, les résultats scolaires, etc.',
            'icon': 'fas fa-graduation-cap'
        },
        {
            'name': 'Agriculture',
            'description': 'Données agricoles, production, météo, etc.',
            'icon': 'fas fa-seedling'
        },
        {
            'name': 'Environnement',
            'description': 'Données environnementales, pollution, biodiversité, etc.',
            'icon': 'fas fa-leaf'
        },
        {
            'name': 'Économie',
            'description': 'Données économiques, PIB, commerce, emploi, etc.',
            'icon': 'fas fa-chart-line'
        },
        {
            'name': 'Transport',
            'description': 'Données de transport, trafic, infrastructure, etc.',
            'icon': 'fas fa-car'
        },
        {
            'name': 'Démographie',
            'description': 'Données démographiques, population, migrations, etc.',
            'icon': 'fas fa-users'
        },
        {
            'name': 'Technologie',
            'description': 'Données technologiques, innovation, numérique, etc.',
            'icon': 'fas fa-microchip'
        }
    ]
    
    for domain_data in domains_data:
        domain, created = Domain.objects.get_or_create(
            name=domain_data['name'],
            defaults={
                'description': domain_data['description'],
                'icon': domain_data['icon']
            }
        )
        
        if created:
            print(f"✅ Domaine créé: {domain.name}")
        else:
            print(f"ℹ️  Domaine existant: {domain.name}")

def main():
    """Fonction principale"""
    print("🚀 Initialisation de la base de données Nosdonnées...")
    
    # Créer les migrations et appliquer
    print("\n📋 Création et application des migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations appliquées avec succès!")
    except Exception as e:
        print(f"❌ Erreur lors des migrations: {e}")
        return
    
    # Créer les domaines
    print("\n🏷️  Création des domaines par défaut...")
    create_domains()
    
    # Créer le superutilisateur
    print("\n👤 Création du superutilisateur...")
    create_superuser()
    
    print("\n🎉 Initialisation terminée!")
    print("\n📝 Prochaines étapes:")
    print("   1. Lancer le serveur: python manage.py runserver")
    print("   2. Se connecter à l'admin: http://localhost:8000/admin")
    print("   3. Commencer à ajouter des bases de données!")

if __name__ == '__main__':
    main() 