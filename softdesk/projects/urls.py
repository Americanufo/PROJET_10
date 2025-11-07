from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet

router = DefaultRouter()

# Enregistre les routes pour chaque ViewSet
router.register('projects', ProjectViewSet, basename='project')
router.register('contributors', ContributorViewSet, basename='contributor')
router.register('issues', IssueViewSet, basename='issue')
router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)), # inclut les routes automatiques générées par DRF router
]
