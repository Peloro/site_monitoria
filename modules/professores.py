import streamlit as st
import pandas as pd
from database import (
    inserir_professor, consultar_professores, consultar_professor_por_id,
    atualizar_professor, deletar_professor, consultar_turmas, consultar_turma_por_id
)

def consultar_professor_por_cpf(matricula):
    profs = consultar_professores()
    return next((p for p in profs if p[2] == matricula), None)

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
    st.header("Cadastrar Professor")
    with st.form("form_cad_prof"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome *", placeholder="Ex: João Silva")
            matricula = st.text_input("Matrícula *", placeholder="Ex: PROF001")
            email = st.text_input("E-mail *", placeholder="Ex: joao@email.com")
        with col2:
            tel = st.text_input("Telefone", placeholder="Ex: (11) 98765-4321")
            turmas = consultar_turmas()
            if turmas:
                opts = ["Nenhuma"] + [f"{t[2]} - {t[1]}" for t in turmas]
                turma_sel = st.selectbox("Turma", opts)
            else:
                st.warning("Nenhuma turma cadastrada!")
                turma_sel = "Nenhuma"
        
        if st.form_submit_button("Cadastrar", use_container_width=True):
            if nome and matricula and email:
                turma_id = None
                if turma_sel != "Nenhuma":
                    turma_id = next(t[0] for t in turmas if t[2] == turma_sel.split(" - ")[0])
                sucesso, msg = inserir_professor(nome, matricula, email, tel, turma_id)
                st.success(msg) if sucesso else st.error(msg)
            else:
                st.error("Preencha os campos obrigatórios!")

def consultar():
    st.header("Consultar Professores")
    tipo = st.radio("Tipo:", ["Todos", "Buscar por Matrícula"])
    
    if tipo == "Todos":
        profs = consultar_professores()
        if profs:
            dados = [[p[1], p[2], p[3], p[4] or "N/A",
                     f"{p[8]} ({p[7]})" if p[7] else "Sem turma", p[6]] for p in profs]
            df = pd.DataFrame(dados, columns=["Nome", "Matrícula", "E-mail", "Telefone", "Turma", "Data Cadastro"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.info(f"Total: {len(profs)} professores")
        else:
            st.warning("Nenhum professor cadastrado.")
    else:
        mat = st.text_input("Digite a matrícula:", placeholder="Ex: PROF001")
        if st.button("Buscar"):
            if mat:
                prof = consultar_professor_por_cpf(mat)
                if prof:
                    st.success("Professor encontrado!")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Nome:** {prof[1]}\n**Matrícula:** {prof[2]}\n**E-mail:** {prof[3]}")
                    with col2:
                        turma_info = f"{prof[8]} ({prof[7]})" if prof[7] else "Sem turma"
                        st.write(f"**Telefone:** {prof[4] or 'N/A'}\n**Turma:** {turma_info}\n**Data:** {prof[6]}")
                else:
                    st.error("Professor não encontrado!")
            else:
                st.warning("Digite uma matrícula.")

def modificar():
    st.header("Modificar Professor")
    profs = consultar_professores()
    
    if profs:
        prof_sel = st.selectbox("Selecione:", [f"{p[2]} - {p[1]}" for p in profs])
        prof = consultar_professor_por_cpf(prof_sel.split(" - ")[0])
        
        if prof:
            st.markdown("### Dados Atuais")
            with st.form("form_mod_prof"):
                col1, col2 = st.columns(2)
                with col1:
                    novo_nome = st.text_input("Nome *", value=prof[1])
                    novo_email = st.text_input("E-mail *", value=prof[3])
                with col2:
                    st.text_input("Matrícula", value=prof[2], disabled=True)
                    novo_tel = st.text_input("Telefone", value=prof[4] or "")
                
                turmas = consultar_turmas()
                opts = ["Nenhuma"] + [f"{t[2]} - {t[1]}" for t in turmas]
                
                idx = 0
                if prof[5]:
                    turma_atual = consultar_turma_por_id(prof[5])
                    if turma_atual:
                        idx = next((i for i, opt in enumerate(opts) if turma_atual[2] in opt), 0)
                
                nova_turma = st.selectbox("Turma", opts, index=idx)
                
                st.info("Matrícula não pode ser alterada.")
                
                if st.form_submit_button("Salvar", use_container_width=True):
                    if novo_nome and novo_email:
                        turma_id = None
                        if nova_turma != "Nenhuma":
                            turma_id = next(t[0] for t in turmas if t[2] == nova_turma.split(" - ")[0])
                        sucesso, msg = atualizar_professor(prof[0], novo_nome, novo_email, novo_tel, turma_id)
                        if sucesso:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.error("Preencha os campos obrigatórios!")
    else:
        st.warning("Nenhum professor cadastrado.")

def excluir():
    st.header("Excluir Professor")
    profs = consultar_professores()
    
    if profs:
        prof_sel = st.selectbox("Selecione:", [f"{p[2]} - {p[1]}" for p in profs])
        prof = consultar_professor_por_cpf(prof_sel.split(" - ")[0])
        
        if prof:
            st.markdown("### Dados")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Nome:** {prof[1]}\n**Matrícula:** {prof[2]}\n**E-mail:** {prof[3]}")
            with col2:
                turma_info = f"{prof[8]} ({prof[7]})" if prof[7] else "Sem turma"
                st.write(f"**Telefone:** {prof[4] or 'N/A'}\n**Turma:** {turma_info}")
            
            st.warning("Ação irreversível!")
            if st.button("Confirmar Exclusão", type="primary"):
                sucesso, msg = deletar_professor(prof[0])
                if sucesso:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
    else:
        st.warning("Nenhum professor cadastrado.")
