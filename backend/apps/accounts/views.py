from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializer
     
class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "success": True,
                "message": "회원가입이 완료되었습니다.",
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
            
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)