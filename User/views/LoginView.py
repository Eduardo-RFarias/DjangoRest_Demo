from ..models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import get_object_or_404
from django.utils import timezone
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework.response import Response


class LoginView(KnoxLoginView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        user = get_object_or_404(User, email=request.data.get("email"))

        if not check_password(request.data.get("password"), user.password):
            return Response(
                {"error": "Email and/or password are incorrect"},
                status=status.HTTP_403_FORBIDDEN,
            )

        token_limit_per_user = self.get_token_limit_per_user()

        if token_limit_per_user is not None:
            now = timezone.now()
            token = User.objects.auth_token_set.filter(expiry__gt=now)
            if token.count() >= token_limit_per_user:
                return Response(
                    {"error": "Maximum amount of tokens allowed per user exceeded."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(user, token_ttl)
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        UserSerializer = self.get_user_serializer_class()

        data = {"expiry": instance.expiry, "token": token}
        if UserSerializer is not None:
            data["user"] = UserSerializer(user, context=self.get_context()).data
        return Response(data)
