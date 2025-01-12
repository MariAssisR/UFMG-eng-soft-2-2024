# UFMG-eng-soft-2-2024 - Gerenciador de Tarefas
## Membros do grupo:
- Gabriel Henrique Gonçalves Santos
- Gabriel Oliveira Sant'Ana
- Mariana Assis Ramos

## Descrição do Sistema:
Este projeto consiste em um gerenciador de tarefas web (estilo "to-do list") desenvolvido em Python com o framework Flask. Ele oferece uma interface RESTful para realizar operações de criação, leitura, atualização e exclusão (CRUD) de tarefas, além de permitir o gerenciamento de categorias e prazos.

**Funcionalidades:**

*   Adicionar novas tarefas com descrição, categoria e prazo (deadline).
*   Listar todas as tarefas.
*   Listar tarefas filtradas por status de conclusão (pendentes e concluídas).
*   Editar tarefas existentes (descrição, categoria e prazo).
*   Marcar tarefas como concluídas.
*   Deletar tarefas.
*   Persistência de dados em banco de dados SQLite.

## Explicação de tecnologias usadas:
* **Python:** Linguagem de programação.
*   **Flask:** Microframework web para Python.
*   **Flask-SQLAlchemy:** Extensão do Flask para integração com o SQLAlchemy (ORM - Object-Relational Mapper), permitindo a interação com bancos de dados relacionais.
*   **SQLite:** Banco de dados relacional leve utilizado para desenvolvimento e testes.
*   **pytest:** Framework para testes em Python.
*   **GitHub Actions:** Plataforma de CI/CD para automação de testes e outros processos.


## Configuração e Execução:
1. **Clone o repositório.**

2. **Instale as dependências**
   
    ```bash
    python3 -m venv venv        # Cria o ambiente virtual
    source venv/bin/activate    # Ativa o ambiente (Linux/macOS)
    venv\Scripts\activate      # Ativa o ambiente (Windows)
    pip install -r requirements.txt
    ```

3. **Configurar arquivo '.env':**

Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:
    
    ```
    SECRET_KEY=uma_chave_segura_aleatoria # Gere uma chave aleatória forte
    FLASK_ENV=development
    ```

4. **Executar**
    
    ```bash
    python run.py
    ```
  
## Como rodar os testes
1. **Execute o comando**

    ```bash
    pytest tests/test_app.py
    ```
