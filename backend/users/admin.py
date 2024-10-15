from django.contrib import admin
from .models import CustomUser, Role, Group, Profession


class GroupInline(admin.TabularInline):
    model = CustomUser.groups.through
    extra = 1
    verbose_name = "Команда"
    verbose_name_plural = "Команды"


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'id', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'role')
    inlines = [GroupInline]

    exclude = ['groups']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    search_fields = ('title',)
    list_filter = ('title',)


class ModeratorsInline(admin.TabularInline):
    model = Group.moderators.through
    extra = 2
    verbose_name = "Модератор"
    verbose_name_plural = "Модераторы"


class SpecialistsInline(admin.TabularInline):
    model = Group.specialists.through
    extra = 5
    verbose_name = "Специалист"
    verbose_name_plural = "Специалисты"


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'leader', 'datetime_update', 'datetime_create')
    search_fields = ('name', 'datetime_update', 'datetime_create')
    list_filter = ('name', 'datetime_update', 'datetime_create')
    inlines = [ModeratorsInline, SpecialistsInline]

    fields = ('name', 'leader')
