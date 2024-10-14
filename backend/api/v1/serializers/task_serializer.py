from rest_framework import serializers
from tasks.models import Task
from .user_serializer import MyUserSerializerForTask
from users.models import CustomUser, Group


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
    datetime_start = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S', required=False)
    datetime_finish_plan = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S', required=False)
    datetime_finish_fact = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S', required=False)
    author = MyUserSerializerForTask(read_only=True)
    implementer = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)

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
        )

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return Task.objects.create(**validated_data)

    def validate(self, attrs):
        datetime_start = attrs.get('datetime_start')
        datetime_finish_plan = attrs.get('datetime_finish_plan')
        datetime_finish_fact = attrs.get('datetime_finish_fact')

        if datetime_start and datetime_finish_plan and datetime_finish_fact:
            if datetime_finish_plan <= datetime_start:
                raise serializers.ValidationError("Планируемая дата окончания не может быть раньше даты начала.")

            if datetime_finish_fact <= datetime_start:
                raise serializers.ValidationError("Фактическая дата окончания не может быть раньше даты начала.")

        return attrs
