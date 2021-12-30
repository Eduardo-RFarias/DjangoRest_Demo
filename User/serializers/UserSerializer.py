from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            "url",
            "username",
            "email",
            "full_name",
            "password",
            "is_active",
            "is_superuser",
            "last_login",
            "date_joined",
        ]
        read_only_fields = [
            "last_login",
            "is_superuser",
            "date_joined",
            "is_active",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def create_superuser(self, validated_data):
        return User.objects.create_superuser(**validated_data)

    def get_fields(self):
        fields = super().get_fields()

        request = self.context.get("request")

        if request:
            method = getattr(request, "method")

            if method == "PUT":
                fields["password"].required = False

        return fields
