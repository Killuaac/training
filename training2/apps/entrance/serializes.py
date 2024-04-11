from rest_framework import serializers

from .models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'fio')

    def save(self):
        user = CustomUser(
            username=self.validated_data['email'],
            email=self.validated_data['email'],
            fio=self.validated_data['fio']
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user


class AuthorizationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)
