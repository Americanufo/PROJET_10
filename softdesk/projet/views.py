from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

class UserPagination(LimitOffsetPagination):
    default_limit = 10


# ViewSet pour gérer les utilisateurs
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # Tous les utilisateurs
    serializer_class = UserSerializer  # Serializer défini ci-dessus
    pagination_class = UserPagination    # Pagination 10 par page
    
    # Gestion des permissions selon l'action (création ouverte à tous, autre requête nécessite authentification)
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]  # Création sans authentification obligatoire
        else:
            permission_classes = [IsAuthenticated]  # Autres actions nécessitent une authentification
        return [permission() for permission in permission_classes]
