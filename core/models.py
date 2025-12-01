from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# --- Utilitários ---
def audio_upload_path(instance, filename):
    """Gera um caminho organizado: media/reunioes/audio/ID_DA_REUNIAO/arquivo.mp3"""
    # Como o ID ainda não existe na criação, usamos 'temp' ou tratamos depois, 
    # mas para hackathon o ID costuma funcionar se salvar em duas etapas ou usar UUID.
    # Vamos simplificar salvando por data.
    from datetime import datetime
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    return f'reunioes/audio/{data_hoje}/{filename}'

class TimeStampedModel(models.Model):
    """Classe abstrata para auditar criação e modificação em todas as tabelas"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# --- Modelos do Negócio ---

class PerfilColaborador(TimeStampedModel):
    """
    Extensão do usuário para dados de Acessibilidade.
    Resolve a dor: Identificar necessidades especiais (Pedro) e contexto (Mariana).
    """
    TIPO_DEFICIENCIA = [
        ('NENHUMA', 'Nenhuma'),
        ('AUDITIVA', 'Auditiva / Surdez'),
        ('VISUAL', 'Visual / Baixa Visão'),
        ('MOTORA', 'Motora'),
        ('INTELECTUAL', 'Intelectual / Neurodivergente'),
        ('OUTRA', 'Outra'),
    ]

    PREFERENCIA_COMUNICACAO = [
        ('TEXTO', 'Texto / Chat (Assíncrono)'),
        ('LIBRAS', 'LIBRAS (Língua de Sinais)'),
        ('LEITURA_LABIAL', 'Vídeo com Foco Labial'),
        ('AUDIO', 'Áudio / Voz'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    cargo = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    
    # Dados cruciais para a acessibilidade (Lei LBI)
    deficiencia = models.CharField(
        max_length=20, 
        choices=TIPO_DEFICIENCIA, 
        default='NENHUMA',
        verbose_name="Tipo de Deficiência"
    )
    
    preferencia_comunicacao = models.CharField(
        max_length=20, 
        choices=PREFERENCIA_COMUNICACAO, 
        default='TEXTO',
        verbose_name="Preferência de Comunicação"
    )

    bio_resumida = models.TextField(blank=True, help_text="Breve descrição para vitrine de talentos.")

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.cargo})"


class ReuniaoAcessivel(TimeStampedModel):
    """
    Onde ocorre a mágica do 'Escriba Inteligente'.
    Armazena o áudio e recebe o processamento da IA (Whisper + GPT).
    """
    STATUS_PROCESSAMENTO = [
        ('PENDENTE', 'Pendente'),
        ('PROCESSANDO', 'Processando IA...'),
        ('CONCLUIDO', 'Concluído'),
        ('ERRO', 'Erro no Processamento'),
    ]

    titulo = models.CharField(max_length=200, verbose_name="Título da Reunião")
    data_reuniao = models.DateTimeField(verbose_name="Data e Hora")
    participantes = models.ManyToManyField(User, related_name='reunioes')
    
    # Arquivo de áudio (Input)
    arquivo_audio = models.FileField(upload_to=audio_upload_path, blank=True, null=True, verbose_name="Gravação (MP3/WAV)")
    
    # Campos preenchidos pela IA (Output)
    transcricao_completa = models.TextField(blank=True, verbose_name="Transcrição Literal (Whisper)")
    
    resumo_executivo = models.TextField(blank=True, verbose_name="Ata Inteligente (GPT)")
    
    # O Pulo do Gato: JSON que guarda quem deu qual ideia.
    # Ex: {"Pedro": ["Sugeriu mudar o layout", "Alertou sobre o bug"], "Mariana": ["Definiu o prazo"]}
    pontos_destaque = models.JSONField(default=dict, blank=True, verbose_name="Atribuição de Créditos")

    status_ia = models.CharField(max_length=20, choices=STATUS_PROCESSAMENTO, default='PENDENTE')

    def __str__(self):
        return f"{self.titulo} - {self.data_reuniao.strftime('%d/%m/%Y')}"


class GlossarioCultural(TimeStampedModel):
    """
    Banco de dados para o 'Tradutor Cultural'.
    Ajuda a Mariana a entender termos complexos sem constrangimento.
    """
    termo_tecnico = models.CharField(max_length=200, unique=True, help_text="Ex: Budget, Churn, ASAP")
    explicacao_simples = models.TextField(help_text="Explicação em linguagem clara e acessível.")
    exemplo_uso = models.TextField(blank=True)
    
    tags = models.CharField(max_length=200, blank=True, help_text="Ex: Financeiro, TI, Siglas")

    def __str__(self):
        return self.termo_tecnico


class AnaliseFeedback(TimeStampedModel):
    """
    Ferramenta de Mentoria para Líderes.
    Detecta viés inconsciente antes do envio do feedback.
    """
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks_enviados')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks_recebidos')
    
    texto_original = models.TextField()
    
    # Análise da IA
    texto_sugerido_ia = models.TextField(blank=True, help_text="Versão reescrita para ser mais inclusiva")
    vies_detectado = models.BooleanField(default=False)
    explicacao_vies = models.TextField(blank=True, help_text="Explicação pedagógica do viés encontrado")
    
    foi_enviado = models.BooleanField(default=False)

    def __str__(self):
        return f"Feedback de {self.autor} para {self.destinatario}"