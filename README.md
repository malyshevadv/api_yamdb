# API для базы данных произведений (api_yamdb)

# Описание
 Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. Произведению может быть присвоен жанр (Genre) из списка предустановленных. Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв. К отзывам пользователи могут оставлять комментарии. 

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/malyshevadv/api_yamdb
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```


## Заполнение базы данными

Для заполнения используется management-команда:
```bash
./manage.py loaddata <file_name.csv> [<file_name2.csv> ...]
```

### Примеры запросов:

Регистрация нового пользователя:
```
POST http://127.0.0.1:8000/api/v1/auth/signup/
Content-Type: application/json

{
    "email": "string",
    "username": "string"
}
```

Запрос токена доступа:
```
POST http://127.0.0.1:8000/api/v1/auth/token/
Content-Type: application/json

{
    "username": "string",
    "confirmation_code": "string"
}
```


Получение списка всех категорий:
```
GET http://127.0.0.1:8000/api/v1/categories/
```

Добавление новой категории:
```
POST http://127.0.0.1:8000/api/v1/categories/
Content-Type: application/json
Authorization: Bearer <token>

{
    "name": "string",
    "slug": "string"
}
```

Удаление категории:
```
DELETE http://127.0.0.1:8000/api/v1/categories/{slug}/
```

Получение списка всех жанров: 
```
GET http://127.0.0.1:8000/api/v1/genres/
```

Добавление жанра:
```
POST http://127.0.0.1:8000/api/v1/genres/
Content-Type: application/json
Authorization: Bearer <token>

{
    "name": "string",
    "slug": "string"
}
```

Удаление жанра
```
DELETE http://127.0.0.1:8000/api/v1/genres/{slug}/
```

Получение списка всех произведений: 
```
GET http://127.0.0.1:8000/api/v1/titles/
```

Добавление произведения:
```
POST http://127.0.0.1:8000/api/v1/titles/
Content-Type: application/json
Authorization: Bearer <token>

{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": 

    [
        "string"
    ],
    "category": "string"
}
```

Получение информации о произведении: 
```
GET http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

Частичное обновление информации о произведении:
```
PATCH http://127.0.0.1:8000/api/v1/titles/{titles_id}/
Content-Type: application/json
Authorization: Bearer <token>

{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": 

    [
        "string"
    ],
    "category": "string"
}
```

Удаление произведения:
```
DELETE http://127.0.0.1:8000/api/v1/titles/{titles_id}/
Content-Type: application/json
Authorization: Bearer <token>
```

Получение списка всех отзывов: 
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

Добавление нового отзыва:
```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
Content-Type: application/json
Authorization: Bearer <token>

{
    "text": "string",
    "score": 1
}
```

Полуение отзыва по id: 
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```

Частичное обновление отзыва по id:
```
PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
Content-Type: application/json
Authorization: Bearer <token>

{
    "text": "string",
    "score": 1
}
```

Удаление отзыва по id:
```
DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
Content-Type: application/json
Authorization: Bearer <token>
```

Получение списка всех комментариев к отзыву: 
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

Добавление комментария к отзыву:
```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
Content-Type: application/json
Authorization: Bearer <token>

{
    "text": "string"
}
```

Получение комментария к отзыву: 
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

Частичное обновление комментария к отзыву:
```
PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
Content-Type: application/json
Authorization: Bearer <token>

{
    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2019-08-24T14:15:22Z"
}
```

Удаление комментария к отзыву:
```
DELETE http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
Content-Type: application/json
Authorization: Bearer <token>
```

Получение списка всех пользователей: 
```
GET http://127.0.0.1:8000/api/v1/users/
```

Добавление пользователя:
```
POST http://127.0.0.1:8000/api/v1/users/
Content-Type: application/json
Authorization: Bearer <token>

{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```

Получение пользователя по username: 
```
GET http://127.0.0.1:8000/api/v1/users/{username}/
```
Внесение изменение данных пользователя по username:
```
PATCH http://127.0.0.1:8000/api/v1/users/{username}/
Content-Type: application/json
Authorization: Bearer <token>

{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```

Удаление пользователя по username:
```
DELETE http://127.0.0.1:8000/api/v1/users/{username}/
Content-Type: application/json
Authorization: Bearer <token>
```

Получение данных своей учетной записи: 
```
GET http://127.0.0.1:8000/api/v1/users/me/
```

Внесение изменение данных своей учетной записи:
```
PATCH http://127.0.0.1:8000/api/v1/users/me/
Content-Type: application/json
Authorization: Bearer <token>

{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string"
}
```

### Технологии
- Python 3.7
- Django 2.2.19

### Авторы
Руководитель группы: Дарья Малышева

Антон Горошко

Михаил Лаврухин
