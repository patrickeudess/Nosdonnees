Nosdonnées - Plateforme de partage de bases de données
🎯 Description
Nosdonnées est une plateforme web centralisée de téléchargement et de partage de bases de données utilisées dans divers domaines (santé, éducation, agriculture, environnement, économie, etc.).

✨ Fonctionnalités principales
👥 Rôles utilisateurs
Visiteur : peut consulter et télécharger les bases
Contributeur : peut proposer une base à publier
Administrateur : valide les contributions, modère les contenus, gère les utilisateurs
📁 Fonctionnalités
📂 Catalogue filtrable des bases de données par domaine, format, année, pays, mot-clé
🔍 Moteur de recherche textuel par mot-clé
📝 Page de chaque base de données avec métadonnées complètes
⬆️ Formulaire de dépôt d'une nouvelle base
✅ Espace admin pour valider ou rejeter les contributions
📈 Statistiques d'usage (bases les plus téléchargées, domaines les plus actifs)
🚀 Installation et démarrage
Prérequis
Python 3.8+
pip
Installation
Cloner le projet
git clone <repository-url>
cd nosdonnees
Créer un environnement virtuel
python -m venv .venv
Activer l'environnement virtuel
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
Installer les dépendances
pip install -r requirements.txt
Installer le projet en mode développement
pip install -e .
Initialiser la base de données
python init_db.py
Lancer le serveur de développement
python run_server.py
L'application sera disponible sur : http://localhost:8000

🔧 Configuration
Variables d'environnement
Créez un fichier .env à la racine du projet :

NOSDONNEES_SECRET_KEY=your-secret-key-here
NOSDONNEES_DEBUG=True
NOSDONNEES_ALLOWED_HOSTS=localhost,127.0.0.1
Base de données
Par défaut, l'application utilise SQLite. Pour utiliser PostgreSQL ou MySQL, modifiez settings.py.

📊 Structure du projet
nosdonnees/
├── datasets/                 # Application principale
│   ├── models.py            # Modèles de données
│   ├── views.py             # Vues et logique métier
│   ├── forms.py             # Formulaires
│   ├── urls.py              # URLs de l'application
│   └── admin.py             # Configuration admin
├── templates/               # Templates HTML
│   ├── base.html           # Template de base
│   └── datasets/           # Templates spécifiques
├── static/                 # Fichiers statiques
│   ├── css/               # Styles CSS
│   └── js/                # JavaScript
├── media/                  # Fichiers uploadés
├── manage.py              # Script de gestion Django
├── settings.py            # Configuration Django
├── urls.py                # URLs principales
├── requirements.txt       # Dépendances Python
└── README.md             # Ce fichier
🗄️ Modèles de données
UserProfile
Extension du modèle User de Django
Rôles : visiteur, contributeur, administrateur
Informations supplémentaires : organisation, bio
Domain
Domaines thématiques (santé, éducation, etc.)
Description et icône
Dataset
Base de données principale
Métadonnées complètes (titre, description, source, etc.)
Gestion des fichiers et formats
Système de validation et statuts
Statistiques d'usage
DatasetVersion
Gestion des versions des bases de données
Historique des modifications
DownloadLog
Journal des téléchargements
Traçabilité et statistiques
Comment
Système de commentaires et évaluations
Interaction utilisateur
🔐 Authentification
L'application utilise le système d'authentification standard de Django avec des rôles personnalisés :

Visiteur : accès en lecture seule
Contributeur : peut proposer des bases de données
Administrateur : accès complet et modération
📈 Statistiques
L'application collecte automatiquement :

Nombre de téléchargements par base
Nombre de vues par base
Statistiques par domaine
Utilisation par utilisateur
🎨 Interface utilisateur
Design responsive avec Bootstrap 5
Interface moderne et intuitive
Recherche en temps réel
Filtres avancés
Dashboard personnalisé selon le rôle
🔍 Recherche et filtres
Recherche textuelle dans les titres, descriptions et mots-clés
Filtrage par domaine, format, pays, date
Tri par popularité, date, nom
Pagination des résultats
📱 Responsive design
L'interface s'adapte automatiquement aux différentes tailles d'écran :

Desktop : affichage complet avec sidebar
Tablet : layout adapté
Mobile : navigation optimisée
🚀 Déploiement
Production
Configurer les variables d'environnement
Utiliser une base de données PostgreSQL
Configurer un serveur web (Nginx + Gunicorn)
Configurer les fichiers statiques
Configurer HTTPS
Docker (optionnel)
docker build -t nosdonnees .
docker run -p 8000:8000 nosdonnees
🤝 Contribution
Fork le projet
Créer une branche feature (git checkout -b feature/AmazingFeature)
Commit les changements (git commit -m 'Add some AmazingFeature')
Push vers la branche (git push origin feature/AmazingFeature)
Ouvrir une Pull Request
📝 Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

📞 Support
Pour toute question ou problème :

Ouvrir une issue sur GitHub
Contacter l'équipe de développement
🔄 Mises à jour
Ajouter une nouvelle migration
python manage.py makemigrations datasets
python manage.py migrate
Mettre à jour les dépendances
pip install -r requirements.txt --upgrade
🎯 Roadmap
 API REST complète
 Système de notifications
 Export en différents formats
 Intégration avec des sources de données externes
 Système de recommandations
 Analytics avancées
 Application mobile
Nosdonnées - Partagez vos données, enrichissez la connaissance ! 📊
