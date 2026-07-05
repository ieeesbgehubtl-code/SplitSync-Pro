from rest_framework import generics, permissions, response, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserPublicSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class=RegisterSerializer; permission_classes=[permissions.AllowAny]
    def create(self, request,*args,**kwargs):
        res=super().create(request,*args,**kwargs)
        return response.Response({'success':True,'data':res.data}, status=status.HTTP_201_CREATED)

class MeView(generics.RetrieveAPIView):
    serializer_class=UserPublicSerializer
    def get_object(self): return self.request.user

class LogoutView(generics.GenericAPIView):
    def post(self, request):
        refresh=request.data.get('refresh')
        if refresh: RefreshToken(refresh).blacklist()
        return response.Response({'success':True})
