from api.v1.serializers.user_serializer import (
    CustomCreateUserSerializer,
    MyUserSerializerForGet,
    MyUserSerializer,
    GroupSerializerForGet,
    GroupSerializerForPost
)
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import CustomUser, Group
from users.permissions import IsAdmin, IsNotBlocked, IsModerator


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
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(summary="API для редактирования конкретного пользователя по ID")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


@extend_schema(tags=['Группы/Команды'])
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated, IsNotBlocked]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GroupSerializerForGet
        else:
            return GroupSerializerForPost

    @extend_schema(summary="API для получения всех групп/команд")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="API для получения конкретной группы/команды по ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(summary="API для частичного редактирования конкретной группы/команды по ID")
    def partial_update(self, request, *args, **kwargs):
        self.permission_classes = [IsModerator]
        self.check_permissions(request)

        group = self.get_object()

        current_moderators = list(group.moderators.values_list('id', flat=True))
        current_specialists = list(group.specialists.values_list('id', flat=True))
        current_leader = group.leader.id if group.leader else None

        serializer = self.get_serializer(group, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        group = serializer.save()

        leader_id = request.data.get('leader')
        if leader_id is not None:
            try:
                leader = CustomUser.objects.get(id=leader_id)
                if current_leader != leader_id:
                    if current_leader:
                        current_leader_user = CustomUser.objects.get(id=current_leader)
                        current_leader_user.groups.remove(group)
                    group.leader = leader
                    leader.groups.add(group)
            except ObjectDoesNotExist:
                return Response({"detail": "Лидер не найден."}, status=status.HTTP_400_BAD_REQUEST)

        moderators_ids = request.data.get('moderators', [])

        for moderator_id in moderators_ids:
            try:
                moderator = CustomUser.objects.get(id=moderator_id)
                group.moderators.add(moderator)
                moderator.groups.add(group)
            except ObjectDoesNotExist:
                return Response({"detail": f"Модератор с ID {moderator_id} не найден."},
                                status=status.HTTP_400_BAD_REQUEST)

        for current_moderator_id in current_moderators:
            if current_moderator_id not in moderators_ids:
                group.moderators.remove(current_moderator_id)
                CustomUser.objects.get(id=current_moderator_id).groups.remove(group)

        specialists_ids = request.data.get('specialists', [])

        for specialist_id in specialists_ids:
            try:
                specialist = CustomUser.objects.get(id=specialist_id)
                group.specialists.add(specialist)
                specialist.groups.add(group)
            except ObjectDoesNotExist:
                return Response({"detail": f"Специалист с ID {specialist_id} не найден."},
                                status=status.HTTP_400_BAD_REQUEST)

        for current_specialist_id in current_specialists:
            if current_specialist_id not in specialists_ids:
                group.specialists.remove(current_specialist_id)
                CustomUser.objects.get(id=current_specialist_id).groups.remove(group)

        return Response(GroupSerializerForGet(group).data, status=status.HTTP_200_OK)

    @extend_schema(summary="API для полного редактирования конкретной группы/команды по ID")
    def update(self, request, *args, **kwargs):
        self.permission_classes = [IsModerator]
        self.check_permissions(request)

        group = self.get_object()

        current_moderators = list(group.moderators.values_list('id', flat=True))
        current_specialists = list(group.specialists.values_list('id', flat=True))
        current_leader = group.leader.id if group.leader else None

        serializer = self.get_serializer(group, data=request.data)
        serializer.is_valid(raise_exception=True)

        group = serializer.save()

        leader_id = request.data.get('leader')
        if leader_id is not None:
            try:
                leader = CustomUser.objects.get(id=leader_id)

                if current_leader != leader_id:
                    if current_leader:
                        current_leader_user = CustomUser.objects.get(id=current_leader)
                        current_leader_user.groups.remove(group)
                    group.leader = leader
                    leader.groups.add(group)
            except ObjectDoesNotExist:
                return Response({"detail": "Лидер не найден."}, status=status.HTTP_400_BAD_REQUEST)

        moderators_ids = request.data.get('moderators', [])
        group.moderators.clear()
        for moderator_id in moderators_ids:
            try:
                moderator = CustomUser.objects.get(id=moderator_id)
                group.moderators.add(moderator)
                moderator.groups.add(group)
            except ObjectDoesNotExist:
                return Response({"detail": f"Модератор с ID {moderator_id} не найден."},
                                status=status.HTTP_400_BAD_REQUEST)

        for current_moderator_id in current_moderators:
            if current_moderator_id not in moderators_ids:
                group.moderators.remove(current_moderator_id)
                CustomUser.objects.get(id=current_moderator_id).groups.remove(group)

        specialists_ids = request.data.get('specialists', [])
        group.specialists.clear()
        for specialist_id in specialists_ids:
            try:
                specialist = CustomUser.objects.get(id=specialist_id)
                group.specialists.add(specialist)
                specialist.groups.add(group)
            except ObjectDoesNotExist:
                return Response({"detail": f"Специалист с ID {specialist_id} не найден."},
                                status=status.HTTP_400_BAD_REQUEST)

        for current_specialist_id in current_specialists:
            if current_specialist_id not in specialists_ids:
                group.specialists.remove(current_specialist_id)
                CustomUser.objects.get(id=current_specialist_id).groups.remove(group)

        return Response(GroupSerializerForGet(group).data, status=status.HTTP_200_OK)

    @extend_schema(summary="API для создания группы/команды")
    def create(self, request, *args, **kwargs):
        self.permission_classes = [IsAdmin]
        self.check_permissions(request)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group = serializer.save()

        leader_id = request.data.get('leader')
        if leader_id:
            try:
                leader = CustomUser.objects.get(id=leader_id)
                group.leader = leader
                group.save()
                leader.groups.add(group)
            except ObjectDoesNotExist:
                return Response({"detail": "Лидер не найден."}, status=status.HTTP_400_BAD_REQUEST)

        moderators_ids = request.data.get('moderators', [])
        for moderator_id in moderators_ids:
            try:
                moderator = CustomUser.objects.get(id=moderator_id)
                group.moderators.add(moderator)
                moderator.groups.add(group)
            except ObjectDoesNotExist:
                return Response({"detail": f"Модератор с ID {moderator_id} не найден."},
                                status=status.HTTP_400_BAD_REQUEST)

        specialists_ids = request.data.get('specialists', [])
        for specialist_id in specialists_ids:
            try:
                specialist = CustomUser.objects.get(id=specialist_id)
                group.specialists.add(specialist)
                specialist.groups.add(group)
            except ObjectDoesNotExist:
                return Response({"detail": f"Специалист с ID {specialist_id} не найден."},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(GroupSerializerForGet(group).data, status=status.HTTP_201_CREATED)

    @extend_schema(summary="API для удаления конкретной группы/команды по ID")
    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [IsAdmin]
        self.check_permissions(request)
        return super().destroy(request, *args, **kwargs)
