import streamlit as st
import pandas as pd
from database import (
    inserir_turma, consultar_turmas, consultar_turma_por_id, 
    atualizar_turma, deletar_turma, consultar_professores, conectar_db,
    atribuir_professor_turma
)

def consultar_turma_por_codigo(codigo):
    turmas = consultar_turmas()
    return next((t for t in turmas if t[2] == codigo), None)

def consultar_professor_por_turma(turma_id):
    profs = consultar_professores()
    return next((p for p in profs if p[5] == turma_id), None)

def render(submenu):
    if submenu == "Cadastrar":
        cadastrar()
    elif submenu == "Consultar":
        consultar()
    elif submenu == "Modificar":
        modificar()
    elif submenu == "Excluir":
        excluir()

def cadastrar():
    st.header("Cadastrar Turma")
    with st.form("form_cad_turma"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome *", placeholder="Ex: 3º Ano A")
            codigo = st.text_input("Código *", placeholder="Ex: 3A-2025")
        with col2:
            turno = st.selectbox("Turno *", ["Matutino", "Vespertino", "Noturno"])
            ano = st.number_input("Ano *", min_value=2020, max_value=2030, value=2025, step=1)
        
        if st.form_submit_button("Cadastrar", use_container_width=True):
            if nome and codigo:
                sucesso, msg = inserir_turma(nome, codigo, turno, ano)
                st.success(msg) if sucesso else st.error(msg)
            else:
                st.error("Preencha os campos obrigatórios!")

def consultar():
    st.header("Consultar Turmas")
    tipo = st.radio("Tipo:", ["Todas", "Buscar por Código"])
    
    if tipo == "Todas":
        turmas = consultar_turmas()
        if turmas:
            dados = [[t[1], t[2], t[3], t[4], t[5]] for t in turmas]
            df = pd.DataFrame(dados, columns=["Nome", "Código", "Turno", "Ano", "Data Cadastro"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.info(f"Total: {len(turmas)} turmas")
        else:
            st.warning("Nenhuma turma cadastrada.")
    else:
        cod = st.text_input("Digite o código:", placeholder="Ex: 3A-2025")
        if st.button("Buscar"):
            if cod:
                turma = consultar_turma_por_codigo(cod)
                if turma:
                    st.success("Turma encontrada!")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Nome:** {turma[1]}\n**Código:** {turma[2]}\n**Turno:** {turma[3]}")
                    with col2:
                        st.write(f"**Ano:** {turma[4]}\n**Data:** {turma[5]}")
                    
                    st.markdown("### Alunos e Professor")
                    conn = conectar_db()
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(DISTINCT a.id) FROM alunos a INNER JOIN aluno_turma at ON a.id = at.aluno_id WHERE at.turma_id = ?", (turma[0],))
                    total_alunos = cursor.fetchone()[0]
                    conn.close()
                    
                    prof = consultar_professor_por_turma(turma[0])
                    prof_nome = prof[1] if prof else "Sem professor"
                    st.write(f"**Professor:** {prof_nome}\n**Alunos:** {total_alunos}")
                    
                    # Opção para alterar professor
                    st.markdown("### Alterar Professor")
                    todos_profs = consultar_professores()
                    profs_disponiveis = [p for p in todos_profs if not p[5] or p[5] == turma[0]]
                    
                    if profs_disponiveis:
                        opts = ["Remover professor"] + [f"{p[2]} - {p[1]}" for p in profs_disponiveis]
                        prof_atual_idx = 0
                        if prof:
                            prof_atual_idx = next((i for i, p in enumerate(profs_disponiveis) if p[0] == prof[0]), 0) + 1
                        
                        novo_prof = st.selectbox("Professor:", opts, index=prof_atual_idx)
                        
                        if st.button("Atribuir Professor"):
                            prof_id = None
                            if novo_prof != "Remover professor":
                                prof_id = next(p[0] for p in profs_disponiveis if p[2] == novo_prof.split(" - ")[0])
                            sucesso, msg = atribuir_professor_turma(turma[0], prof_id)
                            if sucesso:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
                    else:
                        st.info("Nenhum professor disponível")
                else:
                    st.error("Turma não encontrada!")
            else:
                st.warning("Digite um código.")

def modificar():
    st.header("Modificar Turma")
    turmas = consultar_turmas()
    
    if turmas:
        turma_sel = st.selectbox("Selecione:", [f"{t[2]} - {t[1]}" for t in turmas])
        turma = consultar_turma_por_codigo(turma_sel.split(" - ")[0])
        
        if turma:
            st.markdown("### Dados Atuais")
            
            # Exibir professor atual
            prof = consultar_professor_por_turma(turma[0])
            if prof:
                st.info(f"👨‍🏫 Professor: {prof[1]} ({prof[2]})")
            else:
                st.warning("Sem professor atribuído")
            
            with st.form("form_mod_turma"):
                col1, col2 = st.columns(2)
                with col1:
                    novo_nome = st.text_input("Nome *", value=turma[1])
                    novo_turno = st.selectbox("Turno *", ["Matutino", "Vespertino", "Noturno"], 
                                            index=["Matutino", "Vespertino", "Noturno"].index(turma[3]))
                with col2:
                    st.text_input("Código", value=turma[2], disabled=True)
                    novo_ano = st.number_input("Ano *", min_value=2020, max_value=2030, value=int(turma[4]), step=1)
                
                st.info("Código não pode ser alterado.")
                
                if st.form_submit_button("Salvar", use_container_width=True):
                    if novo_nome:
                        sucesso, msg = atualizar_turma(turma[0], novo_nome, novo_turno, novo_ano)
                        if sucesso:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.error("Preencha os campos obrigatórios!")
            
            # Seção para modificar professor
            st.markdown("---")
            st.markdown("### Modificar Professor")
            todos_profs = consultar_professores()
            profs_disponiveis = [p for p in todos_profs if not p[5] or p[5] == turma[0]]
            
            if profs_disponiveis:
                opts = ["Remover professor"] + [f"{p[2]} - {p[1]}" for p in profs_disponiveis]
                prof_atual_idx = 0
                if prof:
                    prof_atual_idx = next((i for i, p in enumerate(profs_disponiveis) if p[0] == prof[0]), 0) + 1
                
                novo_prof = st.selectbox("Selecione o professor:", opts, index=prof_atual_idx)
                
                if st.button("Atribuir Professor", type="primary"):
                    prof_id = None
                    if novo_prof != "Remover professor":
                        prof_id = next(p[0] for p in profs_disponiveis if p[2] == novo_prof.split(" - ")[0])
                    sucesso, msg = atribuir_professor_turma(turma[0], prof_id)
                    if sucesso:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            else:
                st.info("Nenhum professor disponível")
    else:
        st.warning("Nenhuma turma cadastrada.")

def excluir():
    st.header("Excluir Turma")
    turmas = consultar_turmas()
    
    if turmas:
        turma_sel = st.selectbox("Selecione:", [f"{t[2]} - {t[1]}" for t in turmas])
        turma = consultar_turma_por_codigo(turma_sel.split(" - ")[0])
        
        if turma:
            st.markdown("### Dados")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Nome:** {turma[1]}\n**Código:** {turma[2]}")
            with col2:
                st.write(f"**Turno:** {turma[3]}\n**Ano:** {turma[4]}")
            
            st.warning("Ação irreversível!")
            if st.button("Confirmar Exclusão", type="primary"):
                sucesso, msg = deletar_turma(turma[0])
                if sucesso:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
    else:
        st.warning("Nenhuma turma cadastrada.")
