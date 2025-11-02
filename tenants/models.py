# tenants/models.py
from django_tenants.models import TenantMixin, DomainMixin
from django.db import models

class Barbearia(TenantMixin):
    """Representa a Barbearia (Tenant)"""
    name = models.CharField(max_length=100)
    paid_until = models.DateField() # Exemplo de campo de gerenciamento
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    class Meta:
        verbose_name = "Barbearia"
        verbose_name_plural = "Barbearias"

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    """Representa o Domínio ou Subdomínio de acesso do Tenant"""
    pass # Este modelo é usado pelo django-tenants para mapear o domínio à Barbearia