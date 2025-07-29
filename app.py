#!/usr/bin/env python
"""
Nosdonnées - Application Flask
Plateforme de partage de bases de données
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore
from werkzeug.utils import secure_filename # type: ignore
import os
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nosdonnees-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nosdonnees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max

# Créer le dossier uploads s'il n'existe pas
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modèles de données
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='visitor')  # visitor, contributor, admin
    organization = db.Column(db.String(200))
    bio = db.Column(db.Text)
    
    # Informations académiques et professionnelles
    education_level = db.Column(db.String(50))  # Bac, Licence, Master, Doctorat, etc.
    diploma = db.Column(db.String(200))  # Diplôme obtenu
    field_of_study = db.Column(db.String(200))  # Domaine d'études
    institution = db.Column(db.String(200))  # Établissement d'études
    graduation_year = db.Column(db.Integer)  # Année d'obtention du diplôme
    
    # Informations professionnelles
    job_title = db.Column(db.String(200))  # Poste actuel
    department = db.Column(db.String(200))  # Département/Service
    years_experience = db.Column(db.Integer)  # Années d'expérience
    expertise_areas = db.Column(db.Text)  # Domaines d'expertise
    
    # Informations de contact
    phone = db.Column(db.String(20))
    linkedin = db.Column(db.String(200))
    website = db.Column(db.String(200))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(300))
    source = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(500), nullable=False)
    file_format = db.Column(db.String(10), nullable=False)
    file_size = db.Column(db.Integer)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'), nullable=False)
    keywords = db.Column(db.String(500))
    documentation = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_validated = db.Column(db.Boolean, default=False)  # Gardé pour compatibilité
    status = db.Column(db.String(20), default='pending')  # pending, validated, rejected
    rejection_reason = db.Column(db.Text)  # Raison du rejet
    download_count = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    
    # Relations
    domain = db.relationship('Domain', backref='datasets')
    user = db.relationship('User', backref='datasets')
    comments = db.relationship('Comment', backref='dataset', lazy='dynamic')

class DownloadLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    downloaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)  # 1-5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    user = db.relationship('User', backref='comments')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    """Page d'accueil"""
    stats = {
        'total_datasets': Dataset.query.filter_by(status='validated').count(),
        'total_downloads': db.session.query(db.func.sum(Dataset.download_count)).scalar() or 0,
        'total_users': User.query.count()
    }
    
    popular_datasets = Dataset.query.filter_by(status='validated').order_by(Dataset.download_count.desc()).limit(6).all()
    active_domains = Domain.query.join(Dataset).filter(Dataset.status == 'validated').group_by(Domain.id).order_by(db.func.count(Dataset.id).desc()).limit(5).all()
    
    return render_template('home.html', stats=stats, popular_datasets=popular_datasets, active_domains=active_domains)

