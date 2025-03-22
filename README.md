# API для Сокращения URL

Современный сервис для сокращения URL-адресов, построенный на FastAPI, с функциями аутентификации, аналитики и предпросмотра ссылок.
Сервис развернут на платформе Render - https://url-shortener-e3rb.onrender.com/docs

## Возможности

- Сокращение URL с пользовательскими алиасами
- Аутентификация пользователей с помощью JWT токенов
- Аналитика ссылок (количество переходов, последний доступ)
- Генерация предпросмотра ссылок
- Срок действия ссылок
- Проверка валидности и безопасности URL
- Поддержка CORS

## Технологический стек

- FastAPI
- SQLAlchemy
- SQLite (легко переключается на PostgreSQL)
- Pydantic
- JWT Аутентификация
- BeautifulSoup4 для предпросмотра ссылок

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите приложение:
```bash
uvicorn app.main:app --reload
```

API будет доступен по адресу `http://localhost:8000`

## Документация API

После запуска сервера вы можете получить доступ к:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Ручки API

### Аутентификация
- `POST /auth/register` - Регистрация нового пользователя
- `POST /auth/login` - Вход и получение токена доступа
- `POST /auth/login/json` - Вход с данными JSON

### Ссылки
- `POST /links/shorten` - Создание новой короткой ссылки
- `GET /{short_code}` - Перенаправление на оригинальный URL
- `DELETE /links/{short_code}` - Удаление ссылки
- `PUT /links/{short_code}` - Обновление ссылки
- `GET /links/{short_code}/stats` - Получение статистики ссылки
- `GET /links/search` - Поиск ссылки по URL

## Примеры запросов

### Регистрация пользователя
```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
           "email": "user@example.com",
           "password": "strongpassword123"
         }'
```

### Вход в систему
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user@example.com&password=strongpassword123"
```

### Создание короткой ссылки
```bash
curl -X POST "http://localhost:8000/links/shorten" \
     -H "Authorization: Bearer your_access_token" \
     -H "Content-Type: application/json" \
     -d '{
           "url": "https://example.com/very-long-url",
           "custom_alias": "my-short-link",
           "expires_at": "2024-12-31T23:59:59"
         }'
```

### Получение статистики ссылки
```bash
curl -X GET "http://localhost:8000/links/my-short-link/stats" \
     -H "Authorization: Bearer your_access_token"
```

## Структура базы данных

### Таблица Users
- `id`: INTEGER (Primary Key) - Уникальный идентификатор пользователя
- `email`: VARCHAR - Email пользователя (уникальный)
- `hashed_password`: VARCHAR - Хешированный пароль
- `created_at`: TIMESTAMP - Дата создания аккаунта

### Таблица Links
- `id`: INTEGER (Primary Key) - Уникальный идентификатор ссылки
- `user_id`: INTEGER (Foreign Key) - ID пользователя-владельца
- `original_url`: VARCHAR - Оригинальный URL
- `short_code`: VARCHAR - Короткий код ссылки (уникальный)
- `custom_alias`: VARCHAR - Пользовательский алиас (опциональный)
- `created_at`: TIMESTAMP - Дата создания ссылки
- `expires_at`: TIMESTAMP - Дата истечения срока действия
- `click_count`: INTEGER - Количество переходов
- `last_accessed`: TIMESTAMP - Время последнего перехода

### Таблица LinkPreviews
- `id`: INTEGER (Primary Key) - Уникальный идентификатор предпросмотра
- `link_id`: INTEGER (Foreign Key) - ID связанной ссылки
- `title`: VARCHAR - Заголовок страницы
- `description`: TEXT - Описание страницы
- `image_url`: VARCHAR - URL изображения
- `created_at`: TIMESTAMP - Дата создания предпросмотра

## Переменные окружения

Создайте файл `.env` в корневой директории со следующими переменными:
```
SECRET_KEY=ваш-секретный-ключ
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Развертывание

Это приложение настроено для развертывания на Render.io. Файл `render.yaml` содержит необходимую конфигурацию.

## Лицензия

MIT License 
