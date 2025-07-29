#!/usr/bin/env python
"""
Script de migration pour ajouter les nouveaux champs au profil utilisateur
"""

import os
from app import app, db, User

def migrate_user_profile():
    """Ajouter les nouveaux champs au modèle User"""
    with app.app_context():
        print("🔄 Migration du profil utilisateur...")
        
        # Supprimer l'ancienne base de données
        db_path = 'instance/nosdonnees.db'
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"✅ Base de données supprimée: {db_path}")
        
        print("🏗️  Création des nouvelles tables...")
        
        # Créer toutes les tables avec les nouveaux champs
        db.create_all()
        
        print("✅ Tables créées avec succès!")
        
        # Créer les domaines par défaut
        print("📂 Création des domaines par défaut...")
        from app import Domain
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
        
        # Créer un admin par défaut avec profil complet
        print("👤 Création de l'administrateur avec profil complet...")
        admin = User(
            username='admin',
            email='admin@nosdonnees.fr',
            role='admin',
            organization='Nosdonnées',
            bio='Administrateur de la plateforme Nosdonnées',
            
            # Informations académiques
            education_level='Master',
            diploma='Master en Sciences des Données',
            field_of_study='Informatique et Statistiques',
            institution='École Nationale de la Statistique',
            graduation_year=2022,
            
            # Informations professionnelles
            job_title='Data Scientist Senior',
            department='R&D',
            years_experience=8,
            expertise_areas='Machine Learning, Statistiques, Visualisation de données',
            
            # Informations de contact
            phone='+33 1 23 45 67 89',
            linkedin='https://linkedin.com/in/admin-nosdonnees',
            website='https://nosdonnees.fr'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Créer un utilisateur exemple avec profil complet
        print("👤 Création d'un utilisateur exemple...")
        user_example = User(
            username='chercheur',
            email='chercheur@universite.fr',
            role='contributor',
            organization='Université de Paris',
            bio='Chercheur en sciences des données spécialisé dans l\'analyse de données de santé publique.',
            
            # Informations académiques
            education_level='Doctorat',
            diploma='Doctorat en Statistiques Appliquées',
            field_of_study='Statistiques et Épidémiologie',
            institution='Université de Paris',
            graduation_year=2020,
            
            # Informations professionnelles
            job_title='Chercheur',
            department='Laboratoire de Statistiques',
            years_experience=5,
            expertise_areas='Épidémiologie, Statistiques bayésiennes, R',
            
            # Informations de contact
            phone='+33 1 98 76 54 32',
            linkedin='https://linkedin.com/in/chercheur-donnees',
            website='https://chercheur.universite.fr'
        )
        user_example.set_password('chercheur123')
        db.session.add(user_example)
        
        # Commit des changements
        db.session.commit()
        
        print("✅ Migration terminée avec succès!")
        print("\n📋 Comptes de test créés:")
        print("   👤 Admin: admin / admin123")
        print("   👤 Chercheur: chercheur / chercheur123")
        print("   🌐 URL: http://localhost:8000")
        print("\n🚀 Vous pouvez maintenant lancer l'application avec: python app.py")

if __name__ == '__main__':
    migrate_user_profile() 