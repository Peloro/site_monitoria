import sqlite3
from datetime import datetime

def init_db():
    """Inicializa o banco de dados e cria as tabelas se não existirem"""
    conn = sqlite3.connect('monitoria.db')
    cursor = conn.cursor()
    
    # Tabela de Turmas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            codigo TEXT UNIQUE NOT NULL,
            periodo TEXT NOT NULL,
            sala TEXT,
            data_cadastro TEXT NOT NULL
        )
    ''')
    
    # Tabela de Professores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS professores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            matricula TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT,
            turma_id INTEGER,
            data_cadastro TEXT NOT NULL,
            FOREIGN KEY (turma_id) REFERENCES turmas(id) ON DELETE SET NULL
        )
    ''')
    
    # Tabela de Alunos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            matricula TEXT UNIQUE NOT NULL,
            curso TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT,
            turma_id INTEGER,
            data_cadastro TEXT NOT NULL,
            FOREIGN KEY (turma_id) REFERENCES turmas(id) ON DELETE SET NULL
        )
    ''')
    
    conn.commit()
    conn.close()

# ==================== FUNÇÕES DE TURMAS ====================

def inserir_turma(nome, codigo, periodo, sala):
    """Insere uma nova turma no banco de dados"""
    try:
        conn = sqlite3.connect('monitoria.db')
        cursor = conn.cursor()
        data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO turmas (nome, codigo, periodo, sala, data_cadastro)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, codigo, periodo, sala, data_cadastro))
        
        conn.commit()
        conn.close()
        return True, "Turma cadastrada com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Erro: Código de turma já cadastrado!"
    except Exception as e:
        return False, f"Erro ao cadastrar: {str(e)}"

def consultar_turmas():
    """Retorna todas as turmas cadastradas"""
    conn = sqlite3.connect('monitoria.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM turmas ORDER BY nome')
    turmas = cursor.fetchall()
    
    conn.close()
    return turmas

def consultar_turma_por_id(turma_id):
    """Consulta uma turma específica pelo ID"""
    conn = sqlite3.connect('monitoria.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM turmas WHERE id = ?', (turma_id,))
    turma = cursor.fetchone()
    
    conn.close()
    return turma

def atualizar_turma(id_turma, nome, periodo, sala):
    """Atualiza os dados de uma turma"""
    try:
        conn = sqlite3.connect('monitoria.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE turmas 
            SET nome = ?, periodo = ?, sala = ?
            WHERE id = ?
        ''', (nome, periodo, sala, id_turma))
        
        conn.commit()
        conn.close()
        return True, "Turma atualizada com sucesso!"
    except Exception as e:
        return False, f"Erro ao atualizar: {str(e)}"

def deletar_turma(id_turma):
    """Remove uma turma do banco de dados"""
    try:
        conn = sqlite3.connect('monitoria.db')
        cursor = conn.cursor()
        
        # Verifica se há alunos ou professores vinculados
        cursor.execute('SELECT COUNT(*) FROM alunos WHERE turma_id = ?', (id_turma,))
        count_alunos = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM professores WHERE turma_id = ?', (id_turma,))
        count_professores = cursor.fetchone()[0]
        
        if count_alunos > 0 or count_professores > 0:
            conn.close()
            return False, f"Não é possível excluir! Há {count_alunos} aluno(s) e {count_professores} professor(es) vinculado(s) a esta turma."
        
        cursor.execute('DELETE FROM turmas WHERE id = ?', (id_turma,))
        
        conn.commit()
        conn.close()
        return True, "Turma removida com sucesso!"
    except Exception as e:
        return False, f"Erro ao remover: {str(e)}"

# ==================== FUNÇÕES DE PROFESSORES ====================

def inserir_professor(nome, matricula, email, telefone, turma_id):
    """Insere um novo professor no banco de dados"""
    try:
        conn = sqlite3.connect('monitoria.db')
        cursor = conn.cursor()
        
        # Verifica se já existe um professor nesta turma
        if turma_id:
            cursor.execute('SELECT COUNT(*) FROM professores WHERE turma_id = ?', (turma_id,))
            count = cursor.fetchone()[0]
            if count > 0:
                conn.close()
                return False, "Erro: Esta turma já possui um professor!"
        
        data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO professores (nome, matricula, email, telefone, turma_id, data_cadastro)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, matricula, email, telefone, turma_id, data_cadastro))
        
        conn.commit()
        conn.close()
        return True, "Professor cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Erro: Matrícula já cadastrada!"
    except Exception as e:
        return False, f"Erro ao cadastrar: {str(e)}"

