# Sistema de Gerenciamento de Monitoria

Sistema web completo desenvolvido com Streamlit para gerenciar turmas, professores e alunos em programas de monitoria.

## 📋 Funcionalidades

### 👥 Gestão de Turmas
- ➕ **Cadastrar Turmas**: Crie turmas com nome, código, período e sala
- 🔍 **Consultar Turmas**: Visualize todas as turmas e seus detalhes (professores e alunos)
- ✏️ **Modificar Turmas**: Atualize informações de turmas existentes
- 🗑️ **Excluir Turmas**: Remova turmas do sistema (apenas se não houver alunos ou professores vinculados)

### 👨‍🏫 Gestão de Professores
- ➕ **Cadastrar Professores**: Adicione professores e atribua a uma turma
- 🔍 **Consultar Professores**: Visualize todos os professores e suas turmas
- ✏️ **Modificar Professores**: Atualize dados e reatribua turmas
- 🗑️ **Excluir Professores**: Remova professores do sistema
- ⚠️ **Regra**: Cada professor pode estar em apenas UMA turma, e cada turma pode ter apenas UM professor

### 👨‍🎓 Gestão de Alunos
- ➕ **Cadastrar Alunos**: Adicione alunos e designe-os a turmas
- 🔍 **Consultar Alunos**: Visualize todos os alunos ou busque por matrícula
- ✏️ **Modificar Alunos**: Atualize informações e mude de turma
- 🗑️ **Excluir Alunos**: Remova alunos do sistema

## 🚀 Como Executar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o aplicativo:
```bash
streamlit run app.py
```

3. O aplicativo abrirá automaticamente no navegador em `http://localhost:8501`

## 💾 Banco de Dados

O sistema utiliza SQLite com três tabelas relacionadas:
- **turmas**: Armazena informações das turmas
- **professores**: Armazena dados dos professores (com chave estrangeira para turmas)
- **alunos**: Armazena dados dos alunos (com chave estrangeira para turmas)

O arquivo `monitoria.db` será criado automaticamente na primeira execução.

## 📁 Estrutura do Projeto

```
site_monitoria/
├── app.py              # Aplicação principal Streamlit
├── database.py         # Funções de banco de dados
├── requirements.txt    # Dependências do projeto
└── README.md          # Este arquivo
```

## 📊 Modelo de Dados

### Turma
- Nome, Código (único), Período, Sala, Data de cadastro

### Professor
- Nome, Matrícula (único), E-mail, Telefone, Turma (FK), Data de cadastro
- **Relacionamento**: 1:1 com Turma (um professor por turma)

### Aluno
- Nome, Matrícula (único), Curso, E-mail, Telefone, Turma (FK), Data de cadastro
- **Relacionamento**: N:1 com Turma (vários alunos por turma)

## 🛠️ Tecnologias

- Python 3.x
- Streamlit
- SQLite3
- Pandas

## ℹ️ Regras de Negócio

1. Cada turma pode ter **apenas um professor**
2. Cada professor pode estar em **apenas uma turma**
3. Cada aluno pode estar em **apenas uma turma**
4. Uma turma pode ter **vários alunos**
5. Turmas só podem ser excluídas se não houver alunos ou professores vinculados
6. Matrícula e código de turma são únicos e não podem ser alterados após cadastro
