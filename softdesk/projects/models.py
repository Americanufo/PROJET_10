from django.db import models
from django.conf import settings
import uuid


class Project(models.Model):
    # Choix possibles pour le type de projet
    TYPE_CHOICES = [
        ("back-end", "Back-end"),
        ("front-end", "Front-end"),
        ("iOS", "iOS"),
        ("Android", "Android"),
    ]

    # Titre du projet, champ obligatoire
    title = models.CharField(max_length=255)
    # Description longue, facultative
    description = models.TextField(blank=True)
    # Type du projet, choix restreints à TYPE_CHOICES
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='back-end')
    # Auteur du projet, relation vers User, suppression en cascade
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='projects_created',  # Permet d'accéder aux projets d'un user
        on_delete=models.CASCADE
    )
    # Date de création (auto)
    created_at = models.DateTimeField(auto_now_add=True)
    # Date de dernière modification (auto)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Représentation lisible du projet
        return self.title


class Contributor(models.Model):
    # utilisateur contributeur d'un projet
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='contributions',
        on_delete=models.CASCADE
    )
    # projet associé
    project = models.ForeignKey(
        Project,
        related_name='contributors',
        on_delete=models.CASCADE
    )
    # Date d'ajout du contributeur au projet
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Empêche qu'un utilisateur soit ajouté plusieurs fois au même projet
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} - {self.project.title}"


class Issue(models.Model):
    # Type d'issue possible
    TAG_CHOICES = [
        ('BUG', 'Bug'),
        ('FEATURE', 'Feature'),
        ('TASK', 'Task'),
    ]

    # Statut d'issue possible
    STATUS_CHOICES = [
        ('TO_DO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('FINISHED', 'Finished'),
    ]

    # Titre obligatoire
    title = models.CharField(max_length=255)
    # Description optionnelle
    description = models.TextField(blank=True)
    # Priorité de l'issue (LOW, MEDIUM, HIGH)
    priority = models.CharField(max_length=10, choices=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ])

    tag = models.CharField(max_length=10, choices=TAG_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='TO_DO')

    # L'issue est liée à un projet
    project = models.ForeignKey(
        'Project',
        related_name='issues',
        on_delete=models.CASCADE
    )
    # Attribuée à un contributeur (utilisateur) du projet
    assigned_to = models.ForeignKey(
        'Contributor',
        related_name='assigned_issues',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    # Auteur (créateur) de l'issue
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='issues_created',
        on_delete=models.CASCADE
    )
    # Date de création automatique
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    # Identifiant unique UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Texte du commentaire
    description = models.TextField()
    # Date création automatique
    created_at = models.DateTimeField(auto_now_add=True)
    # Auteur du commentaire (user)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='comments',
        on_delete=models.CASCADE
    )
    # Commentaire lié à une issue
    issue = models.ForeignKey(
        Issue,
        related_name='comments',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Comment by {self.author.username} on {self.issue.title[:20]}"
