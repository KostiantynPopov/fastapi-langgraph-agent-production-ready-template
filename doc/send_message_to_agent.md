# Как отправлять запрос агенту от имени бота (Bitrix24 → flaprt)

## 1. Получи креды из файлов

- **user_token** и **session_token** для нужного чата бери из файлов:
  - `bitrix-bot/data/chat_user_token_map.json`
  - `bitrix-bot/data/chat_session_token_map.json`
- Для теста можно использовать, например, chat_id: `chat194791`.

## 2. Сформируй curl-запрос

```bash
curl -X POST "http://localhost:8000/api/v1/chatbot/chat" \
  -H "Authorization: Bearer <session_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "который час в Хургаде?"
      }
    ],
    "entity_id": "telegrambot|19|442236029|18"
  }'
```

- **<session_token>** — подставь значение из `chat_session_token_map.json` для нужного chat_id.
- **entity_id** — подставь актуальный идентификатор чата (можно взять из логов или из Bitrix24, пример: `telegrambot|19|442236029|18`).

## 3. Проверка результата

- В ответе должен быть JSON с массивом сообщений, последнее из которых — ответ ассистента с актуальным временем для указанного города.
- Пример успешного ответа:
  ```json
  {
    "messages": [
      ...,
      {
        "role": "assistant",
        "content": "У Хургаді зараз 11:25 16 липня 2025 року. Якщо вам потрібна додаткова інформація, будь ласка, запитуйте!"
      }
    ]
  }
  ```

## 4. Примечания

- Если токены устарели — авторизуйся заново через Bitrix24 или перезапусти цепочку регистрации/логина.
- Для других чатов используй соответствующие токены и entity_id.
- Все креды и идентификаторы можно брать напрямую из json-файлов в папке `bitrix-bot/data/`.

---

**Пример для chat194791:**

```bash
curl -X POST "http://localhost:8000/api/v1/chatbot/chat" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1YmMzYTk2ZS0xYWU3LTQxYmUtOTY1ZS0yNjdjZTViNjA2NmYiLCJleHAiOjE3NTM5MjAxNjUsImlhdCI6MTc1MTMyODE2NSwianRpIjoiNWJjM2E5NmUtMWFlNy00MWJlLTk2NWUtMjY3Y2U1YjYwNjZmLTE3NTEzMjgxNjUuNjkyODExIn0.Zwdb1n5XSjmvF4snZ2vylkSJ47sc7r01KtTqyQa2Ddg" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "который час в Хургаде?"
      }
    ],
    "entity_id": "telegrambot|19|442236029|18"
  }'
```

---

**Файл готов для скачивания и использования.** 