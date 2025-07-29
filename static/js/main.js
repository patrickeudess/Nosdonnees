// Nosdonnées - JavaScript principal

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialisation des tooltips Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialisation des popovers Bootstrap
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Animation des cartes au scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // Observer les cartes
    document.querySelectorAll('.card').forEach(card => {
        observer.observe(card);
    });
    
    // Gestion du formulaire de recherche
    const searchForm = document.querySelector('form[action*="dataset_list"]');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="q"]');
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                // Recherche en temps réel (optionnel)
                console.log('Recherche:', searchInput.value);
            }, 500);
        });
    }
    
    // Gestion des filtres
    const filterSelects = document.querySelectorAll('select[name="domain"], select[name="file_format"]');
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            // Auto-submit du formulaire quand un filtre change
            const form = select.closest('form');
            if (form) {
                form.submit();
            }
        });
    });
    
    // Confirmation de suppression
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
                e.preventDefault();
            }
        });
    });
    
    // Gestion des uploads de fichiers
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                // Afficher le nom du fichier sélectionné
                const fileName = file.name;
                const fileSize = (file.size / 1024 / 1024).toFixed(2); // MB
                
                // Créer ou mettre à jour l'affichage du fichier
                let fileDisplay = this.parentNode.querySelector('.file-display');
                if (!fileDisplay) {
                    fileDisplay = document.createElement('div');
                    fileDisplay.className = 'file-display mt-2';
                    this.parentNode.appendChild(fileDisplay);
                }
                
                fileDisplay.innerHTML = `
                    <div class="alert alert-info">
                        <i class="fas fa-file me-2"></i>
                        <strong>${fileName}</strong> (${fileSize} MB)
                    </div>
                `;
                
                // Validation de la taille du fichier
                const maxSize = 100; // MB
                if (file.size > maxSize * 1024 * 1024) {
                    fileDisplay.innerHTML = `
                        <div class="alert alert-danger">
                            <i class="fas fa-exclamation-triangle me-2"></i>
                            Le fichier est trop volumineux. Taille maximale : ${maxSize} MB
                        </div>
                    `;
                    this.value = '';
                }
            }
        });
    });
    
    // Gestion des commentaires
    const commentForms = document.querySelectorAll('.comment-form');
    commentForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const textarea = this.querySelector('textarea');
            if (textarea.value.trim().length < 10) {
                e.preventDefault();
                alert('Le commentaire doit contenir au moins 10 caractères.');
                textarea.focus();
            }
        });
    });
    
    // Gestion des étoiles de notation
    const ratingStars = document.querySelectorAll('.rating-stars .star');
    ratingStars.forEach(star => {
        star.addEventListener('click', function() {
            const rating = this.dataset.rating;
            const container = this.closest('.rating-stars');
            
            // Mettre à jour l'affichage des étoiles
            container.querySelectorAll('.star').forEach(s => {
                if (s.dataset.rating <= rating) {
                    s.classList.add('active');
                } else {
                    s.classList.remove('active');
                }
            });
            
            // Mettre à jour la valeur cachée
            const hiddenInput = container.querySelector('input[type="hidden"]');
            if (hiddenInput) {
                hiddenInput.value = rating;
            }
        });
    });
    
    // Gestion des onglets
    const tabLinks = document.querySelectorAll('[data-bs-toggle="tab"]');
    tabLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const target = this.getAttribute('href');
            const tab = document.querySelector(target);
            if (tab) {
                // Sauvegarder l'onglet actif dans localStorage
                localStorage.setItem('activeTab', target);
            }
        });
    });
    
    // Restaurer l'onglet actif au chargement
    const activeTab = localStorage.getItem('activeTab');
    if (activeTab) {
        const tabLink = document.querySelector(`[href="${activeTab}"]`);
        if (tabLink) {
            const tab = new bootstrap.Tab(tabLink);
            tab.show();
        }
    }
    
    // Gestion des notifications toast
    function showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            // Créer le container s'il n'existe pas
            const container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container position-fixed top-0 end-0 p-3';
            container.style.zIndex = '1055';
            document.body.appendChild(container);
        }
        
        const toastId = 'toast-' + Date.now();
        const toastHtml = `
            <div id="${toastId}" class="toast" role="alert">
                <div class="toast-header">
                    <strong class="me-auto">Nosdonnées</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
                </div>
                <div class="toast-body">
                    ${message}
                </div>
            </div>
        `;
        
        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
        
        // Supprimer le toast après qu'il soit caché
        toastElement.addEventListener('hidden.bs.toast', function() {
            this.remove();
        });
    }
    
    // Exposer la fonction showToast globalement
    window.showToast = showToast;
    
    // Gestion des erreurs AJAX
    document.addEventListener('ajax:error', function(e) {
        showToast('Une erreur est survenue. Veuillez réessayer.', 'error');
    });
    
    // Gestion des succès AJAX
    document.addEventListener('ajax:success', function(e) {
        showToast('Opération réussie !', 'success');
    });
    
    // Auto-hide des alertes après 5 secondes
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Gestion du mode sombre (optionnel)
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            const isDark = document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', isDark);
            
            showToast(
                isDark ? 'Mode sombre activé' : 'Mode clair activé',
                'info'
            );
        });
        
        // Restaurer le mode au chargement
        const savedDarkMode = localStorage.getItem('darkMode') === 'true';
        if (savedDarkMode) {
            document.body.classList.add('dark-mode');
        }
    }
    
    console.log('✅ JavaScript Nosdonnées chargé avec succès !');
}); 