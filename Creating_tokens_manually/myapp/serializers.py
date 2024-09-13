from rest_framework import serializers
from myapp.models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class userRegstrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['email','name','password','password2','tc']
        extra_kwargs={
            'password':{'write_only':True}
        }
#validating passowrd and confirm Password while Regstration
    def validate(self, data):
        # Check if both passwords match
        password=data.get('password')
        password2=data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    #login 
class userLoginSerilaizer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=225)
    class Meta:
        model=User
        fields=['email','password']

class userProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','name']  

class userchangepasswordSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=225,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=225,style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['password','password2']

    def validate(self, data):
        password=data.get('password')
        password2=data.get('password2')
        user=self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        user.set_password(password)
        user.save()
        return data
        
class SendPasswordResteEmialSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email']
    def validate(self, data):
       email=data.get('email')
       if User.objects.filter(email=email).exists():
        user =User.objects.get(email=email)
        uid=urlsafe_base64_encode(force_bytes(user.id))
        token=PasswordResetTokenGenerator().make_token(user)
        link='http://localhost:3000/api/user/reset/'+uid+'/'+token
        return data
       else:
        raise serializers.ValidationError("you are not regster user.")
    