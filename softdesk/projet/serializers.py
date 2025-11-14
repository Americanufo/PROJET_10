from rest_framework import serializers
from .models import User


# Serializer pour le modèle User
class UserSerializer(serializers.ModelSerializer):
    # Champ mot de passe en écriture seule pour sécurité
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        # Champs exposés, le password ne sera pas visible dans la réponse API
        fields = ['id', 'username', 'email', 'age', 'can_be_contacted', 'can_data_be_shared', 'password']

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError("L'âge doit être au moins de 15 ans.")
        return value

    # Surcharge de la méthode create pour gérer correctement le hash du password
    def create(self, validated_data):
        password = validated_data.pop('password')  # Extraire le mot de passe
        user = User(**validated_data)  # Créer l'utilisateur sans le mot de passe
        user.set_password(password)  # Hasher le mot de passe avec la méthode Django native
        user.save()  # Sauvegarder l'utilisateur dans la base
        return user