@app.route('/datasets')
def dataset_list():
    """Liste des bases de données"""
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    # Filtres
    q = request.args.get('q', '')
    domain_id = request.args.get('domain', type=int)
    file_format = request.args.get('file_format', '')
    
    # Ne montrer que les datasets validés
    query = Dataset.query.filter_by(status='validated')
    
    if q:
        query = query.filter(
            db.or_(
                Dataset.title.contains(q),
                Dataset.description.contains(q)
            )
        )
    
    if domain_id:
        query = query.filter_by(domain_id=domain_id)
    
    if file_format:
        query = query.filter_by(file_format=file_format)
    
    datasets = query.order_by(Dataset.creation_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    domains = Domain.query.all()
    
    return render_template('dataset_list.html', datasets=datasets, domains=domains)

@app.route('/datasets/<int:dataset_id>')
def dataset_detail(dataset_id):
    """Détail d'une base de données"""
    dataset = Dataset.query.get_or_404(dataset_id)
    
    # Vérifier que l'utilisateur peut voir ce dataset
    if dataset.status != 'validated' and (not current_user.is_authenticated or 
        (current_user.role != 'admin' and current_user.id != dataset.user_id)):
        flash('Cette base de données n\'est pas accessible.', 'warning')
        return redirect(url_for('dataset_list'))
    
    # Incrémenter le compteur de vues
    dataset.view_count += 1
    db.session.commit()
    
    comments = Comment.query.filter_by(dataset_id=dataset_id).order_by(Comment.created_at.desc()).all()
    
    # Bases similaires (même domaine, seulement validées)
    similar_datasets = Dataset.query.filter_by(
        domain_id=dataset.domain_id, status='validated'
    ).filter(Dataset.id != dataset_id).limit(5).all()
    
    return render_template('dataset_detail.html', dataset=dataset, comments=comments, similar_datasets=similar_datasets)

@app.route('/datasets/<int:dataset_id>/download')
def dataset_download(dataset_id):
    """Téléchargement d'une base de données"""
    dataset = Dataset.query.get_or_404(dataset_id)
    
    # Vérifier les permissions de téléchargement
    can_download = False
    
    # Les admins peuvent télécharger tous les datasets
    if current_user.is_authenticated and current_user.role == 'admin':
        can_download = True
    # Les utilisateurs normaux ne peuvent télécharger que les datasets validés
    elif dataset.status == 'validated':
        can_download = True
    # L'auteur du dataset peut télécharger son propre dataset
    elif current_user.is_authenticated and current_user.id == dataset.user_id:
        can_download = True
    
    if not can_download:
        flash('Vous n\'avez pas les permissions pour télécharger cette base de données.', 'warning')
        return redirect(url_for('dataset_detail', dataset_id=dataset_id))
    
    # Incrémenter le compteur de téléchargements
    dataset.download_count += 1
    db.session.commit()
    
    # Enregistrer le téléchargement
    log = DownloadLog(
        dataset_id=dataset_id,
        user_id=current_user.id if current_user.is_authenticated else None,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent', '')
    )
    db.session.add(log)
    db.session.commit()
    
    # Retourner le fichier
    return send_file(
        dataset.file_path,
        as_attachment=True,
        download_name=f"{dataset.title}.{dataset.file_format}"
    )

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def dataset_upload():
    """Upload d'une nouvelle base de données"""
    if request.method == 'POST':
        # Récupération des données du formulaire
        title = request.form.get('title')
        description = request.form.get('description')
        short_description = request.form.get('short_description', '')
        source = request.form.get('source', '')
        methodology = request.form.get('methodology', '')
        geographic_scope = request.form.get('geographic_scope', '')
        time_period = request.form.get('time_period', '')
        documentation = request.form.get('documentation', '')
        keywords = request.form.get('keywords', '')
        domain_id = request.form.get('domain_id')
        file = request.files.get('file')
        
        # Validation des champs obligatoires
        required_fields = {
            'title': 'Titre',
            'description': 'Description',
            'source': 'Source',
            'documentation': 'Documentation',
            'domain_id': 'Domaine',
            'file': 'Fichier'
        }
        
        missing_fields = []
        for field, label in required_fields.items():
            if field == 'file':
                if not file or file.filename == '':
                    missing_fields.append(label)
            elif not request.form.get(field):
                missing_fields.append(label)
        
        if missing_fields:
            flash(f'Champs obligatoires manquants : {", ".join(missing_fields)}', 'error')
            return render_template('dataset_upload.html', domains=Domain.query.all())
        
        # Validation du fichier
        if file:
            allowed_extensions = {'csv', 'xlsx', 'xls', 'json', 'xml', 'sql', 'zip'}
            file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
            
            if file_extension not in allowed_extensions:
                flash('Type de fichier non autorisé. Formats acceptés : CSV, Excel, JSON, XML, SQL, ZIP', 'error')
                return render_template('dataset_upload.html', domains=Domain.query.all())
        
        # Sauvegarder le fichier
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Créer la documentation enrichie
        enriched_documentation = f"""
CONTEXTE ET MÉTHODOLOGIE

Source des données : {source}
Méthodologie de collecte : {methodology}
Périmètre géographique : {geographic_scope}
Période couverte : {time_period}

DOCUMENTATION DÉTAILLÉE

{documentation}

INFORMATIONS TECHNIQUES
- Format du fichier : {filename.split('.')[-1].upper()}
- Taille du fichier : {os.path.getsize(file_path) / (1024*1024):.2f} MB
- Soumis par : {current_user.username} ({current_user.organization or 'Non spécifiée'})
- Date de soumission : {datetime.now().strftime('%d/%m/%Y à %H:%M')}
"""
        
        # Créer la base de données
        dataset = Dataset(
            title=title,
            description=description,
            short_description=short_description,
            source=source,
            author=current_user.username,
            domain_id=domain_id,
            keywords=keywords,
            documentation=enriched_documentation,
            file_path=file_path,
            file_format=filename.split('.')[-1].lower(),
            file_size=os.path.getsize(file_path),
            user_id=current_user.id,
            status='pending',  # Nouveau système de statuts
            is_validated=False  # Gardé pour compatibilité
        )
        
        db.session.add(dataset)
        db.session.commit()
        
        flash('Base de données soumise avec succès! Elle sera validée par nos administrateurs.', 'success')
        return redirect(url_for('dashboard'))
    
    domains = Domain.query.all()
    return render_template('dataset_upload.html', domains=domains)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Inscription utilisateur"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        organization = request.form.get('organization', '')
        bio = request.form.get('bio', '')
        
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Ce nom d\'utilisateur existe déjà.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Cet email existe déjà.', 'error')
            return render_template('register.html')
        
        user = User(
            username=username,
            email=email,
            organization=organization,
            bio=bio
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Compte créé avec succès! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Connexion utilisateur"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Déconnexion"""
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Tableau de bord utilisateur"""
    # Statistiques utilisateur
    user_stats = {
        'total_datasets': Dataset.query.filter_by(user_id=current_user.id).count(),
        'validated_datasets': Dataset.query.filter_by(user_id=current_user.id, status='validated').count(),
        'pending_datasets': Dataset.query.filter_by(user_id=current_user.id, status='pending').count(),
        'rejected_datasets': Dataset.query.filter_by(user_id=current_user.id, status='rejected').count(),
        'total_downloads': DownloadLog.query.join(Dataset).filter(Dataset.user_id == current_user.id).count(),
        'average_rating': db.session.query(db.func.avg(Comment.rating)).filter(
            Comment.dataset_id.in_(
                db.session.query(Dataset.id).filter_by(user_id=current_user.id)
            )
        ).scalar() or 0
    }
    
    # Bases de données de l'utilisateur
    user_datasets = Dataset.query.filter_by(user_id=current_user.id).order_by(Dataset.creation_date.desc()).all()
    
    # Pour les admins
    pending_datasets = []
    rejected_datasets = []
    validated_datasets = []
    top_datasets = []
    if current_user.role == 'admin':
        # Datasets en attente de validation
        pending_datasets = Dataset.query.filter_by(status='pending').order_by(Dataset.creation_date.desc()).all()
        # Datasets rejetés
        rejected_datasets = Dataset.query.filter_by(status='rejected').order_by(Dataset.creation_date.desc()).all()
        # Datasets validés récents
        validated_datasets = Dataset.query.filter_by(status='validated').order_by(Dataset.creation_date.desc()).limit(10).all()
        # Top datasets par téléchargements
        top_datasets = Dataset.query.filter_by(status='validated').order_by(Dataset.download_count.desc()).limit(10).all()
    
    return render_template('dashboard.html', 
                         user_stats=user_stats,
                         user_datasets=user_datasets,
                         pending_datasets=pending_datasets,
                         rejected_datasets=rejected_datasets,
                         validated_datasets=validated_datasets,
                         top_datasets=top_datasets)

@app.route('/add_comment/<int:dataset_id>', methods=['POST'])
@login_required
def add_comment(dataset_id):
    """Ajouter un commentaire"""
    dataset = Dataset.query.get_or_404(dataset_id)
    rating = request.form.get('rating', type=int)
    comment_text = request.form.get('comment_text', '').strip()
    
    if not comment_text:
        flash('Le commentaire ne peut pas être vide.', 'danger')
        return redirect(url_for('dataset_detail', dataset_id=dataset_id))
    
    comment = Comment(
        dataset_id=dataset_id,
        user_id=current_user.id,
        text=comment_text,
        rating=rating
    )
    
    db.session.add(comment)
    db.session.commit()
    
    flash('Commentaire ajouté avec succès !', 'success')
    return redirect(url_for('dataset_detail', dataset_id=dataset_id))

@app.route('/admin/validate_dataset/<int:dataset_id>', methods=['POST'])
@login_required
def validate_dataset(dataset_id):
    """Valider une base de données (admin seulement)"""
    if current_user.role != 'admin':
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('dashboard'))
    
    dataset = Dataset.query.get_or_404(dataset_id)
    
    # Mettre à jour le statut
    dataset.status = 'validated'
    dataset.is_validated = True
    dataset.rejection_reason = None  # Effacer toute raison de rejet précédente
    
    db.session.commit()
    
    flash(f'Base de données "{dataset.title}" validée avec succès !', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/reject_dataset/<int:dataset_id>', methods=['POST'])
@login_required
def reject_dataset(dataset_id):
    """Rejeter une base de données avec commentaire (admin seulement)"""
    if current_user.role != 'admin':
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('dashboard'))
    
    dataset = Dataset.query.get_or_404(dataset_id)
    rejection_reason = request.form.get('rejection_reason', '').strip()
    
    if not rejection_reason:
        flash('Veuillez fournir une raison pour le rejet.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Mettre à jour le statut
    dataset.status = 'rejected'
    dataset.is_validated = False
    dataset.rejection_reason = rejection_reason
    
    db.session.commit()
    
    flash(f'Base de données "{dataset.title}" rejetée avec succès.', 'warning')
    return redirect(url_for('dashboard'))

@app.route('/admin/dataset_validation/<int:dataset_id>')
@login_required
def dataset_validation_detail(dataset_id):
    """Page de détail pour la validation d'une base de données (admin seulement)"""
    if current_user.role != 'admin':
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('dashboard'))
    
    dataset = Dataset.query.get_or_404(dataset_id)
    return render_template('admin/dataset_validation.html', dataset=dataset)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    """Mettre à jour le profil utilisateur"""
    # Informations de base
    username = request.form['username']
    email = request.form['email']
    organization = request.form.get('organization', '')
    bio = request.form.get('bio', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    # Informations académiques
    education_level = request.form.get('education_level', '')
    diploma = request.form.get('diploma', '')
    field_of_study = request.form.get('field_of_study', '')
    institution = request.form.get('institution', '')
    graduation_year = request.form.get('graduation_year', type=int)
    
    # Informations professionnelles
    job_title = request.form.get('job_title', '')
    department = request.form.get('department', '')
    years_experience = request.form.get('years_experience', type=int)
    expertise_areas = request.form.get('expertise_areas', '')
    
    # Informations de contact
    phone = request.form.get('phone', '')
    linkedin = request.form.get('linkedin', '')
    website = request.form.get('website', '')
    
    # Vérifier si le nom d'utilisateur existe déjà
    existing_user = User.query.filter_by(username=username).first()
    if existing_user and existing_user.id != current_user.id:
        flash('Ce nom d\'utilisateur existe déjà.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Vérifier si l'email existe déjà
    existing_email = User.query.filter_by(email=email).first()
    if existing_email and existing_email.id != current_user.id:
        flash('Cet email est déjà utilisé.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Mettre à jour les informations de base
    current_user.username = username
    current_user.email = email
    current_user.organization = organization
    current_user.bio = bio
    
    # Mettre à jour les informations académiques
    current_user.education_level = education_level
    current_user.diploma = diploma
    current_user.field_of_study = field_of_study
    current_user.institution = institution
    current_user.graduation_year = graduation_year
    
    # Mettre à jour les informations professionnelles
    current_user.job_title = job_title
    current_user.department = department
    current_user.years_experience = years_experience
    current_user.expertise_areas = expertise_areas
    
    # Mettre à jour les informations de contact
    current_user.phone = phone
    current_user.linkedin = linkedin
    current_user.website = website
    
    # Mettre à jour le mot de passe si fourni
    if new_password:
        if new_password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'danger')
            return redirect(url_for('dashboard'))
        current_user.set_password(new_password)
    
    db.session.commit()
    flash('Profil mis à jour avec succès !', 'success')
    return redirect(url_for('dashboard'))

# API Routes
@app.route('/api/search')
def api_search():
    """API de recherche"""
    q = request.args.get('q', '')
    if not q:
        return jsonify({'results': []})
    
    datasets = Dataset.query.filter(
        Dataset.status == 'validated',
        db.or_(
            Dataset.title.contains(q),
            Dataset.description.contains(q)
        )
    ).limit(10).all()
    
    results = []
    for dataset in datasets:
        results.append({
            'id': dataset.id,
            'title': dataset.title,
            'description': dataset.short_description or dataset.description[:100],
            'url': url_for('dataset_detail', dataset_id=dataset.id)
        })
    
    return jsonify({'results': results})

@app.route('/api/stats')
def api_stats():
    """API des statistiques"""
    if not current_user.is_authenticated or current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    stats = {
        'total_datasets': Dataset.query.count(),
        'validated_datasets': Dataset.query.filter_by(status='validated').count(),
        'pending_datasets': Dataset.query.filter_by(status='pending').count(),
        'rejected_datasets': Dataset.query.filter_by(status='rejected').count(),
        'total_users': User.query.count()
    }
    
    return jsonify(stats)

def migrate_existing_datasets():
    """Migrer les datasets existants vers le nouveau système de statuts"""
    with app.app_context():
        # Mettre à jour les datasets existants
        datasets = Dataset.query.all()
        for dataset in datasets:
            if dataset.status is None:
                # Si le statut n'est pas défini, utiliser is_validated
                if dataset.is_validated:
                    dataset.status = 'validated'
                else:
                    dataset.status = 'pending'
        
        db.session.commit()
        print("✅ Migration des datasets terminée!")

def init_db():
    """Initialiser la base de données"""
    with app.app_context():
        db.create_all()
        
        # Créer les domaines par défaut
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
            domain = Domain.query.filter_by(name=domain_data['name']).first()
            if not domain:
                domain = Domain(**domain_data)
                db.session.add(domain)
        
        # Créer un admin par défaut
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@nosdonnees.fr',
                role='admin',
                organization='Nosdonnées'
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        db.session.commit()
        
        # Migrer les datasets existants
        migrate_existing_datasets()
        
        print("✅ Base de données initialisée avec succès!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=8000) 