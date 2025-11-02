# clientes/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cliente
from .forms import ClienteForm

# Mixin de autenticação
class ClienteLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')

# 1. Listagem de Clientes
class ClienteListView(ClienteLoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'
    context_object_name = 'clientes' # Nome da variável no template
    
# 2. Criação de Cliente
class ClienteCreateView(ClienteLoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('clientes:lista_clientes')

# 3. Edição de Cliente
class ClienteUpdateView(ClienteLoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html' # Reutiliza o template de cadastro
    success_url = reverse_lazy('clientes:lista_clientes')

# 4. Exclusão de Cliente
class ClienteDeleteView(ClienteLoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'clientes/cliente_confirm_delete.html'
    success_url = reverse_lazy('clientes:lista_clientes')