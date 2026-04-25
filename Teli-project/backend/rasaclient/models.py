from django.db import models

class RasaClient(models.Model):
    Channel = models.CharField(max_length=255)
    ChannelUserId = models.CharField(max_length=50)
    ConversationId = models.ForeignKey('conversations.Conversation', on_delete=models.CASCADE, related_name='rasa_clients')
    
    def __str__(self):
        return f"nom de la chaine {self.Channel} - id de l'utilisateur {self.ChannelUserId}"
    
    
