from rest_framework import serializers
from users.models import CustomUser, Role, Group
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

CustUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustUser
        fields = (
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'password'
        )


class CustomCreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustUser
        fields = (
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'password'
        )


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'title',
        )


class MyUserSerializerForGet(serializers.ModelSerializer):
    role = serializers.CharField(source='role.title', allow_blank=True, default='')
    group = serializers.CharField(source='group.name', allow_blank=True, default='')

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'role',
            'phone',
            'email',
            'is_staff',
            'is_active',
            'is_blocked',
            'group'
        )


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'role',
            'is_staff',
            'is_active',
            'is_blocked'
        )


class MyUserSerializerForTask(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'first_name',
            'last_name',
            'middle_name',
        )


class GroupSerializerForGet(serializers.ModelSerializer):
    datetime_create = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')
    datetime_update = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')
    leader = MyUserSerializerForTask()
    moderators = MyUserSerializerForTask(many=True)
    specialists = MyUserSerializerForTask(many=True)

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'leader',
            'moderators',
            'specialists',
            'datetime_update',
            'datetime_create'
        )


class GroupSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'leader',
            'moderators',
            'specialists',
        )
