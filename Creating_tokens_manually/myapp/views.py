from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from myapp.models import User
from myapp.serializers import userRegstrationSerializer,userLoginSerilaizer,userProfileSerializer,userchangepasswordSerializer,SendPasswordResteEmialSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


#generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
#h

class userRegistration(APIView):
    def post(self,request):
        serializer=userRegstrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'regstration succes'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class userLoginView(APIView):
    def post(self,request):
        serializer=userLoginSerilaizer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'login succes'},status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid email or password'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
#get request
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = userProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserchangePassword(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer=userchangepasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'changed password'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
class SendPasswordResetEmialview(APIView):
    def post(self,request):
        serializer=SendPasswordResteEmialSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset Link Sent.Please check your email'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

