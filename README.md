# Sistema de Monitoria

Sistema web para gerenciamento de turmas, professores e alunos.

## 📁 Estrutura do Projeto

```
site_monitoria/
├── app.py                 # Aplicação principal
├── database.py            # Funções do banco de dados
├── requirements.txt       # Dependências
├── config/
│   ├── __init__.py
│   └── styles.py         # Estilos CSS customizados
└── modules/
    ├── __init__.py
    ├── turmas.py         # Módulo de turmas
    ├── professores.py    # Módulo de professores
    └── alunos.py         # Módulo de alunos
```

## 🎯 Funcionalidades

- **Turmas**: Cadastrar, consultar, modificar e excluir turmas
- **Professores**: Gerenciar professores (1 professor por turma)
- **Alunos**: Gerenciar alunos (podem estar em múltiplas turmas)

## 🔗 Relacionamentos

- **Aluno ↔ Turma**: Many-to-Many (um aluno pode estar em várias turmas)
- **Professor ↔ Turma**: One-to-One (um professor leciona em apenas uma turma)

## 💾 Banco de Dados

SQLite com 4 tabelas:
- `turmas`: Informações das turmas
- `professores`: Dados dos professores
- `alunos`: Dados dos alunos
- `aluno_turma`: Tabela de junção (many-to-many)

## 🚀 Instalação e Execução

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

## 🛠️ Tecnologias

- Python 3.12
- Streamlit 1.31.0
- SQLite3
- Pandas 2.1.4
