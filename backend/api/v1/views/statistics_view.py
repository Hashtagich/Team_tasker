from django.db.models import Count
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from tasks.models import Task
from users.models import CustomUser, Group
from users.permissions import IsNotBlocked


@extend_schema(tags=['Статистика'])
class TaskStatisticsViewSet(viewsets.ViewSet):
    serializer_class = None
    permission_classes = [IsAuthenticated, IsNotBlocked]

    @extend_schema(
        summary="API для получения статистики по задачам исполнителей, где пользователь является руководителем.",
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'total_tasks': {'type': 'integer', 'description': 'Общее количество задач.'},
                    'status_counts': {
                        'type': 'object',
                        'properties': {
                            'done': {'type': 'integer', 'description': 'Количество задач со статусом выполнено.'},
                            'in_work': {'type': 'integer', 'description': 'Количество задач со статусом в работе.'},
                            'new': {'type': 'integer', 'description': 'Количество задач со статусом новая.'},
                        }
                    }
                }
            }
        }
    )
    @action(detail=False, methods=['get'], url_path='leader')
    def get_leader_statistics(self, request, *args, **kwargs):
        user = request.user

        groups_leader = Group.objects.filter(leader=user)
        implementers = CustomUser.objects.filter(groups__in=groups_leader)
        tasks = Task.objects.filter(implementer__in=implementers)

        total_tasks = tasks.count()
        status_counts = tasks.values('status').annotate(count=Count('id'))

        stats = {
            'total_tasks': total_tasks,
            'status_counts': {status['status']: status['count'] for status in status_counts}
        }

        return Response(stats)

    @extend_schema(
        summary="API для получения статистики по статусам всех задач",
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'total_tasks': {'type': 'integer', 'description': 'Общее количество всех задач.'},
                    'status_counts': {
                        'type': 'object',
                        'properties': {
                            'done': {'type': 'integer', 'description': 'Количество задач со статусом выполнено.'},
                            'in_work': {'type': 'integer', 'description': 'Количество задач со статусом в работе.'},
                            'new': {'type': 'integer', 'description': 'Количество задач со статусом новая.'},
                        }
                    }
                }
            }
        }
    )
    @action(detail=False, methods=['get'], url_path='all')
    def all_task_status(self, request):
        total_tasks = Task.objects.count()
        status_counts = Task.objects.values('status').annotate(count=Count('id'))

        stats = {
            'total_tasks': total_tasks,
            'status_counts': {status['status']: status['count'] for status in status_counts}
        }

        return Response(stats)

    @extend_schema(
        summary="API для получения статистики по задачам исполнителя, где пользователь является исполнителем.",
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'total_tasks': {'type': 'integer', 'description': 'Общее количество задач.'},
                    'status_counts': {
                        'type': 'object',
                        'properties': {
                            'done': {'type': 'integer', 'description': 'Количество задач со статусом выполнено.'},
                            'in_work': {'type': 'integer', 'description': 'Количество задач со статусом в работе.'},
                            'new': {'type': 'integer', 'description': 'Количество задач со статусом новая.'},
                        }
                    }
                }
            }
        }
    )
    @action(detail=False, methods=['get'], url_path='implementer')
    def get_implementer_statistics(self, request, *args, **kwargs):
        user = request.user

        tasks = Task.objects.filter(implementer=user)

        total_tasks = tasks.count()
        status_counts = tasks.values('status').annotate(count=Count('id'))

        stats = {
            'total_tasks': total_tasks,
            'status_counts': {status['status']: status['count'] for status in status_counts}
        }

        return Response(stats)
