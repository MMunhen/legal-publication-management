from django.contrib.auth.models import AbstractUser
from django.db import models


class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.nome


class Usuario(AbstractUser):
    TIPOS = (
        ('admin', 'Administrador'),
        ('funcionario', 'Funcionário'),
        ('cliente', 'Cliente'),
    )

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPOS,
        default='cliente'
    )

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    representante = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.username