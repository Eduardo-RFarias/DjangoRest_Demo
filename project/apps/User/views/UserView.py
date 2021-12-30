from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..models import User
from ..serializers import UserSerializer


class UserView(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    permission_classes = [IsAuthenticated]

    def destroy(self, request, pk=None):
        user = get_object_or_404(self.get_queryset(), pk=pk)
        user.is_active = False
        user.save()

        return Response(self.get_serializer(user).data, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=False)
    def create_superuser(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        created = serializer.create_superuser(serializer.data)
        headers = self.get_success_headers(serializer.data)

        return Response(created, status=status.HTTP_201_CREATED, headers=headers)
