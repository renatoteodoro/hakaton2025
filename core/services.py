# core/services.py

import openai
from django.conf import settings
from .models import GlossarioCultural

# Inicializa o cliente da OpenAI com a chave configurada no settings.py
# (que por sua vez pega do .env)
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

class IAService:
    """
    Camada de Serviço que isola toda a lógica de Inteligência Artificial.
    Isso mantém as Views limpas e facilita a manutenção.
    """

    @staticmethod
    def transcrever_reuniao(caminho_arquivo_audio):
        """
        Recebe o caminho físico do arquivo de áudio (MP3/WAV) e envia para o Whisper.
        Retorna: String com o texto completo transcrito.
        """
        try:
            with open(caminho_arquivo_audio, "rb") as audio_file:
                # O modelo 'whisper-1' é o estado da arte para Speech-to-Text
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file,
                    language="pt", # Força português para melhorar a precisão
                    prompt="Esta é uma reunião corporativa técnica. Identifique os falantes se possível."
                )
            return transcript.text
        except Exception as e:
            print(f"Erro na Transcrição: {e}")
            return "Erro: Não foi possível transcrever o áudio. Verifique o formato do arquivo."

    # @staticmethod
    # def gerar_ata_inteligente(texto_transcrito, lista_participantes="Desconhecidos"): # <--- ADICIONE ESTE 2º PARÂMETRO
    #     """
    #     Gera a Ata Inclusiva com foco em Autoria e Crédito.
    #     Remove formatação Markdown para não quebrar o layout.
    #     """
    #     prompt_sistema = f"""  # <--- Note o 'f' aqui para permitir variáveis
    #     Você é um Assistente de Inclusão Corporativa e Secretário Executivo Sênior.
    #     Sua missão principal é combater a invisibilidade em reuniões, garantindo que a autoria das ideias seja atribuída corretamente.

    #     CONTEXTO DA REUNIÃO:
    #     Participantes Presentes: {lista_participantes}  # <--- AQUI A VARIÁVEL ENTRA
    #     (Use esses nomes para atribuir a autoria das falas e ideias).
        
    #     DIRETRIZES DE ANÁLISE:
    #     1. Se o texto mencionar "O [Nome] disse no chat..." ou "Lendo aqui o que o [Nome] escreveu...", a autoria da ideia é do [Nome], e não de quem leu.
    #     2. Destaque ideias dadas por pessoas que foram interrompidas ou falaram pouco.
        
    #     FORMATO DE SAÍDA (HTML ESTRITO):
    #     Não use Markdown (```). Retorne apenas o código HTML puro usando classes Bootstrap 5 simples.
        
    #     Estrutura desejada:
    #     <div class="mb-4">
    #         <h4 class="text-primary">📋 Resumo Executivo</h4>
    #         <p>[Um parágrafo resumindo o objetivo da reunião e decisões finais]</p>
    #     </div>

    #     <div class="mb-4">
    #         <h4 class="text-success">💡 Mapa de Autoria & Créditos (Destaque Inclusivo)</h4>
    #         <ul class="list-group">
    #             <li class="list-group-item">
    #                 <strong>[Nome do Autor]</strong>: [Ideia/Sugestão dada] 
    #                 <span class="badge bg-secondary ms-2">[Via Chat/Oral]</span>
    #             </li>
    #             </ul>
    #     </div>

    #     <div>
    #         <h4 class="text-warning">⚠️ Pontos de Atenção</h4>
    #         <p>[Cite se houve interrupções, falhas técnicas ou ruídos que atrapalharam a inclusão]</p>
    #     </div>
    #     """

    #     try:
    #         response = client.chat.completions.create(
    #             model="gpt-4o-mini",
    #             messages=[
    #                 {"role": "system", "content": prompt_sistema},
    #                 {"role": "user", "content": f"Transcrição da Reunião para análise:\n\n{texto_transcrito[:20000]}"}
    #             ],
    #             temperature=0.4 
    #         )
            
    #         content = response.choices[0].message.content
            
    #         # Limpeza de Markdown
    #         content = content.replace("```html", "").replace("```", "").strip()
            
    #         return content

    #     except Exception as e:
    #         return f"<div class='alert alert-danger'>Erro ao gerar ata inteligente: {str(e)}</div>"


    @staticmethod
    def gerar_ata_inteligente(texto_transcrito, lista_participantes="Desconhecidos"):
        """
        Gera a Ata Inclusiva. 
        AJUSTE: Agora detecta APROPRIAÇÃO DE IDEIAS (Bropriating) e evita alucinar interrupções.
        """
        prompt_sistema = f"""
        Você é um Especialista em Dinâmica de Grupo e Inclusão.
        Sua missão é identificar a VERDADEIRA autoria das ideias e proteger participantes de apropriação.

        CONTEXTO:
        Participantes: {lista_participantes}

        REGRAS CRÍTICAS DE ANÁLISE (LEIA COM ATENÇÃO):
        
        1. DETECÇÃO DE APROPRIAÇÃO ("Bropriating"):
           - Se a Pessoa A der uma ideia e a Pessoa B disser logo em seguida algo como "Exatamente o que eu ia dizer", "Eu já sabia disso", "Como eu disse antes" (sem ter dito), ou apenas repetir a ideia com outras palavras:
           - A CRÉDITO É 100% DA PESSOA A.
           - NÃO coloque a Pessoa B no "Mapa de Autoria" para essa ideia específica. Coloque a ação da Pessoa B nos "Pontos de Atenção" como "Comportamento de Apropriação".

        2. INTERRUPÇÕES (Sem Alucinação):
           - Só marque interrupção se alguém foi CORTADO no meio de uma frase e não conseguiu concluir.
           - Se a pessoa terminou a frase e houve apenas uma troca rápida de turno, ISSO NÃO É INTERRUPÇÃO.
           - Se ninguém foi interrompido, escreva: "Fluidez da conversa foi mantida."

        3. PEDRO (PCD/Chat):
           - Se houver menção de leitura de chat ("O Pedro disse..."), a autoria é EXCLUSIVA do Pedro. Quem leu foi apenas o porta-voz.

        FORMATO DE SAÍDA (HTML Bootstrap 5):
        Não use Markdown. Retorne HTML puro.

        Estrutura:
        <div class="mb-4">
            <h4 class="text-primary"><i class="bi bi-clipboard-data"></i> Resumo Executivo</h4>
            <p>[Resumo objetivo das decisões]</p>
        </div>

        <div class="mb-4">
            <h4 class="text-success"><i class="bi bi-lightbulb"></i> Mapa de Autoria Real (Quem teve a ideia)</h4>
            <ul class="list-group">
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <strong>[Nome do Autor Original]</strong>: [A ideia resumida]
                    </div>
                    <span class="badge bg-primary rounded-pill">[Canal: Chat/Voz]</span>
                </li>
            </ul>
        </div>

        <div class="card border-warning mb-3">
            <div class="card-header bg-warning text-dark fw-bold">
                <i class="bi bi-exclamation-triangle"></i> Análise de Comportamento & Apropriação
            </div>
            <div class="card-body">
                <ul class="mb-0">
                    <li>[Ex: Carlos tentou validar a ideia de Pedro como se fosse dele ("Eu já sabia"), mas o crédito original foi mantido.]</li>
                    <li>[Ex: Nenhuma interrupção brusca detectada.]</li>
                </ul>
            </div>
        </div>
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini", # Se puder usar gpt-4o (sem mini) fica ainda mais inteligente
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": f"Transcrição:\n\n{texto_transcrito[:20000]}"}
                ],
                temperature=0.2 # Temperatura baixa para ser mais analítico e menos "criativo"
            )
            
            content = response.choices[0].message.content
            content = content.replace("```html", "").replace("```", "").strip()
            return content

        except Exception as e:
            return f"<div class='alert alert-danger'>Erro: {str(e)}</div>"

    @staticmethod
    def analisar_vies_feedback(texto_feedback):
        """
        Analisa viés com explicação detalhada e pedagógica.
        """
        prompt_sistema = """
        Você é um Mentor Sênior em Liderança Inclusiva e Psicologia Organizacional.
        Sua missão é educar os gestores sobre vieses inconscientes de forma profunda e específica.
        
        Analise o feedback abaixo.
        
        REGRAS PARA A EXPLICAÇÃO DO VIÉS (SEJA DETALHISTA):
        Se encontrar problemas, não dê respostas genéricas.
        1. Identifique o trecho exato: Cite as palavras usadas (ex: "O uso do termo 'emocional'...").
        2. Explique o conceito: Diga qual viés está agindo (ex: "Double Bind" de gênero, "Glass Ceiling", "Estereótipo de Agressividade").
        3. Explique o impacto: Por que isso desmotiva? Por que é injusto? (ex: "Ao comparar com Pedro, você invalida a jornada individual da Mariana").
        
        REGRAS PARA A REESCRITA:
        1. Remova qualquer comparação com outros colegas.
        2. Troque julgamentos de personalidade por observações de fatos/resultados.
        3. Mantenha um tom de desenvolvimento (Growth Mindset).

        FORMATO DE SAÍDA (HTML):
        Se houver viés, retorne:
        <div class='alert alert-warning'>
           <h5 class='alert-heading'><i class='bi bi-exclamation-triangle'></i> Análise de Viés Detectada:</h5>
           <ul class='mb-3'>
               <li>[Explicação detalhada do ponto 1]</li>
               <li>[Explicação detalhada do ponto 2]</li>
           </ul>
           <hr>
           <strong>💡 Sugestão de Reescrita (Focada em Fatos):</strong><br>
           <em>"[Texto reescrito]"</em>
        </div>

        Se for neutro: "<span class='text-success'>✅ Feedback Inclusivo e Aprovado!</span>"
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": f"Texto do Feedback: '{texto_feedback}'"}
                ],
                temperature=0.3 # Um pouco mais alto para permitir explicações mais fluídas
            )
            return response.choices[0].message.content
        except Exception as e:
            return "<span class='text-danger'>Erro ao conectar com a IA de análise.</span>"

    @staticmethod
    def tradutor_cultural(texto_complexo):
        """
        RAG: Busca termos e traduz mantendo a ordem estrita: TermoOriginal (**Tradução**)
        """
        todos_termos = GlossarioCultural.objects.all()
        # Cria o contexto
        contexto_glossario = "\n".join([f"- {t.termo_tecnico}: {t.explicacao_simples}" for t in todos_termos])
        
        prompt_sistema = f"""
        Você é um assistente que ajuda funcionários a entender termos corporativos.
        Use este Glossário como referência:
        {contexto_glossario}
        
        REGRAS CRÍTICAS DE FORMATAÇÃO (SIGA ESTRITAMENTE):
        1. NÃO substitua o termo original pela tradução. Mantenha o termo em inglês/sigla no texto.
        2. Adicione a explicação IMEDIATAMENTE APÓS o termo original.
        3. Use o formato: TermoOriginal (**Explicação**)
        
        EXEMPLOS DE O QUE FAZER E O QUE NÃO FAZER:
        
        Texto Original: "Preciso do report ASAP."
        
        ❌ ERRADO (Não inverta):
        "Preciso do relatório (**report**) assim que possível (**ASAP**)."
        
        ✅ CERTO (Mantenha a ordem):
        "Preciso do report (**relatório**) ASAP (**assim que possível**)."
        
        Texto Original: "O Churn subiu."
        ✅ CERTO: "O Churn (**taxa de cancelamento**) subiu."
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": texto_complexo}
                ],
                temperature=0.1 # Temperatura baixíssima para reduzir criatividade e forçar obediência
            )
            return response.choices[0].message.content
        except Exception as e:
            return "Erro na tradução cultural."