from django.db import models
from datetime import timedelta

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)    
    duracao_minutos = models.PositiveIntegerField(default=30) 
    descricao = models.TextField(max_length=500, blank=True, null=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"

    def __str__(self):
        return f"{self.nome} (R$ {self.preco})"