from django.db import models
from usuarios.models import Empresa, Usuario


class Publicacao(models.Model):
    STATUS = (
        ('pendente', 'Pendente'),
        ('aguardando_aprovacao', 'Aguardando Aprovação do Cliente'),
        ('aprovado', 'Aprovado'),
        ('publicado', 'Publicado'),
        ('faturado', 'Faturado'),
        ('pago', 'Pago'),
    )

    cliente = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='publicacoes'
    )

    funcionario_responsavel = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='publicacoes_funcionario'
    )

    titulo = models.CharField(max_length=200)

    arquivo = models.FileField(
        upload_to='publicacoes/',
        blank=True,
        null=True
    )

    jornal = models.CharField(max_length=100, blank=True)

    data_pedido = models.DateTimeField(auto_now_add=True)

    data_publicacao = models.DateField(blank=True, null=True)

    status = models.CharField(
        max_length=30,
        choices=STATUS,
        default='pendente'
    )

    valor_definido = models.BooleanField(default=False)

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Publicação'
        verbose_name_plural = 'Publicações'

    def __str__(self):
        return self.titulo