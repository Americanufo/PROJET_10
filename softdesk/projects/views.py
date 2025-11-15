from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer
from .models import Issue, Comment
from .serializers import IssueSerializer, CommentSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ne retourne que les projets où l'utilisateur est auteur ou contributeur
        user = self.request.user
        return Project.objects.filter(
            Q(author=user) | Q(contributors__user=user)
        ).distinct().select_related('author').prefetch_related('contributors')

    def perform_create(self, serializer):
        # Création projet avec auteur attaché
        project = serializer.save(author=self.request.user)
        # Auteur ajouté aussi comme contributeur automatiquement
        Contributor.objects.create(user=self.request.user, project=project)

    def perform_update(self, serializer):
        # Seul l'auteur du projet peut le modifier
        if self.get_object().author != self.request.user:
            raise PermissionDenied("Seul l'auteur peut modifier ce projet.")
        serializer.save()

    def perform_destroy(self, instance):
        # Seul l'auteur peut supprimer un projet
        if instance.author != self.request.user:
            raise PermissionDenied("Seul l'auteur peut supprimer ce projet.")
        instance.delete()


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # L’auteur du projet voit tous les contributeurs de ses projets seulement
        user = self.request.user
        return Contributor.objects.filter(
            project__author=user
        ).distinct().select_related('user', 'project')

    def perform_create(self, serializer):
        user = self.request.user
        project = serializer.validated_data['project']
        chosen_user = serializer.validated_data['user']  # utilisateur choisi pour être contributeur

        # Contrôle strict : seul l'auteur peut ajouter un contributeur au projet
        if project.author != user:
            raise PermissionDenied("Seul l'auteur peut ajouter un contributeur à ce projet.")

        # Contrôle unicité : évite de réajouter un même contributeur
        if Contributor.objects.filter(user=chosen_user, project=project).exists():
            raise ValidationError("Cet utilisateur est déjà contributeur de ce projet.")

        # Si tout est ok, on crée le contributeur
        serializer.save()

    def perform_update(self, serializer):
        # Seul l'auteur du projet peut modifier un contributeur
        if serializer.instance.project.author != self.request.user:
            raise PermissionDenied("Seul l'auteur peut modifier ce contributeur.")
        serializer.save()

    def perform_destroy(self, instance):
        # Seul l'auteur du projet peut supprimer un contributeur
        if instance.project.author != self.request.user:
            raise PermissionDenied("Seul l'auteur peut supprimer ce contributeur.")
        instance.delete()


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # L’utilisateur accède aux issues des projets où il est contributeur ou auteur
        # Optimisation des relations afin d’éviter des requêtes inutiles (select_related et prefetch_related)
        return Issue.objects.filter(
            Q(project__author=user) | Q(project__contributors__user=user)
        ).distinct().select_related('author', 'assigned_to', 'project').prefetch_related('comments')

    def perform_create(self, serializer):
        user = self.request.user
        project = serializer.validated_data['project']

        # Vérifie que l'utilisateur est contributeur du projet avant création
        if not project.contributors.filter(user=user).exists():
            raise PermissionDenied("Vous devez être contributeur du projet pour créer une issue.")

        # Assignation automatique de l’utilisateur connecté en tant que contributeur assigné
        assigned_contrib = project.contributors.get(user=user)

        # Enregistre l’issue avec l’auteur et l’assigné (contributeur connecté)
        serializer.save(author=user, assigned_to=assigned_contrib)

    def perform_update(self, serializer):
        # Seul l’auteur de l’issue peut modifier
        if self.get_object().author != self.request.user:
            raise PermissionDenied("Seul l'auteur peut modifier cette issue.")
        serializer.save()

    def perform_destroy(self, instance):
        # Seul l'auteur de l’issue peut supprimer
        if instance.author != self.request.user:
            raise PermissionDenied("Seul l'auteur peut supprimer cette issue.")
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # L’utilisateur a accès aux commentaires des issues des projets où il est contributeur ou auteur
        return Comment.objects.filter(
            Q(issue__project__author=user) | Q(issue__project__contributors__user=user)
        ).distinct().select_related('author', 'issue')

    def perform_create(self, serializer):
        # L’auteur du commentaire est user connecté
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        # Seul l'auteur du commentaire peut modifier
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Seul l'auteur peut modifier ce commentaire.")
        serializer.save()

    def perform_destroy(self, instance):
        # Seul l'auteur du commentaire peut supprimer
        if instance.author != self.request.user:
            raise PermissionDenied("Seul l'auteur peut supprimer ce commentaire.")
        instance.delete()
