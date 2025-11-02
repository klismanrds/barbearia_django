# usuarios/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Campo para identificar o cargo dentro da barbearia
    class Cargo(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        BARBEIRO = 'BARBEIRO', 'Barbeiro'
        
    cargo = models.CharField(
        max_length=8,
        choices=Cargo.choices,
        default=Cargo.BARBEIRO,
        verbose_name='Cargo na Barbearia'
    )
    
    telefone = models.CharField(max_length=15, blank=True, null=True)
    # ... (restante do modelo)