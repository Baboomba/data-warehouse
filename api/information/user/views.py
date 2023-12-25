from django.contrib.auth import authenticate
from django.conf import settings
from django.middleware import csrf

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from .models import Info
from .serializer import SignUpSerializer, UserSerializer, TokenSerializer



class SignUpView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer =  SignUpSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            password2 = serializer.validated_data['password2']
            
            if password != password2:
                return Response({'error': 'Password do not match'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = Info.objects.create_user(email=email, password=password)
            
            # create JWT
            refresh_token = RefreshToken.for_user(user=user)
            access_token = str(refresh_token.access_token)
            
            response_data = {
                'email': user.email,
                'password': user.password,
                'refresh_token': str(refresh_token),
                'access_token': access_token
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        data = request.data
        response = Response()
        username = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value = data["access"],
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                    domain = settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
                    path = settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                )
                
                csrf.get_token(request)
                response.data = {"Success" : "Login successfully", "data": data}
                return response
            else:
                return Response({"No active" : "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid" : "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)



# class LoginView(TokenObtainPairView):
#     permission_classes = [AllowAny]
#     serializer_class = TokenObtainPairSerializer


# class HTTPOnlyLoginView(LoginView):
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, *kwargs)
        
#         if response.status_code == 200:
#             refresh = RefreshToken.for_user(request.user)
#             access_token = str(refresh.access_token)
            
#             response.set_cookie(key='access_token', value=access_token, httponly=True)
        
#         return response


class HTTPOnlyLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            res = Response()
            res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
            res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
            res.delete_cookie('X-CSRFToken')
            return res
        except:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


# class HTTPOnlyLogoutView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request, *args, **kwargs):
#         access_token = request.data.get('access_token')
#         if access_token:
#             try:
#                 token = RefreshToken(access_token)
#                 token.blacklist()
#             except Exception as e:
#                 return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

#         return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    

class ReadUserView(APIView):
    def get(self, request):
        users = Info.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)