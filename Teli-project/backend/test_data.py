#!/usr/bin/env python
"""
Script pour initialiser des données de test pour les endpoints conversations et rasaclient
Exécutez avec: python manage.py shell < test_data.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import Administrator, role
from conversations.models import Conversation, Actor, Message
from rasaclient.models import RasaClient
from django.utils import timezone

print("=" * 60)
print("CRÉATION DES DONNÉES DE TEST")
print("=" * 60)

# 1. Créer un rôle superadmin
print("\n1. Création du rôle superadmin...")
superadmin_role, created = role.objects.get_or_create(
    name='superadmin',
    defaults={'authorisation': 'superadmin'}
)
print(f"   ✓ Rôle créé: {superadmin_role}")

# 2. Créer un administrateur
print("\n2. Création d'un administrateur...")
admin, created = Administrator.objects.get_or_create(
    username='admin_test',
    defaults={
        'email': 'admin@test.com',
        'first_name': 'Admin',
        'last_name': 'Test',
        'tel': '221770000000',
        'address': '123 Rue Test, Dakar',
        'role': superadmin_role,
        'is_staff': True,
    }
)
if created:
    admin.set_password('admin123456')
    admin.save()
    print(f"   ✓ Admin créé: {admin.username}")
else:
    print(f"   ℹ Admin existant: {admin.username}")

# 3. Créer des conversations
print("\n3. Création de conversations...")
conversations = []
for i in range(3):
    conv, created = Conversation.objects.get_or_create(
        id=1000 + i,
        defaults={
            'context': {'client_name': f'Client_{i+1}', 'product': 'Offer_A'},
            'is_satisfied': i == 2  # Dernière conversation = satisfied
        }
    )
    conversations.append(conv)
    status = "créée" if created else "existante"
    print(f"   ✓ Conversation {conv.id} ({status})")

# 4. Créer des RasaClients
print("\n4. Création de RasaClients...")
rasa_clients = []
for i, conv in enumerate(conversations):
    rasa_client, created = RasaClient.objects.get_or_create(
        Channel=f'channel_{i+1}',
        ChannelUserId=f'user_{i+1}@channel_{i+1}',
        defaults={'ConversationId': conv}
    )
    rasa_clients.append(rasa_client)
    status = "créé" if created else "existant"
    print(f"   ✓ RasaClient (Channel: {rasa_client.Channel}, User: {rasa_client.ChannelUserId}) - {status}")

# 5. Créer des Actors
print("\n5. Création d'Actors...")

# Actor Bot
bot_actor, created = Actor.objects.get_or_create(
    actor_type='bot',
    defaults={'rasa_client': None, 'administrator': None}
)
print(f"   ✓ Actor Bot créé" if created else f"   ℹ Actor Bot existant")

# Actor Admin
admin_actor, created = Actor.objects.get_or_create(
    actor_type='admin',
    defaults={'administrator': admin, 'rasa_client': None}
)
print(f"   ✓ Actor Admin créé" if created else f"   ℹ Actor Admin existant")

# Actor Clients
client_actors = []
for i, rasa_client in enumerate(rasa_clients):
    client_actor, created = Actor.objects.get_or_create(
        actor_type='client',
        defaults={'rasa_client': rasa_client, 'administrator': None}
    )
    client_actors.append(client_actor)
    print(f"   ✓ Actor Client {i+1} créé" if created else f"   ℹ Actor Client {i+1} existant")

# 6. Créer des Messages
print("\n6. Création de Messages...")
message_count = 0

for i, conv in enumerate(conversations):
    # Message du client
    msg1, created = Message.objects.get_or_create(
        conversation=conv,
        sender=client_actors[i],
        content=f"Bonjour, je veux acheter une offre",
        message_type='text',
        status='delivered'
    )
    if created:
        message_count += 1
    
    # Message du bot
    msg2, created = Message.objects.get_or_create(
        conversation=conv,
        sender=bot_actor,
        content=f"Bienvenue! Je peux vous aider avec nos offres spéciales.",
        message_type='text',
        status='delivered'
    )
    if created:
        message_count += 1
    
    # Message d'escalade si pas satisfait
    if not conv.is_satisfied:
        msg3, created = Message.objects.get_or_create(
            conversation=conv,
            sender=bot_actor,
            content="Permettez-moi de vous mettre en contact avec un administrateur.",
            message_type='escalation',
            status='sent'
        )
        if created:
            message_count += 1
        
        # Réponse admin
        msg4, created = Message.objects.get_or_create(
            conversation=conv,
            sender=admin_actor,
            content="Bonjour, comment puis-je vous aider?",
            message_type='text',
            status='sent'
        )
        if created:
            message_count += 1

print(f"   ✓ {message_count} messages créés")

# 7. Résumé
print("\n" + "=" * 60)
print("RÉSUMÉ DES DONNÉES DE TEST")
print("=" * 60)
print(f"\n✓ Conversations: {Conversation.objects.count()}")
print(f"✓ RasaClients: {RasaClient.objects.count()}")
print(f"✓ Actors: {Actor.objects.count()}")
print(f"✓ Messages: {Message.objects.count()}")
print(f"✓ Administrateurs: {Administrator.objects.count()}")

print("\n" + "=" * 60)
print("DONNÉES DE TEST POUR POSTMAN")
print("=" * 60)
print(f"""
1. ENDPOINT: POST /rasaclient/continue_or_start_conversation/
   BODY (JSON):
   {{
       "channel": "channel_1",
       "channel_user_id": "user_1@channel_1"
   }}

2. ENDPOINT: GET /conversations/view_conversation/<ChannelUserId>/
   Exemples:
   - /conversations/view_conversation/user_1@channel_1/
   - /conversations/view_conversation/user_2@channel_2/
   - /conversations/view_conversation/user_3@channel_3/

3. ENDPOINT: GET /conversations/list_conversations/
   (Liste toutes les conversations)

4. ENDPOINT: GET /conversations/view_single_message/<message_id>/
   Exemple: /conversations/view_single_message/1/

Token pour tests (si authentification requise):
- Utilisateur: {admin.username}
- Mot de passe: admin123456
(Récupérez le token via /administrators/login/)
""")
print("=" * 60 + "\n")
