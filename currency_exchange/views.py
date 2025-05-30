# import requests
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer, TransactionSerializer
from .models import User, Wallet, Transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.db import transaction as db_transaction 
from django.db.models import Q
from django.utils.dateparse import parse_date

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
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_amount(request):
    sender = request.user
    receiver_email = request.data.get('receiver_email')
    amount = request.data.get('amount')
    
    try:
        receiver = User.objects.get(email=receiver_email)
    except User.DoesNotExist:
        return Response({"error": "Receiver not found"}, status=404)
    
    try:
        sender_wallet = Wallet.objects.get(user_id=sender.id)
        receiver_wallet = Wallet.objects.get(user_id=receiver.id)
    except Wallet.DoesNotExist:
        return Response({"error": "Sender or Receiver wallet not found"}, status=404)
    
    if sender_wallet.inr_balance < amount:
        return Response({"error": "Insufficient balance"}, status=400)
    
    with db_transaction.atomic():
        sender_wallet.inr_balance -= amount
        receiver_wallet.inr_balance += amount
        sender_wallet.save()
        receiver_wallet.save()
        
        transaction = Transaction.objects.create(
            sender=sender,
            receiver=receiver,
            amount=amount,
            sender_ip=get_client_ip(request)
        )
    serializer = TransactionSerializer(transaction)
    return Response(serializer.data, status=201)
   
        
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transaction(request):
    user = request.user
    tx_type = str(request.GET.get('tx_type')).lower()
    from_date = request.GET.get('date_from')
    to_date = request.GET.get('to_date')
    
    transactions = Transaction.objects.filter(Q(sender=user) | Q(receiver=user))
    
    if tx_type == 'sent':
        transactions = transactions.filter(sender=user)
    elif tx_type == 'received':
        transactions = transactions.filter(receiver=user)
        
    if from_date:
        transactions = transactions.filter(timestamp__date__gte=parse_date(from_date))
    if to_date:
        transactions = transactions.filter(timestamp__date__lte=parse_date(to_date))

    data = []
    for tx in transactions:
        data.append({
            "id": tx.id,
            "sender_email": tx.sender.email,
            "sender_name": tx.sender.name,
            "receiver_email" : tx.receiver.email,
            "receiver_name" : tx.receiver.name,
            "amount": float(tx.amount),
            "date": tx.timestamp.strftime("%Y-%m-%d %H:%M"),
            "ip": tx.sender_ip,
        })
    return Response(data)