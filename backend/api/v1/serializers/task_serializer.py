from rest_framework import serializers
from tasks.models import Task
from .user_serializer import MyUserSerializerForTask


class TaskSerializerForGET(serializers.ModelSerializer):
    datetime_start = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')
    datetime_finish_plan = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')
    datetime_finish_fact = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')
    datetime_create = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')
    author = MyUserSerializerForTask()
    implementer = MyUserSerializerForTask()

    class Meta:
        model = Task
        fields = (
            'name',
            'description',
            'status',
            'author',
            'implementer',
            'datetime_start',
            'datetime_finish_plan',
            'datetime_finish_fact',
            'datetime_create'
        )


class TaskSerializerForPOST(serializers.ModelSerializer):
    datetime_start = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')
    datetime_finish_plan = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')
    datetime_finish_fact = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')
    datetime_create = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')
    author = MyUserSerializerForTask()
    implementer = MyUserSerializerForTask()

    class Meta:
        model = Task
        fields = (
            'name',
            'description',
            'status',
            'author',
            'implementer',
            'datetime_start',
            'datetime_finish_plan',
            'datetime_finish_fact',
            'datetime_create'
        )

        read_only_fields = ("datetime_create",)
