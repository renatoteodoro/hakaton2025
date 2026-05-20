# Hakaton 2025 — Reuniões Acessíveis com IA

[![Django](https://img.shields.io/badge/Django-5.x-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-Whisper%20%7C%20GPT-orange.svg)](https://openai.com/)

Aplicação Django desenvolvida no Hackaton 2025 do Programa Jovem Programador — Senac/SC. Foco em **reuniões acessíveis**, utilizando IA para transcrição de áudio, geração de atas inteligentes e ferramentas de inclusão.

## Funcionalidades

- **Transcrição de reuniões** — upload de áudio (MP3/WAV) processado pelo OpenAI Whisper
- **Geração de atas** — resumo inteligente da reunião via GPT
- **Glossário Cultural** — busca e tradução de termos técnicos com IA
- **Mentoria de Feedback** — análise de viés em feedbacks em tempo real
- **Perfis de acessibilidade** — informações de inclusão dos colaboradores
- **Dashboard** — visualização de reuniões recentes e estatísticas

## Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| Backend | Django, Python 3.8+ |
| IA | OpenAI GPT, Whisper (speech-to-text) |
| Áudio | pydub |
| Frontend | Templates Django, Bootstrap |
| Banco de Dados | SQLite (dev) |
| Config | python-decouple |

## Como Rodar Localmente

**Pré-requisitos:** Python 3.8+, chave de API da OpenAI

```bash
# 1. Clone o repositório
git clone https://github.com/renatoteodoro/hakaton2025.git
cd hakaton2025

# 2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate   # Linux/Mac

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite .env e adicione sua OPENAI_API_KEY e SECRET_KEY

# 5. Execute as migrações
python manage.py migrate

# 6. Inicie o servidor
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000/`

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz:

```env
SECRET_KEY=sua-secret-key-segura-aqui
OPENAI_API_KEY=sk-...
DEBUG=True
```

## Estrutura do Projeto

```
hakaton2025/
├── app/           # Configurações Django
├── core/          # App principal (reuniões, transcrições, atas)
├── templates/     # Templates HTML
├── media/         # Uploads de áudio
└── manage.py
```

---

> Projeto desenvolvido no Hackaton 2025 — Programa Jovem Programador — Senac/SC
