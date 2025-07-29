#!/usr/bin/env python
"""
Script pour corriger la base de données Nosdonnées
Supprime l'ancienne base et recrée les tables avec la bonne structure
"""

import os
from app import app, db, User, Domain, Dataset, DownloadLog, Comment
from datetime import datetime

def fix_database():
    """Corriger la base de données"""
    with app.app_context():
        print("🗑️  Suppression de l'ancienne base de données...")
        
        # Supprimer le fichier de base de données s'il existe
        db_path = 'instance/nosdonnees.db'
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"✅ Base de données supprimée: {db_path}")
        
        print("🏗️  Création des nouvelles tables...")
        
        # Créer toutes les tables
        db.create_all()
        
        print("✅ Tables créées avec succès!")
        
        # Créer les domaines par défaut
        print("📂 Création des domaines par défaut...")
        domains_data = [
            {'name': 'Santé', 'description': 'Bases de données liées à la santé publique', 'icon': 'fas fa-heartbeat'},
            {'name': 'Éducation', 'description': 'Données sur l\'éducation et les écoles', 'icon': 'fas fa-graduation-cap'},
            {'name': 'Agriculture', 'description': 'Données agricoles et production', 'icon': 'fas fa-seedling'},
            {'name': 'Environnement', 'description': 'Données environnementales', 'icon': 'fas fa-leaf'},
            {'name': 'Économie', 'description': 'Données économiques et financières', 'icon': 'fas fa-chart-line'},
            {'name': 'Transport', 'description': 'Données de transport et mobilité', 'icon': 'fas fa-car'},
            {'name': 'Démographie', 'description': 'Données démographiques', 'icon': 'fas fa-users'},
            {'name': 'Technologie', 'description': 'Données technologiques', 'icon': 'fas fa-microchip'}
        ]
        
        for domain_data in domains_data:
            domain = Domain(**domain_data)
            db.session.add(domain)
        
        # Créer un admin par défaut
        print("👤 Création de l'administrateur par défaut...")
        admin = User(
            username='admin',
            email='admin@nosdonnees.fr',
            role='admin',
            organization='Nosdonnées'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Créer quelques bases de données d'exemple
        print("📊 Création de bases de données d'exemple...")
        
        # Récupérer le premier domaine
        health_domain = Domain.query.filter_by(name='Santé').first()
        education_domain = Domain.query.filter_by(name='Éducation').first()
        
        if health_domain:
            sample_dataset1 = Dataset(
                title='Données de santé publique 2024',
                description='Base de données complète sur les indicateurs de santé publique en France pour l\'année 2024.',
                short_description='Indicateurs de santé publique 2024',
                source='Ministère de la Santé',
                author='admin',
                file_path='uploads/sample_health_data.csv',
                file_format='csv',
                file_size=1024000,
                domain_id=health_domain.id,
                keywords='santé, publique, indicateurs, 2024',
                documentation='Cette base contient les principaux indicateurs de santé publique...',
                user_id=admin.id,
                is_validated=True,
                download_count=15,
                view_count=45,
                rating=4.2
            )
            db.session.add(sample_dataset1)
        
        if education_domain:
            sample_dataset2 = Dataset(
                title='Statistiques éducatives nationales',
                description='Données complètes sur le système éducatif français : effectifs, résultats, infrastructures.',
                short_description='Statistiques du système éducatif',
                source='Ministère de l\'Éducation',
                author='admin',
                file_path='uploads/sample_education_data.xlsx',
                file_format='xlsx',
                file_size=2048000,
                domain_id=education_domain.id,
                keywords='éducation, statistiques, écoles, résultats',
                documentation='Base de données des statistiques éducatives...',
                user_id=admin.id,
                is_validated=True,
                download_count=8,
                view_count=32,
                rating=4.5
            )
            db.session.add(sample_dataset2)
        
        # Commit des changements
        db.session.commit()
        
        print("✅ Base de données corrigée avec succès!")
        print("\n📋 Informations de connexion:")
        print("   👤 Admin: admin")
        print("   🔑 Mot de passe: admin123")
        print("   🌐 URL: http://localhost:8000")
        print("\n🚀 Vous pouvez maintenant lancer l'application avec: python app.py")

if __name__ == '__main__':
    fix_database() 