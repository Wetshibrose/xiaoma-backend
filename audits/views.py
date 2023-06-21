from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions
from knox.auth import TokenAuthentication

from .serializers import AuditsSerializers

from django.contrib.admin.models import LogEntry


class AuditsAPIView(APIView):
    permission_classes = (IsAuthenticated | IsAdminUser,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request: Request, *args, **kwargs):
        logs = LogEntry.objects.all().order_by("-action_time")
        serializers = AuditsSerializers(logs, many=True)
        return Response({"data": serializers.data}, status=status.HTTP_200_OK)
