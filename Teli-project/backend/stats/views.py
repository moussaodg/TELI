from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from conversations.models import Conversation


class DashboardStatisticsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        total = Conversation.objects.count()
        closed = Conversation.objects.filter(status='CLOSED').count()
        active = Conversation.objects.exclude(status='CLOSED').count()
        satisfied = Conversation.objects.filter(is_satisfied=True).count()
        return Response({
            'total_conversations': total,
            'closed_conversations': closed,
            'active_conversations': active,
            'satisfied_conversations': satisfied,
        })
