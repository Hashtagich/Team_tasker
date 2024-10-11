from api.v1.serializers.user_serializer import (
    CustomCreateUserSerializer,
    MyUserSerializerForGet,
    MyUserSerializer
)
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import CustomUser
from users.permissions import IsAdmin


@extend_schema(tags=['Пользователи'])
class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomCreateUserSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    @extend_schema(
        summary="API для регистрации пользователя",
        request=CustomCreateUserSerializer,
        responses={
            201: OpenApiResponse(description="Пользователь успешно зарегистрирован."),
            400: OpenApiResponse(description="Ошибка в данных запроса.")
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Пользователи'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MyUserSerializerForGet
        else:
            return MyUserSerializer

    @extend_schema(
        summary="API для разблокировки пользователя",
        request=None,
        responses={
            200: OpenApiResponse(description="Пользователь заблокирован."),
        }
    )
    @action(detail=True, methods=['patch'])
    def block_user(self, request, pk=None):
        user = self.get_object()
        user.is_blocked = True
        user.save()
        return Response({"message": f"Пользователь {user} заблокирован."}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="API для разблокировки пользователя",
        request=None,
        responses={
            200: OpenApiResponse(description="Пользователь разблокирован."),
        }
    )
    @action(detail=True, methods=['patch'])
    def unblock_user(self, request, pk=None):
        user = self.get_object()
        user.is_blocked = False
        user.save()
        return Response({"message": f"Пользователь {user} разблокирован."}, status=status.HTTP_200_OK)

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return Response({'error': 'Метод обновления недоступен.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        return Response({'error': 'Метод создания недоступен.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        return Response({'error': 'Метод удаления недоступен.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(summary="API для получения всех пользователей")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="API для получения конкретного пользователя по ID")
    def retrieve(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="API для редактирования конкретного пользователя по ID")
    def partial_update(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
