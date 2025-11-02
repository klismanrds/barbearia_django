# agendamentos/models.py
from datetime import timedelta
from django.db import models
from clientes.models import Cliente
from barbeiros.models import Barbeiro
from servicos.models import Servico

# Opções de Status
STATUS_CHOICES = (
    ('P', 'Pendente'),      # Cliente agendou, mas precisa de confirmação (ou é o status inicial)
    ('C', 'Confirmado'),    # Agendamento confirmado
    ('E', 'Concluído'),     # Serviço executado e pago
    ('X', 'Cancelado'),     # Agendamento cancelado
    ('N', 'No-show'),       # Cliente não compareceu
)

class Agendamento(models.Model):
    # Relações Chave Estrangeira (ForeignKey)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agendamentos')
    barbeiro = models.ForeignKey(Barbeiro, on_delete=models.CASCADE, related_name='agendamentos')
    servico = models.ForeignKey(Servico, on_delete=models.SET_NULL, null=True, related_name='agendamentos')
    
    data_hora_inicio = models.DateTimeField(verbose_name="Data e Hora de Início")
    data_hora_fim = models.DateTimeField(null=True, blank=True, verbose_name="Data e Hora de Fim") # NOVO CAMPO    
    # Campo para o tempo de duração real, se diferente do serviço
    duracao_minutos = models.PositiveSmallIntegerField(verbose_name="Duração (minutos)")
    
    # Dados Financeiros (Preço é copiado do Serviço no momento da criação)
    preco_final = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Preço Cobrado")
    
    # Status e Controle
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='C', verbose_name="Status")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ['data_hora_inicio']

    def save(self, *args, **kwargs):
        if self.data_hora_inicio and self.duracao_minutos:
            # Calcula o fim como início + duração
            self.data_hora_fim = self.data_hora_inicio + timedelta(minutes=self.duracao_minutos)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.servico.nome} para {self.cliente.nome} em {self.data_hora_inicio.strftime('%d/%m %H:%M')}"