def consultar_professores():
    """Retorna todos os professores cadastrados com suas turmas"""
    conn = sqlite3.connect('monitoria.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.*, t.nome as turma_nome, t.codigo as turma_codigo
        FROM professores p
        LEFT JOIN turmas t ON p.turma_id = t.id
        ORDER BY p.nome
    ''')
    professores = cursor.fetchall()
    
    conn.close()
    return professores

def consultar_professor_por_id(professor_id):
    """Consulta um professor específico pelo ID"""
    conn = sqlite3.connect('monitoria.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.*, t.nome as turma_nome, t.codigo as turma_codigo
        FROM professores p
        LEFT JOIN turmas t ON p.turma_id = t.id
        WHERE p.id = ?
    ''', (professor_id,))
    professor = cursor.fetchone()
    
    conn.close()
    return professor

def atualizar_professor(id_professor, nome, email, telefone, turma_id):
    """Atualiza os dados de um professor"""
    try:
        conn = sqlite3.connect('monitoria.db')
        cursor = conn.cursor()
        
        # Verifica se já existe um professor nesta turma (exceto o professor atual)
        if turma_id:
            cursor.execute('SELECT COUNT(*) FROM professores WHERE turma_id = ? AND id != ?', 
                         (turma_id, id_professor))
            count = cursor.fetchone()[0]
            if count > 0:
                conn.close()
                return False, "Erro: Esta turma já possui um professor!"
        
        cursor.execute('''
            UPDATE professores 
            SET nome = ?, email = ?, telefone = ?, turma_id = ?
            WHERE id = ?
        ''', (nome, email, telefone, turma_id, id_professor))
        
        conn.commit()
        conn.close()
        return True, "Professor atualizado com sucesso!"
    except Exception as e:
        return False, f"Erro ao atualizar: {str(e)}"

def deletar_professor(id_professor):
    """Remove um professor do banco de dados"""
    try:
        conn = sqlite3.connect('monitoria.db')
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM professores WHERE id = ?', (id_professor,))
        
        conn.commit()
        conn.close()
        return True, "Professor removido com sucesso!"
    except Exception as e:
        return False, f"Erro ao remover: {str(e)}"

# ==================== FUNÇÕES DE ALUNOS ====================

def inserir_aluno(nome, matricula, curso, email, telefone, turma_id):
    """Insere um novo aluno no banco de dados"""
    try:
        conn = sqlite3.connect('monitoria.db')
        cursor = conn.cursor()
        data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO alunos (nome, matricula, curso, email, telefone, turma_id, data_cadastro)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nome, matricula, curso, email, telefone, turma_id, data_cadastro))
        
        conn.commit()
        conn.close()
        return True, "Aluno cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Erro: Matrícula já cadastrada!"
    except Exception as e:
        return False, f"Erro ao cadastrar: {str(e)}"

def consultar_alunos():
    """Retorna todos os alunos cadastrados com suas turmas"""
    conn = sqlite3.connect('monitoria.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT a.*, t.nome as turma_nome, t.codigo as turma_codigo
        FROM alunos a
        LEFT JOIN turmas t ON a.turma_id = t.id
        ORDER BY a.nome
    ''')
    alunos = cursor.fetchall()
    
    conn.close()
    return alunos

def consultar_aluno_por_matricula(matricula):
    """Consulta um aluno específico pela matrícula"""
    conn = sqlite3.connect('monitoria.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT a.*, t.nome as turma_nome, t.codigo as turma_codigo
        FROM alunos a
        LEFT JOIN turmas t ON a.turma_id = t.id
        WHERE a.matricula = ?
    ''', (matricula,))
    aluno = cursor.fetchone()
    
    conn.close()
    return aluno

def consultar_aluno_por_id(aluno_id):
    """Consulta um aluno específico pelo ID"""
    conn = sqlite3.connect('monitoria.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT a.*, t.nome as turma_nome, t.codigo as turma_codigo
        FROM alunos a
        LEFT JOIN turmas t ON a.turma_id = t.id
        WHERE a.id = ?
    ''', (aluno_id,))
    aluno = cursor.fetchone()
    
    conn.close()
    return aluno

def atualizar_aluno(id_aluno, nome, curso, email, telefone, turma_id):
    """Atualiza os dados de um aluno"""
    try:
        conn = sqlite3.connect('monitoria.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE alunos 
            SET nome = ?, curso = ?, email = ?, telefone = ?, turma_id = ?
            WHERE id = ?
        ''', (nome, curso, email, telefone, turma_id, id_aluno))
        
        conn.commit()
        conn.close()
        return True, "Dados atualizados com sucesso!"
    except Exception as e:
        return False, f"Erro ao atualizar: {str(e)}"

def deletar_aluno(id_aluno):
    """Remove um aluno do banco de dados"""
    try:
        conn = sqlite3.connect('monitoria.db')
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM alunos WHERE id = ?', (id_aluno,))
        
        conn.commit()
        conn.close()
        return True, "Aluno removido com sucesso!"
    except Exception as e:
        return False, f"Erro ao remover: {str(e)}"
