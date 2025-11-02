from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .models import Barbeiro
from .forms import BarbeiroCreateForm, BarbeiroUpdateForm
from django import forms
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# 1. DEFINIÇÃO DO MIXIN DE SEGURANÇA (Resolve o erro "não está definido")
class BarbeiroLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login') # Redireciona para sua URL de login

# 1. DEFINIÇÃO DO MIXIN DE SEGURANÇA (Resolve o erro "não está definido")
class BarbeiroLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login') # Redireciona para sua URL de login


# 2. Criação de Barbeiro
class BarbeiroCreateView(BarbeiroLoginRequiredMixin, CreateView):
    model = Barbeiro
    form_class = BarbeiroCreateForm
    template_name = 'barbeiros/barbeiro_form.html'
    success_url = reverse_lazy('barbeiros:lista_barbeiros')
    
    def form_valid(self, form):
        barbeiro = form.save()
        messages.success(self.request, f"Barbeiro {barbeiro.usuario.username} criado com sucesso!") 
        return redirect(self.success_url)

# 3. Listagem de Barbeiros
class BarbeiroListView(BarbeiroLoginRequiredMixin, ListView):
    model = Barbeiro
    context_object_name = 'barbeiros' 
    template_name = 'barbeiros/barbeiro_list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Lógica para filtrar inativos
        if self.request.GET.get('inativos'):
            return queryset.order_by('usuario__first_name')
        else:
            return queryset.filter(ativo=True).order_by('usuario__first_name')

class BarbeiroUpdateView(BarbeiroLoginRequiredMixin, UpdateView):
    model = Barbeiro
    form_class = BarbeiroUpdateForm
    template_name = 'barbeiros/barbeiro_form.html'
    success_url = reverse_lazy('barbeiros:lista_barbeiros')


class BarbeiroDeleteView(LoginRequiredMixin, DeleteView):
    model = Barbeiro
    template_name = 'barbeiros/barbeiro_confirm_delete.html'
    success_url = reverse_lazy('barbeiros:lista_barbeiros')

    def delete(self, request, *args, **kwargs):
        barbeiro = self.get_object()
        username = barbeiro.usuario.username
        messages.success(request, f"O barbeiro '{username}' foi removido com sucesso.")
        return super().delete(request, *args, **kwargs)

class AlterarSenhaForm(forms.Form):
    senha_atual = forms.CharField(
        label="Senha atual",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    nova_senha = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirmar_senha = forms.CharField(
        label="Confirmar nova senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        nova = cleaned_data.get('nova_senha')
        confirmar = cleaned_data.get('confirmar_senha')
        if nova != confirmar:
            raise forms.ValidationError("As novas senhas não conferem.")
        return cleaned_data


class AlterarSenhaView(LoginRequiredMixin, FormView):
    template_name = 'usuarios/alterar_senha.html'
    form_class = AlterarSenhaForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = self.request.user
        senha_atual = form.cleaned_data['senha_atual']
        nova_senha = form.cleaned_data['nova_senha']

        if not user.check_password(senha_atual):
            messages.error(self.request, "A senha atual está incorreta.")
            return self.form_invalid(form)

        user.set_password(nova_senha)
        user.save()
        messages.success(self.request, "Senha alterada com sucesso! Faça login novamente.")
        return super().form_valid(form)
    
# ==========================
# LISTAR BARBEIROS
# ==========================
@login_required
def lista_barbeiros(request):
    barbeiros = Barbeiro.objects.select_related('usuario').all()
    return render(request, 'lista_barbeiros.html', {'barbeiros': barbeiros})


# ==========================
# CRIAR NOVO BARBEIRO
# ==========================
@login_required
def novo_barbeiro(request):
    if request.method == 'POST':
        form = BarbeiroCreateForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Novo barbeiro cadastrado com sucesso!')
            return redirect('barbeiros:lista_barbeiros')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = BarbeiroCreateForm()

    return render(request, 'novo_barbeiro.html', {'form': form})


# ==========================
# EDITAR BARBEIRO (perfil do próprio barbeiro logado)
# ==========================
@login_required
def editar_barbeiro(request):
    # Obtém o barbeiro logado
    barbeiro = get_object_or_404(Barbeiro, usuario=request.user)

    if request.method == 'POST':
        form = BarbeiroUpdateForm(request.POST, instance=barbeiro)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('dashboard')  # pode trocar por 'barbeiros:lista_barbeiros' se quiser
        else:
            messages.error(request, "Verifique os erros no formulário.")
    else:
        form = BarbeiroUpdateForm(instance=barbeiro)

    return render(request, 'editar_barbeiro.html', {'form': form})