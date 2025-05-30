# import requests
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer
from .models import User, Wallet
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()

        #  create wallet
        userInstance = User.objects.get(id=serializer.data['id'])
        Wallet.objects.create(inr_balance=0.0, user=userInstance)
        
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return Response({
            'msg':"User login successfully",
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_wallet_balance(request):
    user = request.user
    try:
        wallet = Wallet.objects.get(user_id=user.id)
        return Response({'name':user.name,'inr_balance': wallet.inr_balance})
    except:
        return Response({"detail": "Wallet not found"}, status=404)