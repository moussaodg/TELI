# Copilot instructions for TELI backend

## Project structure
- `Teli-project/backend/` is the Django backend.
- App boundaries are explicit: `accounts`, `offers`, `conversations`, `rasaclient`, `notifications`, `webhook`, `stats`.
- Each app typically contains: `models.py`, `serializers.py`, `views.py`, `urls.py`, and optionally `services.py` for business logic.

## Architecture patterns
- Keep business logic in `services.py` when it spans multiple database operations or external calls.
  - Example: `conversations/services.py` and `rasaclient/services.py`.
- Use DRF `ViewSet` / custom actions in `views.py`, but do not put heavy workflow logic there.
- App routes are defined manually in each app `urls.py` and included from `config/urls.py`.
  - Example: `rasaclient/urls.py` contains `send_message/` and management endpoints.
- The default backend permission in `config/settings.py` is `AllowAny`, so enforce auth per view with `permission_classes`.
  - Example: `ConverstationViewSet.permission_classes = [IsAuthenticated]`.

## Key models and domain rules
- `accounts.Administrator` is the custom user model (`AUTH_USER_MODEL`).
- `conversations.Conversation` uses a `status` choice field (`BOT_ACTIVE`, `ESCALATED`, `HUMAN_ACTIVE`, `CLOSED`) and keeps `is_satisfied` for historical state.
- `notifications.Notification` is now linked primarily to `conversation`, with an optional `message` reference and a JSON `context` field.
- `offers.Offer` includes `is_active` and a `sync_rasa()` hook on save to keep chatbot state updated.
- Avoid cross-app route leakage: Rasa client APIs belong in `rasaclient/`, not in `offers/`.

## External integration points
- `rasaclient` is the main connector to the Rasa/chatbot service.
- `webhook/views.py` handles external webhook verification and incoming messages.
- `stats` is a backend metrics app rather than a dashboard UI app; it exposes aggregations such as total conversations and satisfaction counts.
- Do not name an app `statistics` because it shadows Python’s standard `statistics` module; the app is called `stats`.

## Developer workflow
- Use the backend virtualenv in `Teli-project/backend/env/`.
- Common validation commands:
  - `cd Teli-project/backend && ./env/bin/python -m py_compile <files>`
  - `cd Teli-project/backend && ./env/bin/python manage.py check`
  - `cd Teli-project/backend && ./env/bin/python manage.py makemigrations <app>`
  - `cd Teli-project/backend && ./env/bin/python manage.py migrate --plan`
- If you add a new app, register it in `config/settings.py` and include its `urls.py` in `config/urls.py`.

## Project-specific conventions
- Prefer DRF permission classes over manual `request.user.is_authenticated` checks.
- Use `services.py` for:
  - get-or-create flows
  - external HTTP calls
  - multi-model updates
- Keep view methods focused on request parsing, service invocation, and response formatting.
- Use `response.status` and explicit error messages for API consistency.

## Notes for Copilot
- When editing backend endpoints, always check the app’s `urls.py` for the exact action-to-path mapping.
- Existing code uses a custom authentication helper in `config/authentication.py` to normalize malformed `Authorization` headers.
- The backend is SQLite-based and the app models must be migrated through Django migrations.
- Favor existing app conventions and service extraction rather than introducing new cross-cutting utilities unless strictly needed.
