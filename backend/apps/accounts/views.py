from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from .token import generate_email_verification_token, add_token_to_blacklist, create_access_token, create_refresh_token
from .utils.exceptions import EmailSendError

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.conf import settings

from .token import create_access_token
from .utils.email import check_email_throttle
from .task import send_verification_email_task

import jwt

User = get_user_model()
class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "success": True,
            "message": "회원가입이 완료되었습니다. 입력한 이메일로 인증 메일이 발송되었습니다.",
            "user_id": user.id,
            "verification_required": user.is_active is False,
        }, status=status.HTTP_201_CREATED)
            
class SendVerificationEmailView(APIView):
    def post(self, request : Request) -> Response:
        serializer = SendVerificationEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        uid = serializer.validated_data['uid']
        email = serializer.validated_data['email']
        
        check_email_throttle(email)
        
        token = generate_email_verification_token(uid, email)
        
        try:
            send_verification_email_task.delay(email, token)
            return Response({
                "success": True,
                "message": "인증 이메일을 발송하였습니다."
            })
        
        except EmailSendError as e:
            if settings.DEBUG:
                return Response({
                    "success": False, 
                    "message": str(e)
                }, status=500)
            else:
                return Response({
                    "success": False,
                    "message": "이메일 발송에 실패했습니다."
                }, status=500)

class VerifyEmailView(APIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        payload=serializer.validated_data['payload']
        uid=payload.get('user_id')
        jti=payload.get('jti')
        exp=payload.get('exp')

            
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            raise NotFound("존재하지 않는 유저입니다.")
        
        user.is_active=True
        user.save()
        
        if jti and exp:
            add_token_to_blacklist(jti, exp)
            
        return Response({
            "success": True, 
            "message": "이메일 인증이 완료되었습니다."
            })

class LoginView(APIView):
    """LoginView API endpoint for user authentication.

    Methods:
      post : Login    
    """
    def post(self, request: Request) -> Response:
        """Login user with email and password.

        Post /api/v1/accounts/login/
        
        request data:
        {
            "email": "user@example.com",
            "password": "pass1234"
        }
        
        response:
        {
            "success": true,
            "message": "Login successful",
            "access_token": "access_token",
            "refresh_token": "refresh_token"
        }
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, email=email, password=password)
        
        if user: 
            access_token = create_access_token(user)
            refresh_token = create_refresh_token(user)

            user.refresh_token = refresh_token
            user.save(update_fields=['refresh_token'])
            
            return Response({
                "success": True,
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token
                }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request : Request) -> Response:
        user = request.user
        user.refresh_token = None
        user.save()
        return Response({"detail": "로그아웃 완료"}, status=200)
    
class TokenRefreshView(APIView):
    """
    refresh access token using refresh token.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request : Request) -> Response:
        user = request.user
        refresh_token = user.refresh_token
        
        if not refresh_token:
            return Response({
                "error": "No refresh token found"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        try : 
            payload = jwt.decode(
                refresh_token, 
                settings.SECRET_KEY, 
                algorithms=[settings.JWT_ALGORITHM]
            )
            if payload.get('type') != 'refresh':
                raise jwt.InvalidTokenError("Invalid token type")
            
            user_id = payload.get("user_id") 
            new_access_token = create_access_token(user)
            
            if user.refresh_token != refresh_token:
                    return Response({
                        "error": "already fired or changed token"
                        }, status=401)
                
            return Response({
                "success": True,
                "access_token": new_access_token
            }, status=status.HTTP_200_OK)

        except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
            return Response({"error": "invailed token"}, status=401)