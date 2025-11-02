from django import forms
from .models import Servico

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        # Exclua o campo 'barbearia' se ele for preenchido automaticamente pelo TenantMixin
        fields = ['nome', 'preco', 'duracao_minutos', 'descricao', 'ativo'] 
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'duracao_minutos': forms.NumberInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }