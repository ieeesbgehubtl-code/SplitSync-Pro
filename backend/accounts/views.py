from rest_framework import generics, permissions, response, status, views
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer,
    UserPublicSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        return response.Response(
            {"success": True, "data": res.data}, status=status.HTTP_201_CREATED
        )


class MeView(generics.RetrieveUpdateAPIView):
    def get_serializer_class(self):
        return (
            ProfileSerializer
            if self.request.method in ["PUT", "PATCH"]
            else UserPublicSerializer
        )

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)
        return response.Response({"success": True, "data": res.data})


class ChangePasswordView(views.APIView):
    def post(self, request):
        ser = ChangePasswordSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        request.user.set_password(ser.validated_data["new_password"])
        request.user.save(update_fields=["password"])
        return response.Response({"success": True})


class DeleteAccountView(views.APIView):
    def delete(self, request):
        request.user.is_active = False
        request.user.save(update_fields=["is_active"])
        return response.Response({"success": True}, status=status.HTTP_204_NO_CONTENT)


class LogoutView(generics.GenericAPIView):
    def post(self, request):
        refresh = request.data.get("refresh")
        if refresh:
            RefreshToken(refresh).blacklist()
        return response.Response({"success": True})
