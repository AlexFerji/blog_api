from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer

from .models import CustomUser, Profile


class UserLoginSerializer(LoginSerializer):
    username = serializers.CharField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2']

    def save(self, *args, **kwargs):
        user = CustomUser(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        user.set_password(password)

        user.save()
        Profile.objects.create(user=user)

        return user




class UserListSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='profile.image', required=False)
    first_name = serializers.CharField(source='profile.first_name')
    last_name = serializers.CharField(source='profile.last_name')
    birth_date = serializers.DateField(source='profile.birth_date')
    class Meta:
        model = CustomUser
        fields = ( 'image','username', 'email', 'first_name', 'last_name', 'birth_date')


    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.image = profile_data.get('image', profile.image)
        profile.first_name = profile_data.get('first_name', profile.first_name)
        profile.last_name = profile_data.get('last_name', profile.last_name)
        profile.birth_date = profile_data.get('birth_date', profile.birth_date)
        profile.save()

        return instance





