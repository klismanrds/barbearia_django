# clientes/models.py
from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    telefone = models.CharField(max_length=15, verbose_name="Telefone", help_text="Ex: (99) 99999-9999")
    email = models.EmailField(max_length=100, verbose_name="E-mail", blank=True, null=True)
    data_nascimento = models.DateField(verbose_name="Data de Nascimento", blank=True, null=True)
    
    # Campo para registrar quando o cliente foi adicionado (apenas para referência)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome']

    def __str__(self):
        return self.nome