from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Project, Contributor
from .models import Issue, Comment

# Récupère dynamiquement le modèle utilisateur personnalisé de ton projet
User = get_user_model()

class ContributorNestedSerializer(serializers.ModelSerializer):
    # Affiche username lié au contributeur
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Contributor
        # Affiche id, et username de l'utilisateur
        fields = ['id', 'user']


class ProjectSerializer(serializers.ModelSerializer):
    # Affiche username de l'auteur, lecture seule
    author = serializers.ReadOnlyField(source='author.username')
    # Liste imbriquée des contributeurs (avec username), lecture seule (pas modifiable ici)
    contributors = ContributorNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        # Champs exposés via l’API
        fields = ['id', 'title', 'description', 'type', 'author', 'contributors', 'created_at', 'updated_at']


class ContributorSerializer(serializers.ModelSerializer):
    # Champ user pour lecture : affiche le nom d'utilisateur de l'utilisateur lié
    user = serializers.ReadOnlyField(source='user.username')
    # Champ user pour écriture : permet de spécifier un utilisateur en passant son ID (clé primaire)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),  # queryset ajusté avec le modèle User personnalisé
        source='user',  # lie ce champ au champ user du modèle Contributor
        write_only=True  # champ non présent en sortie, uniquement en écriture
    )

    # Affiche titre du projet en lecture seule pour informations dans la réponse API
    project_title = serializers.ReadOnlyField(source='project.title')

    class Meta:
        model = Contributor
        # On expose : id, user en lecture (username), user_id en écriture (clé primaire), projet, titre projet, date création
        fields = ['id', 'user', 'user_id', 'project', 'project_title', 'created_at']


class IssueSerializer(serializers.ModelSerializer):
    # Affiche le nom d'utilisateur de l’auteur
    author = serializers.ReadOnlyField(source='author.username')
    # Affiche l’utilisateur assigné (contributeur) en lecture seulement avec username
    assigned_to = serializers.StringRelatedField()  # Affiche __str__ de Contributor (à adapter si besoin)

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'priority', 'tag', 'status',
            'project', 'assigned_to', 'author', 'created_at'
        ]


class CommentSerializer(serializers.ModelSerializer):
    # Affiche le nom d’utilisateur de l’auteur du commentaire
    author = serializers.ReadOnlyField(source='author.username')
    # Doit contenir description et être lié à une issue et auteur
    class Meta:
        model = Comment
        fields = ['id', 'description', 'created_at', 'author', 'issue']
