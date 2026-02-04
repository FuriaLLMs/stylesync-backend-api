# StyleSync Flask 🐍

Bem-vindo ao **StyleSync Flask**! Este é um projeto educativo desenvolvido para aprender e praticar o desenvolvimento backend com Python e Flask.

## 📋 Sobre o Projeto

Este repositório contém o código fonte da aplicação StyleSync, focada em boas práticas de desenvolvimento, estrutura de projeto organizada e testes automatizados.

### ✨ Funcionalidades Recentes

- **Formatação de Moeda**: Implementação de uma função utilitária `format_currency` para exibir valores monetários no padrão brasileiro (ex: `1.200,50`).
- **Padronização de Testes**: A estrutura de pastas foi reorganizada para seguir o padrão da comunidade Python, utilizando uma pasta `tests/` e configuração adequada de pacotes.

## 🚀 Como Rodar o Projeto

Pré-requisitos: Python 3.10+ instalado.

1.  **Clone o repositório** (se ainda não o fez):
    ```bash
    git clone https://github.com/FuriaLLMs/Aula01FlaskAlura.git
    cd Aula01FlaskAlura
    ```

2.  **Crie e ative um ambiente virtual** (recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # ou
    .\venv\Scripts\activate   # Windows
    ```

3.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação**:
    ```bash
    python run.py
    ```

## 🧪 Testes Automatizados

A qualidade do código é garantida através de testes automatizados com `pytest`.

Para rodar os testes, execute o seguinte comando na raiz do projeto:

```bash
pytest
```

> **Nota Didática**: A pasta de testes foi renomeada de `testes` para `tests`. Isso é uma convenção internacional em projetos Python. Manter o código em inglês (nomes de pastas, variáveis, funções) aumenta a legibilidade e a compatibilidade com ferramentas de CI/CD e IDEs.

## 📂 Estrutura do Projeto

```
stylesync_flask/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py       # Útil: Formatação de moeda
├── tests/             # Testes automatizados (Padrão de mercado)
│   ├── __init__.py
│   └── test_utils.py  # Testes da função de formatação
├── run.py
├── config.py
└── requirements.txt
```

---
Desenvolvido com 💙 durante o curso de Flask.
