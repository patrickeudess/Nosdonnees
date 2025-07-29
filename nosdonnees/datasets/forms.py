from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Dataset, Domain, UserProfile, Comment


class UserRegistrationForm(UserCreationForm):
    """Formulaire d'inscription utilisateur"""
    email = forms.EmailField(required=True)
    organization = forms.CharField(max_length=200, required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Créer le profil utilisateur
            UserProfile.objects.create(
                user=user,
                organization=self.cleaned_data.get('organization', ''),
                bio=self.cleaned_data.get('bio', '')
            )
        return user


class DatasetUploadForm(forms.ModelForm):
    """Formulaire d'upload de base de données"""
    tags = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Mots-clés séparés par des virgules'}),
        help_text="Séparez les mots-clés par des virgules"
    )
    
    class Meta:
        model = Dataset
        fields = [
            'title', 'description', 'short_description', 'source', 'author',
            'creation_date', 'file', 'file_format', 'domain', 'tags',
            'country', 'language'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'source': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'creation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'file_format': forms.Select(attrs={'class': 'form-control'}),
            'domain': forms.Select(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limiter les domaines disponibles
        self.fields['domain'].queryset = Domain.objects.all()
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Vérifier la taille du fichier (max 100MB)
            if file.size > 100 * 1024 * 1024:
                raise forms.ValidationError("Le fichier ne doit pas dépasser 100MB.")
        return file


class DatasetSearchForm(forms.Form):
    """Formulaire de recherche de bases de données"""
    q = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher par titre, description, mots-clés...'
        })
    )
    domain = forms.ModelChoiceField(
        queryset=Domain.objects.all(),
        required=False,
        empty_label="Tous les domaines",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    file_format = forms.ChoiceField(
        choices=[('', 'Tous les formats')] + Dataset.FORMAT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    country = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pays'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )


class CommentForm(forms.ModelForm):
    """Formulaire de commentaire"""
    class Meta:
        model = Comment
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Votre commentaire...'
            }),
            'rating': forms.Select(attrs={'class': 'form-control'})
        }


class DatasetUpdateForm(forms.ModelForm):
    """Formulaire de mise à jour de base de données"""
    class Meta:
        model = Dataset
        fields = [
            'title', 'description', 'short_description', 'source', 'author',
            'creation_date', 'domain', 'tags', 'country', 'language'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'source': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'creation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'domain': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'})
        }


class AdminValidationForm(forms.ModelForm):
    """Formulaire de validation admin"""
    class Meta:
        model = Dataset
        fields = ['status', 'rejection_reason']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'rejection_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Raison du rejet (si applicable)...'
            })
        } 