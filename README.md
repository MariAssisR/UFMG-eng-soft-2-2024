# UFMG-eng-soft-2-2024
## Membros do grupo:
- Gabriel Henrique Gonçalves Santos
- Gabriel Oliveira Sant'Ana
- Mariana Assis Ramos

## Explicação do sistema:
Um sistema simples para gerenciar tarefas do dia a dia, permitindo:
- Adicionar e remover tarefas.
- Marcar tarefas como concluídas.
- Listar tarefas pendentes e concluídas.
- Salvar e carregar tarefas em JSON.
- Adicionar categorias e prazos.

## Explicação de tecnologias usadas:
- Python (Flask)
- Testes unitários com pytest
- CI/CD com GitHub Actions

## Como Usar:
1. Clone o repositório.
2. Instale as dependências
    - python3 -m venv venv
    - source venv/bin/activate  # No Windows: venv\Scripts\activate
    - pip install -r requirements.txt
3. Configurar arquivo '.env' com as seguintes configurações:
    - FLASK_ENV=development
    - SECRET_KEY=uma_chave_segura_aleatória
4. Executar
    - python run.py

