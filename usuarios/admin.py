from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Empresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'telefone')
    search_fields = ('nome', 'cnpj')


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = (
        ('Acesso', {
            'fields': (
                'username',
                'password',
                'tipo_usuario',
            )
        }),
        ('Dados do usuário', {
            'fields': (
                'email',
                'empresa',
                'representante',
                'celular',
            )
        }),
        ('Permissões Django', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Datas', {
            'fields': (
                'last_login',
                'date_joined',
            )
        }),
    )

    add_fieldsets = (
        ('Criar novo usuário', {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2',
                'tipo_usuario',
                'empresa',
                'representante',
                'is_active',
                'is_staff',
                'is_superuser',
                'email',
                'celular',
            ),
        }),
    )

    list_display = (
        'username',
        'empresa',
        'tipo_usuario',
        'representante',
        'is_staff',
        'is_active',
        'email',
        'celular',
    )

    list_filter = (
        'tipo_usuario',
        'is_staff',
        'is_active',
    )

    search_fields = (
        'username',
        'empresa__nome',
        'empresa__cnpj',
        'representante',
        'email',
    )

    ordering = ('username',)