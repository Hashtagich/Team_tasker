from api.v1.serializers.task_serializer import (
    TaskSerializerForGET,
    TaskSerializerForPOST
)
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from tasks.models import Task
from users.permissions import IsNotBlocked


@extend_schema(tags=['Задачи'])
class SlotViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    permission_classes = [IsAuthenticated, IsNotBlocked]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskSerializerForGET
        else:
            return TaskSerializerForPOST

    @extend_schema(summary="API для получения всех задач")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="API для получения конкретной задачи по ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
