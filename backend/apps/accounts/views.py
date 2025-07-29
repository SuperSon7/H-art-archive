from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.conf import settings

from .task import send_verification_email_task
from .serializers import *
from .token import create_access_token,generate_email_verification_token, add_token_to_blacklist, create_access_token, create_refresh_token
from .utils.exceptions import EmailSendError
from .utils.email import check_email_throttle
from .utils.s3_presigner import generate_presigned_url

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
    """Sending Veryfication Email for Singup"""
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
        
class UserInfoViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, pk=None):
        """Retrieve user information by user ID."""
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound("User not found")
        
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """Update user information."""
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound("User not found")
        
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='profile-image')
    def generate_profile_image_url(self, request, pk=None)-> Response:
        """ Generate a presigned URL for uploading a profile image to S3

        Raises:
            NotFound: User not found

        Response:
            "upload_url": S3 presigned URL
            "s3_key": S3 key of image inside the bucket 
        """
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound("User not found")

        serializer = ProfileImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = generate_presigned_url(
            user_id=user.id,
            filename=serializer.validated_data['filename'],
            content_type=serializer.validated_data['content_type']
        )

        return Response({
            "upload_url": url,
            "s3_key": f"user_uploads/{user.id}/{serializer.validated_data['filename']}"
        }, status=status.HTTP_200_OK)
    
    
    @action(detail=True, methods=['post'], url_path='profile-image/save')
    def save_profile_image(self, request, pk=None) -> Response:
        """ Save the profile image URL to the user model after upload

        Raises:
            ValidationError: no key porvieded
            NotFound: User not found
        """
        key = request.data.get("key")
        if not key:
            raise ValidationError("key is required")

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound("User not found")

        user.profile_image_url = f"https://{settings.AWS_S3_PROFILE_BUCKET}.s3.amazonaws.com/{key}"
        user.save(update_fields=["profile_image_url"])

        return Response({"success": True})
    
