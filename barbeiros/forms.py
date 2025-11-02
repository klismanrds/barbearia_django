from django import forms
from .models import Barbeiro
from usuarios.models import Usuario
from django.contrib import messages
from django.core.exceptions import ValidationError

# Funções auxiliares (usada para sugerir um username, mas a validação mais forte será no clean)
def gerar_username_unico(base):
    username = base.strip().lower().replace(" ", ".")
    original = username
    contador = 1
    while Usuario.objects.filter(username=username).exists():
        username = f"{original}{contador}"
        contador += 1
    return username

# 🧩 Formulário para criar um barbeiro (e o usuário correspondente)
class BarbeiroCreateForm(forms.ModelForm):
    # Campos extras (não pertencem ao modelo Barbeiro)
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome de Usuário (Login)'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Senha para Login'
        })
    )
    password_confirm = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar Senha'
        }),
        label='Confirmar Senha'
    )
    
    # Validação: Garante que o username não exista no banco (Resolve IntegrityError)
    def clean_username(self):
        username = self.cleaned_data['username']
        # Verifica se já existe um usuário com este username
        if Usuario.objects.filter(username=username).exists():
            raise ValidationError(
                f"Este nome de usuário ('{username}') já está em uso. Por favor, escolha outro."
            )
        return username

    # Validação: Garante que as senhas coincidam
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError("As senhas digitadas não coincidem.")
            
        return password_confirm 
    
    class Meta:
        model = Barbeiro
        # CORREÇÃO: Define fields apenas uma vez, listando campos do modelo Barbeiro.
        # O campo 'usuario' é omitido para ser setado no save().
        fields = ['comissao_percentual', 'telefone', 'ativo']
        widgets = {
            'comissao_percentual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0,
                'max': 100
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: (99) 99999-9999'
            }),
        }
    
    # Inicialização opcional (pode ser removida se não for usada)
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


    # O método save deve ser o local onde você cria o Usuario e salva o Barbeiro
    def save(self, commit=True):
        # 1. Cria o Usuário (agora validado como único)
        user = Usuario.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            cargo=Usuario.Cargo.BARBEIRO, # Define o cargo
            # Ajuste: Use o username como first_name apenas se não tiver um campo de nome real
            first_name=self.cleaned_data['username'], 
        )
        
        # 2. Cria o Objeto Barbeiro
        barbeiro = super().save(commit=False)
        barbeiro.usuario = user # Liga o usuário recém-criado ao Barbeiro
        
        if commit:
            barbeiro.save()
            
        # O método save() da View (form_valid) é quem deve usar o messages.success
        return barbeiro


# --- Formulário de Atualização (Corrigido e Simplificado) ---

class BarbeiroUpdateForm(forms.ModelForm):
    # Campos para trocar senha
    nova_senha = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nova Senha (deixe em branco se não quiser trocar)'
        }),
        label='Nova Senha'
    )
    confirmar_senha = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar Nova Senha'
        }),
        label='Confirmar Nova Senha'
    )

    class Meta:
        model = Barbeiro
        fields = ['telefone', 'comissao_percentual', 'ativo']
        widgets = {
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: (99) 99999-9999'}),
            'comissao_percentual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0, 'max': 100}),
        }

    def clean(self):
        cleaned_data = super().clean()
        nova_senha = cleaned_data.get('nova_senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        if nova_senha or confirmar_senha:
            if nova_senha != confirmar_senha:
                raise forms.ValidationError("As novas senhas não conferem.")
        return cleaned_data

    def save(self, commit=True):
        barbeiro = super().save(commit=False)
        nova_senha = self.cleaned_data.get('nova_senha')

        # Se o barbeiro quiser alterar a senha
        if nova_senha:
            barbeiro.usuario.set_password(nova_senha)
            barbeiro.usuario.save() # Salva a mudança de senha no objeto Usuario

        if commit:
            barbeiro.save() # Salva a mudança no objeto Barbeiro

        return barbeiro