from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from .serializers import SignUpSerializer,SendVerificationEmailSerializer, VerifyEmailSerializer
from .utils.email import send_verification_email
from .token import generate_email_verification_token, add_token_to_blacklist
from .utils.exceptions import EmailSendError

from django.contrib.auth import get_user_model
from django.conf import settings

from .utils.email import check_email_throttle
from .task import send_verification_email_task
User = get_user_model()
class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "success": True,
            "message": "회원가입이 완료되었습니다. 입력한 이메일로 인증 메일이 발송되었습니다.",
            "user_id": user.id
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


#TODO
# 1. 토큰 블랙리스트

# 사용된 토큰 재사용 방지
# Redis나 DB에 사용된 토큰 ID 저장
# 재시도 정책
# 캐시 vs DB: 어떤 방식으로 인증 코드를 저장할까?
# 동기 vs 비동기: 이메일 발송을 어떻게 처리할까?