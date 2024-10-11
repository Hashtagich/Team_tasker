# Система управления задачами команд в рамках стажировки в компании Promo-IT.

<details>
<summary>

## Описание сервиса
</summary>
Backend приложение, которое позволяет командам организовать и управлять своими задачами, временем.

</details>

---
<details>
<summary>

## Описание функционала
</summary>

текст

</details>

---
<details>
<summary>

## Запуск проекта
</summary>

### 1. Клонирование репозиторий
```bash
git clone https://github.com/Hashtagich/Team_tasker.git
```

### 2. Установка переменных окружения
***В корене проекта заполняем файл template.db.env и переименовываем его в db.env или просто создаём файл db.env и заполняем его***
```bash
POSTGRES_DB=Например, db
POSTGRES_USER=Например, db
POSTGRES_PASSWORD=Например, db
```

***В папке backend заполняем файл template.env и переименовываем его в .env или просто создаём файл .env и заполняем его***
 ```bash
 SECRET_KEY='Ваш секретный ключ проекта'
 DEBUG=Булевое значение True или False
 ALLOWED_HOSTS='Разрешенные хосты'
 LANGUAGE_CODE='Язык, например, ru'
 TIME_ZONE='Временная зона, например, UTC'

 DB_NAME='Имя Базы данных (БД), например, db'
 DB_LOGIN='Логин БД, например, db'
 DB_PASS='Пароль БД, например, db'
 DB_HOST='Хост БД, например, db'
 DB_PORT='Порт БД, например, 5432'
 
 EMAIL_BACKEND='Сервис для почты, например, django.core.mail.backends.smtp.EmailBackend'
 EMAIL_HOST='Хост почты, например для gmail smtp.gmail.com или smtp.mail.ru для mail'
 EMAIL_PORT=Порт почты, например, 587
 DEFAULT_FROM_EMAIL='Почта с которой будет отправлять письма youremail@gmail.com если выбрали smtp.gmail.com'
 EMAIL_USE_TLS=Булевое значение True или False причём EMAIL_USE_TLS не равен EMAIL_USE_SSL
 EMAIL_USE_SSL=Булевое значение True или False причём EMAIL_USE_TLS не равен EMAIL_USE_SSL
 EMAIL_HOST_PASSWORD='Пароль для внешнего приложения для доступа к почте, подробнее тут https://help.mail.ru/mail/security/protection/external/'
 NOTIFICATION_EMAIL='Перечень почт куда будут отправлять письма, пишите через пробел, можно указать одну'

 ```

### 3. Сборка и запуск контейнеров

```bash

docker-compose up --build -d

```


### 4. Инициализация БД (Создание ролей для пользователей)

```bash

docker-compose exec web python manage.py initialize_db

```


### 5. Создание суперпользователя.

```bash

docker-compose exec web python manage.py createsuperuser

```

</details>

___

### Urls и API

***Административная панель***

<code>/admin/</code>

***Страница с документацией по API***

<code>/api/v1/swagger/</code>

***API Регистрация и логирование***
<details>
<summary><code>POST/api/v1/register/</code></summary>

*Регистрация пользователя. Необходимо ввести фамилию, имя, отчество, роль, почту и пароль. Пароль должен быть не менее 8 символов и содержать минимум одну строчную латинскую букву и цифры.*

```
{
  "first_name": "string",
  "last_name": "string",
  "middle_name": "string",
  "email": "user@example.com",
  "password": "string"
}
```

</details>
<details>
<summary><code>POST/api/v1/auth/jwt/create/</code></summary>

*Логирование пользователя и генерация токена. Необходимо ввести почту и пароль пользователя.*

```
{
  "email": "string",
  "password": "string"
}
```

</details>


