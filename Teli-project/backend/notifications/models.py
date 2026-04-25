from math import tau
from django.db import models
from conversations.models import Conversation, Message
from accounts.models import Administrator, role
from rasaclient.models import RasaClient

class Notification(models.Model):
    CHOICES = (
        ('system', 'System'),
        ('escalation', 'Escalation'),
    )

    PROBLEMS = (
        ('Configuration_reseau', 'Configuration réseau'),
        ('Probleme_technique', 'Problème technique'),
        ('Telecel_Money', 'Problème avec Telecel Money'),
        ('MusiCool', 'Problème avec MusiCool'),
        ('Credit', 'Problème de crédit'),
        ('Autre', 'Autre'),
    )  

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )
    gravity = models.CharField(max_length=20, choices=CHOICES)
    status = models.BooleanField(default=False)  # False = non lue, True = lue
    created_at = models.DateTimeField(auto_now_add=True)
    answered_by = models.ForeignKey(Administrator, on_delete=models.SET_NULL, null=True, blank=True, related_name='answered_notifications')
    problem_type = models.CharField(max_length=255, choices=PROBLEMS, default='Autre')
    context = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Notification for Conversation {self.conversation.id} - Gravity: {self.gravity}"