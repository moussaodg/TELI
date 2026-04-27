# Rasa Chatbot

Ce dossier contient la configuration de base pour entraîner un modèle Rasa.

## Fichiers principaux

- `config.yml` : pipeline NLU et politiques Rasa
- `domain.yml` : intentions, réponses et configuration de session
- `data/nlu.yml` : exemples d'entraînement pour l'intention
- `data/rules.yml` : règles de dialogue pour les intentions
- `credentials.yml` : canaux supportés par Rasa
- `endpoints.yml` : point d'accès pour les actions personnalisées

## Entraînement

Depuis `Teli-project/chatbot` :

```bash
rasa train
```

## Exécution

Depuis `Teli-project/chatbot` :

```bash
rasa run --enable-api --cors "*"
```

## Intégration avec le backend

Ton backend peut envoyer un POST sur :

```text
http://localhost:5005/webhooks/rest/webhook
```

Avec le payload :

```json
{
  "sender": "user_id",
  "message": "Bonjour"
}
```
