from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['user', 'description']


class UserSerializer(serializers.ModelSerializer):
    address = serializers.CharField(max_length=500)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'address']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop('password', None)
        address = validated_data.pop('address', None)
        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
            instance.save()

        instance_address, created = Address.objects.update_or_create(user=instance, description=address)
        if created:
            instance.address = instance_address
        instance.save()

        return instance

