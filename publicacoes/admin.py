from django.contrib import admin
from .models import Publicacao
from usuarios.models import Usuario


@admin.register(Publicacao)
class PublicacaoAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'cliente',
        'funcionario_responsavel',
        'jornal',
        'status',
        'data_pedido',
        'data_publicacao',
        'tamanho',
        'valor_definido',
        'valor',
    )

    list_filter = (
        'status',
        'jornal',
        'valor_definido',
        'data_publicacao',
    )

    search_fields = (
        'titulo',
        'cliente__nome',
        'cliente__cnpj',
        'jornal',
    )

    ordering = ('-data_pedido',)

    fieldsets = (
        ('Dados principais', {
            'fields': (
                'cliente',
                'funcionario_responsavel',
                'titulo',
                'arquivo',
            )
        }),
        ('Publicação', {
            'fields': (
                'jornal',
                'data_publicacao',
                'tamanho',
                'status',
            )
        }),
        ('Financeiro', {
            'fields': (
                'valor_definido',
                'valor',
            )
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "funcionario_responsavel":
            kwargs["queryset"] = Usuario.objects.filter(
                tipo_usuario__in=['admin', 'funcionario'],
                is_active=True
            )

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs
        )