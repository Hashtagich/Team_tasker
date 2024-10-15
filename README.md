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

1) Все пользователи регистрируются в роли Пользователь;
2) Администратором может быть только superuser;
3) Администраторы могу:
* Блокировать и разблокировать пользователя;
* Создавать, просматривать, редактировать и удалять группы/команды;
* Создавать, просматривать, редактировать и удалять задача.
4) Пользователи могут:
* Создавать, просматривать задачи.
5) Модераторы групп/команд могут:
* Создавать, просматривать, редактировать группы/команды;
* Создавать, просматривать, редактировать и удалять задача.
6) Статистику могут просматривать все авторизованные пользователи;
7) Можно просматривать: 
* Статус и кол-во всех задач;
* Свою статистику, те задачи где отмечен как исполнитель.
* Статистику подчинённых/членов команды, если находимся на позиции руководителя в группе/команде, т.е. получаем статус и кол-во всех задач наших членов команды отмеченных как исполнитель, иначе получаем пустой список.
8) Все права распределяются в зависимости от занятой позиции в команде.

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

***API для Администратора***
<details>
<summary><code>GET/api/v1/users/</code></summary>

*Получение списка всех пользователей*
```
[
  {
    "id": 0,
    "first_name": "string",
    "last_name": "string",
    "middle_name": "string",
    "role": "",
    "phone": "string",
    "email": "user@example.com",
    "is_staff": true,
    "is_active": true,
    "is_blocked": true
  }
]
```
</details>
<details>
<summary><code>GET/api/v1/users/{id}/</code></summary>

*Получение информации о пользователе через его id*

```
{
  "id": 0,
  "first_name": "string",
  "last_name": "string",
  "middle_name": "string",
  "role": "",
  "phone": "string",
  "email": "user@example.com",
  "is_staff": true,
  "is_active": true,
  "is_blocked": true
}
```

</details>
<details>
<summary><code>PATCH/api/v1/users/{id}/</code></summary>

*Редактирования конкретного пользователя по ID*

```
{
  "first_name": "string",
  "last_name": "string",
  "middle_name": "string",
  "role": 0,
  "is_staff": true,
  "is_active": true,
  "is_blocked": true
}
```

</details>
<details>
<summary><code>PATCH/api/v1/users/{id}/unblock_user/</code></summary>

*Разблокировка пользователя*

</details>
<details>
<summary><code>PATCH/api/v1/users/{id}/block_user/</code></summary>

*Блокировка пользователя*

</details>
<details>
<summary><code>POST/api/v1/groups/</code></summary>

*Создание группы/команды*

```
{
  "name": "string",
  "leader": 0,
  "moderators": [
    0
  ],
  "specialists": [
    0
  ]
}
```

</details>
<details>
<summary><code>DELETE/api/v1/groups/{id}/</code></summary>

*Удаление группы/команды*

</details>

***API для всех Пользователей***

<details>
<summary><code>GET/api/v1/groups/</code></summary>

*Получение всех групп/команд*

```
[
  {
    "id": 0,
    "name": "string",
    "leader": {
      "id": 0,
      "first_name": "string",
      "last_name": "string",
      "middle_name": "string"
    },
    "moderators": [
      {
        "id": 0,
        "first_name": "string",
        "last_name": "string",
        "middle_name": "string"
      }
    ],
    "specialists": [
      {
        "id": 0,
        "first_name": "string",
        "last_name": "string",
        "middle_name": "string"
      }
    ],
    "datetime_update": "2024-10-14T21:33:27.079Z",
    "datetime_create": "2024-10-14T21:33:27.079Z"
  }
]
```

</details>
<details>
<summary><code>GET/api/v1/groups/{id}/</code></summary>

*Получение конкретной группы/команды по ID*

```
{
  "id": 0,
  "name": "string",
  "leader": {
    "id": 0,
    "first_name": "string",
    "last_name": "string",
    "middle_name": "string"
  },
  "moderators": [
    {
      "id": 0,
      "first_name": "string",
      "last_name": "string",
      "middle_name": "string"
    }
  ],
  "specialists": [
    {
      "id": 0,
      "first_name": "string",
      "last_name": "string",
      "middle_name": "string"
    }
  ],
  "datetime_update": "2024-10-14T21:34:04.886Z",
  "datetime_create": "2024-10-14T21:34:04.886Z"
}
```

</details>
<details>
<summary><code>GET/api/v1/tasks/</code></summary>

*Получение всех задач*

