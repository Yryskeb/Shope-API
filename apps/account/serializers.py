from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=5, max_length=20, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=5, max_length=20, required=True, write_only=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'password', 'password_confirm', 'first_name', 'last_name',
                  'username')

    def validate(self, attrs):
        phone_number = attrs['phone_number'].strip()
        password_confirm = attrs.pop('password_confirm')
        password = attrs['password']
        if password != password_confirm:
            raise serializers.ValidationError('Password mismatch')
        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError('Wrong password')
        if phone_number[0] != '+':
            attrs['phone_number'] = '+' + phone_number
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


# class RegisterPhoneSerializer(serializers.ModelSerializer):
#     pass




