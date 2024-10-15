from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission)


class Role(models.Model):
    """Модель роли пользователя."""
    title = models.CharField(
        'Название',
        max_length=64,
    )

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.title


class Profession(models.Model):
    """Модель профессии пользователя."""
    title = models.CharField(
        'Название',
        max_length=64,
    )

    class Meta:
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель роли команды."""
    name = models.CharField(
        'Название',
        max_length=50,
        unique=True
    )

    leader = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='lead_groups',
        verbose_name='Руководитель',
        null=True
    )

    moderators = models.ManyToManyField(
        'CustomUser',
        related_name='moderated_groups',
        verbose_name='Модераторы',
        blank=True
    )

    specialists = models.ManyToManyField(
        'CustomUser',
        related_name='specialized_groups',
        verbose_name='Специалисты',
        blank=True
    )

    datetime_update = models.DateTimeField(
        verbose_name='Дата редактирования',
        auto_now=True
    )

    datetime_create = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        ordering = ('name', '-datetime_create')

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **kwargs):
        is_staff = kwargs.pop('is_staff', False)
        is_superuser = kwargs.pop('is_superuser', False)
        role = Role(id=2)
        kwargs.setdefault('role', role)
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=True,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password, **kwargs):
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        role = Role(id=1)
        kwargs.setdefault('role', role)

        return self._create_user(email=email, password=password, **kwargs)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя."""
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=128,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=128,
        blank=True,
        null=True,
    )
    middle_name = models.CharField(
        verbose_name='Отчество',
        max_length=128,
        blank=True,
        null=True,
    )
    role = models.ForeignKey(
        verbose_name='Роль',
        to=Role,
        on_delete=models.PROTECT,
        related_name='role',
        null=True,
        blank=True,
    )

    Profession = models.ForeignKey(
        Profession,
        on_delete=models.CASCADE,
        related_name='profession',
        verbose_name='Профессия',
        blank=True,
        null=True
    )

    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=15,
        blank=True,
        null=True,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Email',
        null=False,
        unique=True,
    )
    is_staff = models.BooleanField(
        verbose_name='Суперпользователь',
        default=False
    )
    is_active = models.BooleanField(
        verbose_name='Активен',
        default=True
    )

    is_blocked = models.BooleanField(
        verbose_name='Заблокирован',
        default=False
    )

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'first_name',
        'last_name',
        'middle_name',
        'password',
    )

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'
