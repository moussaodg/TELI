from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from conversations.models import Conversation
from accounts.models import Administrator


class DashboardStatisticsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        total = Conversation.objects.count()
        weekly = Conversation.objects.filter(start_date__gte='2024-01-01').count()
        satisfied = Conversation.objects.filter(is_satisfied=True).count()  # Example filter for weekly stats
        closed = Conversation.objects.filter(status='CLOSED').count()
        active = Conversation.objects.exclude(status='CLOSED').count()

        return Response({
            'total_conversations': total,
            'closed_conversations': closed,
            'active_conversations': active,
            'satisfied_conversations': satisfied,
        })

    def active_administrators(self, request):
        user = request.user
        if not user.is_authenticated or user.role.authorisation != 'superadmin':
            return Response({'message': 'User not authenticated or permission denied'}, status=401)
        active_admins = Administrator.objects.filter(is_active=True).count()
        return Response({'active_administrators': active_admins})