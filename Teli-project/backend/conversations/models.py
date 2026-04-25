from django.db import models
from accounts.models import Administrator, role


# =========================
# CONVERSATION
# =========================
class Conversation(models.Model):
    context = models.JSONField(default=dict, blank=True)  # structuré
    STATUS_CHOICES = (
        ('BOT_ACTIVE', 'Bot active'),
        ('ESCALATED', 'Escalated'),
        ('HUMAN_ACTIVE', 'Human active'),
        ('CLOSED', 'Closed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='BOT_ACTIVE')
    administrator = models.ForeignKey(
        Administrator,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_conversations'
    )
    is_satisfied = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)  # correction

    def __str__(self):
        return f"Conversation {self.id}"


# =========================
# ACTOR (expéditeur générique)
# =========================
class Actor(models.Model):
    ACTOR_TYPES = (
        ('client', 'Client'),
        ('admin', 'Admin'),
        ('bot', 'Bot'),
    )

    name = models.CharField(max_length=100, blank=True, null=True)

    actor_type = models.CharField(max_length=10, choices=ACTOR_TYPES)
    
    # Relations optionnelles (UNE SEULE doit être remplie selon actor_type)
    rasa_client = models.OneToOneField(
        'rasaclient.RasaClient', null=True, blank=True, on_delete=models.CASCADE
    )
    administrator = models.OneToOneField(
        Administrator, null=True, blank=True, on_delete=models.CASCADE
    )

    def clean(self):
        """
        Pour garantir la cohérence entre actor_type et relations
        """
        if self.actor_type == 'client' and not self.rasa_client:
            raise ValueError("Un client doit être lié à un RasaClient")

        if self.actor_type == 'admin' and not self.administrator:
            raise ValueError("Un admin doit être lié à un Administrator")

        if self.actor_type == 'bot':
            if self.rasa_client or self.administrator:
                raise ValueError("Un bot ne doit avoir aucune relation")

    def __str__(self):
        return f"{self.name} ({self.actor_type})"


# =========================
# MESSAGE
# =========================
class Message(models.Model):
    MESSAGE_TYPES = (
        ('text', 'Text'),
        ('system', 'System'),
        ('escalation', 'Escalation'),
    )

    STATUS_CHOICES = (
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    message_type = models.CharField(
        max_length=20,
        choices=MESSAGE_TYPES,
        default='text'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='sent'
    )

    reply_to = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='responses'
    )

    def __str__(self):
        return f"{self.sender} → {self.content[:30]}"