```
[
  {
    "name": "string",
    "description": "string",
    "status": "new",
    "author": {
      "id": 0,
      "first_name": "string",
      "last_name": "string",
      "middle_name": "string"
    },
    "implementer": {
      "id": 0,
      "first_name": "string",
      "last_name": "string",
      "middle_name": "string"
    },
    "datetime_start": "2024-10-14T21:48:57.238Z",
    "datetime_finish_plan": "2024-10-14T21:48:57.238Z",
    "datetime_finish_fact": "2024-10-14T21:48:57.238Z",
    "datetime_create": "2024-10-14T21:48:57.238Z"
  }
]
```

</details>
<details>
<summary><code>GET/api/v1/tasks/{id}/</code></summary>

*Получение конкретной задачи по ID*

```
{
  "name": "string",
  "description": "string",
  "status": "new",
  "author": {
    "id": 0,
    "first_name": "string",
    "last_name": "string",
    "middle_name": "string"
  },
  "implementer": {
    "id": 0,
    "first_name": "string",
    "last_name": "string",
    "middle_name": "string"
  },
  "datetime_start": "2024-10-14T21:49:49.575Z",
  "datetime_finish_plan": "2024-10-14T21:49:49.575Z",
  "datetime_finish_fact": "2024-10-14T21:49:49.575Z",
  "datetime_create": "2024-10-14T21:49:49.575Z"
}
```

</details>
<details>
<summary><code>POST/api/v1/tasks/</code></summary>

*Создание задачи. Автором становиться текущий пользователь. Название и описание являются обязательными к заполнению.*

```
{
  "name": "string",
  "description": "string",
  "status": "new",
  "author": {
    "id": 0,
    "first_name": "string",
    "last_name": "string",
    "middle_name": "string"
  },
  "implementer": {
    "id": 0,
    "first_name": "string",
    "last_name": "string",
    "middle_name": "string"
  },
  "datetime_start": "2024-10-14T21:49:49.575Z",
  "datetime_finish_plan": "2024-10-14T21:49:49.575Z",
  "datetime_finish_fact": "2024-10-14T21:49:49.575Z",
  "datetime_create": "2024-10-14T21:49:49.575Z"
}
```

</details>

***API для Модератора группы/команды и Администратора***

<details>
<summary><code>PATCH/api/v1/groups/{id}/</code></summary>

*Частичное редактирование конкретной группы/команды по ID*

```
{
  "name": "string",
  "leader": 0,
  "moderators": [
    0
  ],
  "specialists": [
    0
  ]
}
```

</details>
<details>
<summary><code>PUT/api/v1/groups/{id}/</code></summary>

*Полное редактирование конкретной группы/команды по ID*

```
{
  "name": "string",
  "leader": 0,
  "moderators": [
    0
  ],
  "specialists": [
    0
  ]
}
```

</details>
<details>
<summary><code>PUT/api/v1/tasks/{id}/</code></summary>

*Полное редактирование конкретной задачи по ID. Может выполнить также автор задачи.*

```
{
  "name": "string",
  "description": "string",
  "status": "new",
  "implementer": 0,
  "datetime_start": "2024-10-14T21:54:32.618Z",
  "datetime_finish_plan": "2024-10-14T21:54:32.618Z",
  "datetime_finish_fact": "2024-10-14T21:54:32.618Z"
}
```

</details>
<details>
<summary><code>PATCH/api/v1/tasks/{id}/</code></summary>

*Частичное редактирование конкретной задачи по ID. Может выполнить также автор задачи.*

```
{
  "name": "string",
  "description": "string",
  "status": "new",
  "implementer": 0,
  "datetime_start": "2024-10-14T21:54:32.618Z",
  "datetime_finish_plan": "2024-10-14T21:54:32.618Z",
  "datetime_finish_fact": "2024-10-14T21:54:32.618Z"
}
```

</details>
<details>
<summary><code>DELETE/api/v1/tasks/{id}/</code></summary>

*Удаление конкретной задачи по ID. Может выполнить также автор задачи.*

</details>

***API Статистика***

<details>
<summary><code>GET/api/v1/tasks_statistics/leader/</code></summary>

*Получение статистики по статусам задач исполнителей, где пользователь является руководителем.*

```
{
  "total_tasks": 0,
  "status_counts": {
    "done": 0,
    "in_work": 0,
    "new": 0
  }
}
```

</details>
<details>
<summary><code>GET/api/v1/tasks_statistics/all/</code></summary>

*Получение статистики по статусам всех задач*

```
{
  "total_tasks": 0,
  "status_counts": {
    "done": 0,
    "in_work": 0,
    "new": 0
  }
}
```

</details>
<details>
<summary><code>GET/api/v1/tasks_statistics/implementer/</code></summary>

*Получение статистики по текущему пользователю, собственная статистика.*

```
{
  "total_tasks": 0,
  "status_counts": {
    "done": 0,
    "in_work": 0,
    "new": 0
  }
}
```

</details>