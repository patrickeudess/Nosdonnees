# Generated manually for Nosdonnées

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('icon', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'verbose_name': 'Domaine',
                'verbose_name_plural': 'Domaines',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('visitor', 'Visiteur'), ('contributor', 'Contributeur'), ('admin', 'Administrateur')], default='visitor', max_length=20)),
                ('bio', models.TextField(blank=True, null=True)),
                ('organization', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('short_description', models.CharField(blank=True, max_length=300)),
                ('source', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('creation_date', models.DateField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='datasets/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv', 'xlsx', 'json', 'xml', 'sql', 'zip'])])),
                ('file_format', models.CharField(choices=[('csv', 'CSV'), ('xlsx', 'Excel'), ('json', 'JSON'), ('xml', 'XML'), ('sql', 'SQL'), ('other', 'Autre')], max_length=10)),
                ('file_size', models.PositiveIntegerField(blank=True, help_text='Taille en bytes', null=True)),
                ('tags', models.CharField(blank=True, help_text='Mots-clés séparés par des virgules', max_length=500)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('language', models.CharField(default='fr', max_length=10)),
                ('status', models.CharField(choices=[('draft', 'Brouillon'), ('pending', 'En attente de validation'), ('published', 'Publié'), ('rejected', 'Rejeté')], default='draft', max_length=20)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('validated_at', models.DateTimeField(blank=True, null=True)),
                ('rejection_reason', models.TextField(blank=True)),
                ('download_count', models.PositiveIntegerField(default=0)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('row_count', models.PositiveIntegerField(blank=True, null=True)),
                ('column_count', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datasets', to='datasets.domain')),
                ('submitted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitted_datasets', to='auth.user')),
                ('validated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='validated_datasets', to='auth.user')),
            ],
            options={
                'verbose_name': 'Base de données',
                'verbose_name_plural': 'Bases de données',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='DatasetVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_number', models.PositiveIntegerField()),
                ('file', models.FileField(upload_to='datasets/versions/')),
                ('changelog', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='datasets.dataset')),
            ],
            options={
                'unique_together': {('dataset', 'version_number')},
                'ordering': ['-version_number'],
            },
        ),
        migrations.CreateModel(
            name='DownloadLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.TextField(blank=True)),
                ('downloaded_at', models.DateTimeField(auto_now_add=True)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='download_logs', to='datasets.dataset')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='downloads', to='auth.user')),
            ],
            options={
                'ordering': ['-downloaded_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('rating', models.PositiveSmallIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='datasets.dataset')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auth.user')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ] 