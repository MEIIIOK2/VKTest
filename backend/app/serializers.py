from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from app.models import CustomUser, Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['file']
        

class RegisterSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CustomUser
        fields = ['email','password']

class LoginSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CustomUser
        fields = ['email','password']
        extra_kwargs = {
            'email': {'validators': []},
        }
        
    
    def create(self):
        user = CustomUser.objects.get(email=self.validated_data['email'])
        return user
class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CustomUser
        fields ='__all__'
