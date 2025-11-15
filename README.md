# Tutoring Management System

- Web system for managing classes, teachers, and students.
- Created as final project for Women's Programming School - 2025

## 📁 Project Structure

```
site_monitoria/
├── app.py                # Main application
├── database.py           # Database functions
├── requirements.txt      # Dependencies
├── config/
│   ├── __init__.py
│   └── styles.py         # Custom CSS styles
└── modules/
    ├── __init__.py
    ├── turmas.py         # Classes module
    ├── professores.py    # Teachers module
    └── alunos.py         # Students module
```

## 🎯 Features

- **Classes**: Create, read, update, and delete classes
- **Teachers**: Manage teachers (1 teacher per class)
- **Students**: Manage students (can be enrolled in multiple classes)

## 🔗 Relationships

- **Student ↔ Class**: Many-to-Many (a student can be in multiple classes)
- **Teacher ↔ Class**: One-to-One (a teacher teaches only one class)

## 💾 Database

SQLite with 4 tables:
- `turmas`: Class information
- `professores`: Teacher data
- `alunos`: Student data
- `aluno_turma`: Junction table (many-to-many)

## 🚀 Installation and Execution

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

## 🛠️ Technologies

- Python 3.12
- Streamlit 1.31.0
- SQLite3
- Pandas 2.1.4
