from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Notification
from .serializers import NotificationSerializer
from accounts.permissions import IsSuperAdmin


class NotificationManagementViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def list(self, request):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=200)
    
    def retrieve(self, request, pk=None):
        try:
            notification = Notification.objects.get(pk=pk)
        except Notification.DoesNotExist:
            return Response({'message': 'Notification not found'}, status=404)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=200)
    
    @action(detail=True, methods=['post'], url_path='mark-as-read')
    def mark_as_read(self, request, pk=None):
        user = request.user
        try:
            notification = Notification.objects.get(pk=pk)
        except Notification.DoesNotExist:
            return Response({'message': 'Notification not found'}, status=404)
        
        notification.status = True
        notification.answered_by = user
        notification.save()
        
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=200)
    
    @action(detail=False, methods=['get'], url_path='gravity/escalation')
    def list_escalation_notifications(self, request):
        notifications = Notification.objects.filter(gravity='escalation')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=200)
    
    @action(detail=False, methods=['get'], url_path='gravity/system')
    def list_system_notifications(self, request):
        notifications = Notification.objects.filter(gravity='system')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=200)
    
    @action(detail=False, methods=['get'], url_path='problem-type/(?P<problem_type>[^/.]+)')
    def list_probleme_by_type(self, request, problem_type=None):
        notifications = Notification.objects.filter(problem_type=problem_type)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=200)