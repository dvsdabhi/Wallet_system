from rest_framework import serializers
from .models import User, Transaction

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['sender', 'timestamp', 'sender_ip']