# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

# Importação dos nossos módulos
from .models import ReuniaoAcessivel, GlossarioCultural, PerfilColaborador
from .forms import ReuniaoForm, FeedbackForm, TradutorForm
from .services import IAService  # Certifique-se de ter criado o services.py anteriormente!

# --- VIEW 1: Dashboard Principal ---
def dashboard(request):
    """
    Tela inicial. Mostra as últimas reuniões processadas e estatísticas rápidas.
    """
    reunioes = ReuniaoAcessivel.objects.all().order_by('-data_reuniao')
    
    context = {
        'reunioes': reunioes,
        'total_reunioes': reunioes.count(),
        'colaboradores_cadastrados': PerfilColaborador.objects.count()
    }
    return render(request, 'core/dashboard.html', context)


# --- VIEW 2: Upload e Processamento (O Coração do Sistema) ---
def upload_reuniao(request):
    if request.method == 'POST':
        form = ReuniaoForm(request.POST, request.FILES)
        if form.is_valid():
            reuniao = form.save(commit=False)
            reuniao.status_ia = 'PROCESSANDO'
            reuniao.save()
            
            # IMPORTANTE: Salvar o Many-to-Many antes de usar
            form.save_m2m() 

            try:
                # 1. Pega os nomes dos participantes selecionados no form
                # Cria uma string: "Pedro.Henrique, Carlos.Junior, Admin"
                nomes_participantes = ", ".join([p.username for p in reuniao.participantes.all()])

                # 2. Transcrição (Whisper)
                caminho = reuniao.arquivo_audio.path
                texto = IAService.transcrever_reuniao(caminho)
                reuniao.transcricao_completa = texto

                # 3. Passa os nomes para a IA (AGORA COM CONTEXTO!)
                insights = IAService.gerar_ata_inteligente(texto, nomes_participantes)
                reuniao.resumo_executivo = insights
                
                # ... (resto do código igual) ...
                
                # Sucesso!
                reuniao.status_ia = 'CONCLUIDO'
                reuniao.save()
                
                messages.success(request, f"Reunião '{reuniao.titulo}' processada com sucesso! Acessibilidade gerada.")
                return redirect('detalhe_reuniao', pk=reuniao.pk)

            except Exception as e:
                reuniao.status_ia = 'ERRO'
                reuniao.save()
                messages.error(request, f"Erro ao processar IA: {str(e)}")
                return redirect('dashboard')
    else:
        form = ReuniaoForm()

    return render(request, 'core/upload.html', {'form': form})


# --- VIEW 3: Detalhes da Reunião (Visão do Pedro/PCD) ---
def detalhe_reuniao(request, pk):
    """
    Exibe a ata, a transcrição e o player de áudio.
    """
    reuniao = get_object_or_404(ReuniaoAcessivel, pk=pk)
    return render(request, 'core/detalhe_reuniao.html', {'reuniao': reuniao})


# --- VIEW 4: Mentoria de Feedback (Visão do Gestor) ---
def mentoria_feedback(request):
    """
    Página onde o gestor digita o feedback.
    """
    form = FeedbackForm()
    return render(request, 'core/mentoria_feedback.html', {'form': form})


# --- VIEW 5: Endpoint HTMX (Mágica Assíncrona) ---
def checar_feedback_htmx(request):
    """
    Esta view não retorna uma página inteira, apenas um pedaço de HTML.
    É chamada automaticamente enquanto o usuário digita no formulário.
    """
    texto = request.POST.get('texto_original', '')
    
    if len(texto) < 10:
        return render(request, 'core/partials/analise_feedback_result.html', {'mensagem': 'Digite mais para analisar...'})

    # Chama a IA para detectar viés
    analise_ia = IAService.analisar_vies_feedback(texto)
    
    # Renderiza apenas o "card" com o resultado
    return render(request, 'core/partials/analise_feedback_result.html', {'analise': analise_ia})


# --- VIEW 6: Tradutor Cultural (Visão da Mariana) ---
# Substitua a função glossario_cultural antiga por esta nova versão completa:

def glossario_cultural(request):
    """
    Exibe o glossário E TAMBÉM processa a tradução de textos inteiros.
    """
    # 1. Lógica da Busca Simples (Glossário Visual)
    query = request.GET.get('q')
    termos = GlossarioCultural.objects.all()
    if query:
        termos = termos.filter(termo_tecnico__icontains=query)

    # 2. Lógica da Tradução (IA)
    traducao_resultado = None
    form = TradutorForm()

    if request.method == 'POST':
        form = TradutorForm(request.POST)
        if form.is_valid():
            texto_original = form.cleaned_data['texto_complexo']
            # Chama o serviço de RAG que criamos
            traducao_resultado = IAService.tradutor_cultural(texto_original)

    context = {
        'termos': termos,
        'form': form,
        'traducao': traducao_resultado
    }
    return render(request, 'core/glossario.html', context)

def lista_colaboradores(request):
    """
    Lista todos os perfis cadastrados para monitoramento de inclusão.
    """
    # Usamos select_related('user') para otimizar a busca no banco (boa prática!)
    colaboradores = PerfilColaborador.objects.select_related('user').all()
    
    return render(request, 'core/lista_colaboradores.html', {'colaboradores': colaboradores})
