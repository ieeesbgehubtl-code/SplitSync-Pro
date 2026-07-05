from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from common.validators import require_cloudinary_url
from .models import User


class UserPublicSerializer(serializers.ModelSerializer):
    mutual_friends_count = serializers.IntegerField(read_only=True, default=0)
    mutual_trips_count = serializers.IntegerField(read_only=True, default=0)
    friend_status = serializers.CharField(read_only=True, default="none")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "full_name",
            "profile_picture",
            "bio",
            "created_at",
            "last_active",
            "mutual_friends_count",
            "mutual_trips_count",
            "friend_status",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, min_length=8, validators=[validate_password]
    )

    def validate_profile_picture(self, value):
        return require_cloudinary_url(value)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "full_name",
            "password",
            "profile_picture",
            "bio",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    def validate_profile_picture(self, value):
        return require_cloudinary_url(value)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "full_name",
            "profile_picture",
            "bio",
            "created_at",
            "last_active",
        ]
        read_only_fields = ["id", "username", "email", "created_at", "last_active"]


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )

    def validate(self, attrs):
        if not self.context["request"].user.check_password(attrs["current_password"]):
            raise serializers.ValidationError("Current password is incorrect.")
        return attrs
