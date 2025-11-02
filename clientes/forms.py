# clientes/forms.py
from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    # Adicionando widgets para melhorar a interface de usuário
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'email', 'data_nascimento']
        
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do cliente'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: (99) 99999-9999'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'opcional@email.com'}),
            # Usando o widget DateInput para forçar o campo de data
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }