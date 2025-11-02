# agendamentos/forms.py
from django import forms
from .models import Agendamento
from clientes.models import Cliente
from barbeiros.models import Barbeiro
from servicos.models import Servico
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

class AgendamentoForm(forms.ModelForm):
    # Campo Cliente com Select2 (Mantido)
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all().order_by('nome'),
        label="Cliente",
        widget=forms.Select(attrs={'class': 'form-select select2-enable'}) 
    )
    
    # NOVO: Campo Data (Inicializado com a data atual)
    data = forms.DateField(
        label="Data do Agendamento",
        initial=timezone.localdate(), # Define a data inicial como hoje
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'},
            format='%Y-%m-%d'
        )
    )
    
    # NOVO: Campo Hora
    hora = forms.TimeField(
        label="Hora do Agendamento",
        widget=forms.TimeInput(
            attrs={'class': 'form-control', 'type': 'time'}
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Lógica para preencher Data e Hora na Edição (UpdateView)
        if self.instance and self.instance.pk and self.instance.data_hora_inicio:
            # Converte para o fuso horário local
            data_hora_local = timezone.localtime(self.instance.data_hora_inicio)
            self.fields['data'].initial = data_hora_local.date()
            self.fields['hora'].initial = data_hora_local.time()
            
    class Meta:
        model = Agendamento
        # REMOVIDO 'data_hora_inicio', 'duracao_minutos', 'preco_final'
        fields = [
            'cliente', 'barbeiro', 'servico', 
            'data', 'hora', # Adicionados para entrada do usuário
            'status', 'observacoes'
        ]
        
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    # O método clean é chamado para validar o formulário
def clean(self):
        cleaned_data = super().clean()
        
        data = cleaned_data.get('data')
        hora = cleaned_data.get('hora')
        barbeiro = cleaned_data.get('barbeiro')
        servico = cleaned_data.get('servico')

        if data and hora and barbeiro and servico:
            
            # 1. Combina Data e Hora
            data_hora_inicio = timezone.make_aware(timezone.datetime.combine(data, hora))
            
            # 2. Calcula o Fim do Agendamento Proposto
            duracao = timedelta(minutes=servico.duracao_minutos)
            data_hora_fim_proposta = data_hora_inicio + duracao
            
            # 3. VALIDAÇÃO DE CONFLITO (Lógica de sobreposição padrão)
            
            # Procura por QUALQUER agendamento do barbeiro, exceto o atual (self.instance.pk)
            # que COMEÇA antes do novo agendamento terminar (data_hora_inicio__lt=data_hora_fim_proposta)
            # E TERMINA depois do novo agendamento começar (data_hora_fim__gt=data_hora_inicio)
            
            conflitos = Agendamento.objects.filter(
                barbeiro=barbeiro,
                data_hora_inicio__lt=data_hora_fim_proposta, # O agendamento existente começa antes do novo terminar
                data_hora_fim__gt=data_hora_inicio           # E termina depois do novo começar
            ).exclude(
                pk=self.instance.pk # Exclui o próprio objeto em caso de edição
            )
            
            if conflitos.exists():
                # Formata a mensagem de erro
                conflito_existente = conflitos.first()
                raise ValidationError(
                    f"Conflito de Horário! O Barbeiro {barbeiro.usuario.first_name} já está reservado das "
                    f"{timezone.localtime(conflito_existente.data_hora_inicio).strftime('%H:%M')} às "
                    f"{timezone.localtime(conflito_existente.data_hora_fim).strftime('%H:%M')}."
                )

        return cleaned_data