from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, ResendVerificationSerializer
from .models import User
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EmailVerificationToken
from django.core.mail import send_mail
from django.conf import settings


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            verification = EmailVerificationToken.objects.get(token=token)
        except EmailVerificationToken.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        if verification.expires_at <= timezone.now():
            verification.delete()
            return Response({'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        verification.user.is_active = True
        verification.user.save(update_fields=['is_active'])
        verification.delete()
        return Response({'detail': 'Email verified successfully'}, status=status.HTTP_200_OK)
            
            
class ResendVerificationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResendVerificationSerializer
    
    def post(self, request):
        serializer = ResendVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data['email'])
        EmailVerificationToken.objects.filter(user=user).delete()
        verification_token = EmailVerificationToken.generate_token(user)
        verification_url = f"{settings.FRONTEND_URL}/verify-email/?token={verification_token.token}"
        send_mail(
            'Verify your email',
            verification_url,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return Response({'detail': 'Verification email sent successfully'}, status=status.HTTP_200_OK)
    
class UserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({'first_name': user.first_name, 'email': user.email}, status=status.HTTP_200_OK)