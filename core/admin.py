from django.contrib import admin
from .models import GlossarioCultural, PerfilColaborador, ReuniaoAcessivel, AnaliseFeedback

# Configuração Personalizada para o Glossário
@admin.register(GlossarioCultural)
class GlossarioAdmin(admin.ModelAdmin):
    # Colunas que aparecem na lista
    list_display = ('termo_tecnico', 'explicacao_resumida', 'tags', 'updated_at')
    
    # Campo de busca (lupa) para achar termos rápido
    search_fields = ('termo_tecnico', 'explicacao_simples', 'tags')
    
    # Filtro lateral
    list_filter = ('tags',)
    
    # Cria um resumo para não poluir a tela se a explicação for gigante
    def explicacao_resumida(self, obj):
        return obj.explicacao_simples[:80] + "..." if len(obj.explicacao_simples) > 80 else obj.explicacao_simples
    explicacao_resumida.short_description = "Explicação Simplificada"

# Registro simples dos outros modelos (opcional, mas bom ter)
admin.site.register(PerfilColaborador)
admin.site.register(ReuniaoAcessivel)
admin.site.register(AnaliseFeedback)
