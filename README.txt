README - Projeto Hakaton 2025

Este projeto é uma aplicação Django para reuniões acessíveis, utilizando IA para transcrição, geração de atas inteligentes e ferramentas de inclusão.

PASSOS PARA CLONAR O PROJETO:

1. Certifique-se de ter o Git instalado no seu sistema. Se não tiver, baixe e instale a partir de https://git-scm.com/.

2. Abra o terminal ou prompt de comando.

3. Execute o comando para clonar o repositório:
   git clone https://github.com/renatoteodoro/hakaton2025.git

4. Entre no diretório do projeto clonado:
   cd hakaton2025

5. Crie um ambiente virtual (opcional mas recomendado):
   python -m venv venv
   Para ativar o ambiente virtual:
   # No Linux use: source venv/bin/activate  
   # No Windows use: venv\Scripts\activate

PASSOS PARA TESTAR A APLICAÇÃO (USABILIDADE):

Pré-requisitos:
- Python 3.8 ou superior instalado.
- Uma chave de API da OpenAI (para funcionalidades de IA).

1. Instale as dependências do projeto:
   pip install -r requirements.txt

2. Configure as variáveis de ambiente:
   - Crie ou abra o arquivo .env na raiz do projeto.
   - Adicione ou verifique a linha: OPENAI_API_KEY=sua_chave_api_aqui
   - Substitua "sua_chave_api_aqui" pela sua chave real da OpenAI.

3. Execute as migrações do banco de dados:
   python manage.py migrate

4. Inicie o servidor de desenvolvimento:
   python manage.py runserver

5. Abra um navegador web e acesse: http://127.0.0.1:8000

6. Teste as funcionalidades principais (usabilidade):
   - Dashboard: Visualize as reuniões recentes e estatísticas.
   - Upload de Reunião: Faça upload de um arquivo de áudio (MP3/WAV) de uma reunião, adicione título, data e participantes. Aguarde o processamento da IA para gerar transcrição e ata inteligente.
   - Detalhes da Reunião: Clique em uma reunião processada para ver a transcrição, ata e ouvir o áudio.
   - Glossário Cultural: Busque termos técnicos ou traduza textos complexos usando a IA.
   - Mentoria de Feedback: Digite um feedback e veja a análise de viés em tempo real.
   - Lista de Colaboradores: Visualize os perfis dos colaboradores com informações de acessibilidade.

7. Para testar uploads, use arquivos de áudio de exemplo ou grave um áudio curto.

Nota: Esta é uma aplicação de demonstração. Para uso em produção, configure adequadamente o DEBUG=False e outras configurações de segurança.