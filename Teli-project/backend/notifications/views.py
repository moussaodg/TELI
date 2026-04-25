from django.shortcuts import render

from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer
from accounts.models import Administrator, role
from rest_framework.response import Response
from rest_framework.decorators import action


class NotificationManagementViewset(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def list(self, request):
        user = request.user
        if not user.is_authenticated or not user.role or user.role.authorisation != 'superadmin':
            return Response({'message': 'User not authenticated'}, status=401)
        
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=200)
    
    def mark_as_read(self, request, pk=None):
        user = request.user
        if not user.is_authenticated or not user.role or user.role.authorisation != 'superadmin':
            return Response({'message': 'User not authenticated'}, status=401)
        if user.role.authorisation != 'superadmin':
            return Response({'message': 'User is not an administrator'}, status=403)
        
        try:
            notification = Notification.objects.get(id=pk)
        except Notification.DoesNotExist:
            return Response({'message': 'Notification not found'}, status=404)
        
        notification.status = True
        notification.answered_by = user
        notification.save()
        
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=200)
    
    def list_escalation_notifications(self, request):
        user = request.user
        if not user.is_authenticated or not user.role or user.role.authorisation != 'superadmin':
            return Response({'message': 'User not authenticated'}, status=401)
        if user.role.authorisation != 'superadmin':
            return Response({'message': 'User is not an administrator'}, status=403)
        
        notifications = Notification.objects.filter(gravity='escalation')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=200)
    
    def list_system_notifications(self, request):
        user = request.user
        if not user.is_authenticated or not user.role or user.role.authorisation != 'superadmin':
            return Response({'message': 'User not authenticated'}, status=401)
        if user.role.authorisation != 'superadmin':
            return Response({'message': 'User is not an administrator'}, status=403)
        
        notifications = Notification.objects.filter(gravity='system')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=200)
    
class NotificationProblemeTypeListViewset(viewsets.ViewSet):

    def list_probleme_by_type(self, problem_type):
        user = self.request.user
        if not user.is_authenticated or not user.role or user.role.authorisation != 'superadmin':
            return Response({'message': 'User not authenticated'}, status=401)
        if user.role.authorisation != 'superadmin':
            return Response({'message': 'User is not an administrator'}, status=403)
        
        notifications = Notification.objects.filter(problem_type=problem_type)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=200)
