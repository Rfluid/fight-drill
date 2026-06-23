# FightDrill

Plataforma web de treinamento para artes marciais e esportes de combate.
Oferece modalidades de treino assistido por computador com estímulos sonoros, controle de tempo e gerenciamento de combinações de técnicas.

Desenvolvido como projeto da disciplina de Engenharia de Software I — UFSC, 2025/1.

## Stack

- **Python 3.12** com **PyScript** (execução no navegador via WebAssembly)
- HTML + CSS (sem framework frontend)
- Sem backend — toda persistência via `localStorage`

## Estrutura do projeto

```
index.html             # Página principal (PyScript + CSS)
pyscript.toml          # Configuração PyScript
src/
  main.py              # Entry point (bootstrap da aplicação)
  domain/              # Modelo de domínio (classes de negócio)
  audio/               # Motor de áudio (Web Audio API + Speech Synthesis)
  persistence/         # Camada de persistência (localStorage)
  session/             # Lógica de execução dos treinos (state machines)
  ui/                  # Interface do usuário (Router, Pages, DrillTimer)
    pages/             # Páginas da aplicação (Home, Drills, CRUD)
tests/                 # Testes unitários (pytest)
docs/                  # Documentação e plano de implementação
statement/             # Enunciado do projeto
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

## Comandos (via Make)

```bash
make help         # Mostra todos os targets disponíveis
make test         # Executa todos os testes
make test-v       # Executa testes com saída detalhada
make test-k K=combo  # Executa testes que correspondem ao padrão
make clean        # Remove venv e caches
```

## Gerenciamento de dependências

```bash
# Adicionar pacote: editar requirements.in, depois:
pip-compile requirements.in -o requirements.txt
pip install -r requirements.txt
```

## Compilar relatórios

```bash
pandoc entrega1.md -o entrega1.pdf --pdf-engine=xelatex --citeproc
```

## Autores

- Pedro Artur de Aguiar Cabral
- Ruy Agostinho Otoni Vieira Neto
- Vitor Pedrosa Brito dos Santos
