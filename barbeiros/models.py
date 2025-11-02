# barbeiros/models.py
from django.db import models
from usuarios.models import Usuario

class Barbeiro(models.Model):
    # Relaciona o Barbeiro diretamente ao nosso modelo de Usuário
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        limit_choices_to={'cargo': Usuario.Cargo.BARBEIRO}, # Só pode ser ligado a usuários Barbeiros
        related_name='perfil_barbeiro'
    )
    comissao_percentual = models.DecimalField(
        max_digits=5, decimal_places=2, default=50.00
    ) 
    telefone = models.CharField(max_length=15, blank=True, null=True)
    
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Barbeiro"
        verbose_name_plural = "Barbeiros"

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username