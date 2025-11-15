import streamlit as st
import pandas as pd
from database import (
    inserir_aluno, consultar_alunos, consultar_aluno_por_matricula,
    atualizar_aluno, deletar_aluno, consultar_turmas
)

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
    st.header("Cadastrar Aluno")
    with st.form("form_cad_aluno"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome *", placeholder="Ex: Maria Santos")
            matricula = st.text_input("Matrícula *", placeholder="Ex: 20231234")
            curso = st.text_input("Curso *", placeholder="Ex: Eng. Software")
        with col2:
            email = st.text_input("E-mail *", placeholder="Ex: maria@email.com")
            telefone = st.text_input("Telefone", placeholder="Ex: (11) 98765-4321")
            turmas = consultar_turmas()
            if turmas:
                opts = [f"{t[2]} - {t[1]}" for t in turmas]
                turmas_sel = st.multiselect("Turmas", opts)
            else:
                st.warning("Nenhuma turma cadastrada!")
                turmas_sel = []
        
        if st.form_submit_button("Cadastrar", use_container_width=True):
            if nome and matricula and curso and email:
                turma_ids = [next(t[0] for t in turmas if t[2] == ts.split(" - ")[0]) for ts in turmas_sel] if turmas_sel else []
                sucesso, msg = inserir_aluno(nome, matricula, curso, email, telefone, turma_ids)
                st.success(msg) if sucesso else st.error(msg)
            else:
                st.error("Preencha os campos obrigatórios!")

def consultar():
    st.header("Consultar Alunos")
    tipo = st.radio("Tipo:", ["Todos", "Buscar por Matrícula"])
    
    if tipo == "Todos":
        alunos = consultar_alunos()
        if alunos:
            dados = [[a[1], a[2], a[3], a[4], a[5] or "N/A", a[6] or "Sem turma", a[7]] for a in alunos]
            df = pd.DataFrame(dados, columns=["Nome", "Matrícula", "Curso", "E-mail", "Telefone", "Turmas", "Data Cadastro"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.info(f"Total: {len(alunos)} alunos")
        else:
            st.warning("Nenhum aluno cadastrado.")
    else:
        mat = st.text_input("Digite a matrícula:", placeholder="Ex: 20231234")
        if st.button("Buscar"):
            if mat:
                resultado = consultar_aluno_por_matricula(mat)
                if resultado:
                    aluno, turmas_aluno = resultado
                    st.success("Aluno encontrado!")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Nome:** {aluno[1]}\n**Matrícula:** {aluno[2]}\n**Curso:** {aluno[3]}\n**E-mail:** {aluno[4]}")
                    with col2:
                        turmas_info = ", ".join([f"{t[2]} ({t[1]})" for t in turmas_aluno]) if turmas_aluno else "Sem turma"
                        st.write(f"**Telefone:** {aluno[5] or 'N/A'}\n**Turmas:** {turmas_info}\n**Data:** {aluno[6]}")
                else:
                    st.error("Aluno não encontrado!")
            else:
                st.warning("Digite uma matrícula.")

def modificar():
    st.header("Modificar Aluno")
    alunos = consultar_alunos()
    
    if alunos:
        aluno_sel = st.selectbox("Selecione:", [f"{a[2]} - {a[1]}" for a in alunos])
        resultado = consultar_aluno_por_matricula(aluno_sel.split(" - ")[0])
        
        if resultado:
            aluno, turmas_atuais = resultado
            st.markdown("### Dados Atuais")
            with st.form("form_mod_aluno"):
                col1, col2 = st.columns(2)
                with col1:
                    novo_nome = st.text_input("Nome *", value=aluno[1])
                    novo_curso = st.text_input("Curso *", value=aluno[3])
                    novo_email = st.text_input("E-mail *", value=aluno[4])
                with col2:
                    st.text_input("Matrícula", value=aluno[2], disabled=True)
                    novo_tel = st.text_input("Telefone", value=aluno[5] or "")
                    turmas = consultar_turmas()
                    opts = [f"{t[2]} - {t[1]}" for t in turmas]
                    default = [f"{t[2]} - {t[1]}" for t in turmas_atuais]
                    novas_turmas = st.multiselect("Turmas", opts, default=default)
                
                st.info("Matrícula não pode ser alterada.")
                
                if st.form_submit_button("Salvar", use_container_width=True):
                    if novo_nome and novo_curso and novo_email:
                        turma_ids = [next(t[0] for t in turmas if t[2] == nt.split(" - ")[0]) for nt in novas_turmas] if novas_turmas else []
                        sucesso, msg = atualizar_aluno(aluno[0], novo_nome, novo_curso, novo_email, novo_tel, turma_ids)
                        if sucesso:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.error("Preencha os campos obrigatórios!")
    else:
        st.warning("Nenhum aluno cadastrado.")

def excluir():
    st.header("Excluir Aluno")
    alunos = consultar_alunos()
    
    if alunos:
        aluno_sel = st.selectbox("Selecione:", [f"{a[2]} - {a[1]}" for a in alunos])
        resultado = consultar_aluno_por_matricula(aluno_sel.split(" - ")[0])
        
        if resultado:
            aluno, turmas_aluno = resultado
            st.markdown("### Dados")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Nome:** {aluno[1]}\n**Matrícula:** {aluno[2]}\n**Curso:** {aluno[3]}")
            with col2:
                turmas_info = ", ".join([f"{t[2]} ({t[1]})" for t in turmas_aluno]) if turmas_aluno else "Sem turma"
                st.write(f"**E-mail:** {aluno[4]}\n**Telefone:** {aluno[5] or 'N/A'}\n**Turmas:** {turmas_info}")
            
            st.warning("Ação irreversível!")
            if st.button("Confirmar Exclusão", type="primary"):
                sucesso, msg = deletar_aluno(aluno[0])
                if sucesso:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
    else:
        st.warning("Nenhum aluno cadastrado.")
