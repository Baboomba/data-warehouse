from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from .models import Info
from .serializer import SignUpSerializer, UserSerializer



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


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializer


class HTTPOnlyLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, *kwargs)
        
        if response.status_code == 200:
            refresh = RefreshToken.for_user(request.user)
            access_token = str(refresh.access_token)
            
            response.set_cookie(key='access_token', value=access_token, httponly=True)
        
        return response


class HTTPOnlyLogoutView(APIView):
    def post(self, request):
        user = request.user

        if user.is_authenticated:
            user.refresh_token.delete()
            
            request.user.is_authenticated = False
            request.session['is_logged_in'] = False

            return Response({'detail': 'Successfully logged out'})
        else:
            return Response({'detail': 'You are not logged in'})
    

class ReadUserView(APIView):
    def get(self, request):
        users = Info.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)