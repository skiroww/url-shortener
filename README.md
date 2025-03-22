# API для Сокращения URL

Современный сервис для сокращения URL-адресов, построенный на FastAPI, с функциями аутентификации, аналитики и предпросмотра ссылок.

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
