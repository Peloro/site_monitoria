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
    
    alunos = consultar_alunos()
    
    if alunos:
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            busca = st.text_input("🔍 Pesquisar", placeholder="Nome, matrícula ou email...")
        with col2:
            turmas_disponiveis = consultar_turmas()
            turma_filtro = st.selectbox("Turma", ["Todas"] + [f"{t[2]} - {t[1]}" for t in turmas_disponiveis])
        with col3:
            cursos = sorted(list(set([a[3] for a in alunos])))
            curso_filtro = st.selectbox("Curso", ["Todos"] + cursos)
        
        # Aplicar filtros
        alunos_filtrados = alunos
        
        if busca:
            alunos_filtrados = [a for a in alunos_filtrados if 
                              busca.lower() in a[1].lower() or 
                              busca.lower() in a[2].lower() or 
                              busca.lower() in a[4].lower()]
        
        if turma_filtro != "Todas":
            turma_codigo = turma_filtro.split(" - ")[0]
            alunos_filtrados = [a for a in alunos_filtrados if turma_codigo in (a[6] or "")]
        
        if curso_filtro != "Todos":
            alunos_filtrados = [a for a in alunos_filtrados if a[3] == curso_filtro]
        
        if alunos_filtrados:
            dados = [[a[1], a[2], a[3], a[4], a[5] or "N/A", a[6] or "Sem turma", a[7]] for a in alunos_filtrados]
            df = pd.DataFrame(dados, columns=["Nome", "Matrícula", "Curso", "E-mail", "Telefone", "Turmas", "Data Cadastro"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.info(f"Mostrando {len(alunos_filtrados)} de {len(alunos)} alunos")
            
            # Detalhes de aluno selecionado
            st.markdown("---")
            st.markdown("### Detalhes do Aluno")
            aluno_sel = st.selectbox("Selecione para ver detalhes:", 
                                    [f"{a[2]} - {a[1]}" for a in alunos_filtrados])
            
            if aluno_sel:
                mat = aluno_sel.split(" - ")[0]
                resultado = consultar_aluno_por_matricula(mat)
                
                if resultado:
                    aluno, turmas_aluno = resultado
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Nome:** {aluno[1]}")
                        st.write(f"**Matrícula:** {aluno[2]}")
                        st.write(f"**Curso:** {aluno[3]}")
                        st.write(f"**E-mail:** {aluno[4]}")
                    with col2:
                        st.write(f"**Telefone:** {aluno[5] or 'N/A'}")
                        turmas_info = ", ".join([f"{t[2]} ({t[1]})" for t in turmas_aluno]) if turmas_aluno else "Sem turma"
                        st.write(f"**Turmas:** {turmas_info}")
                        st.write(f"**Data:** {aluno[6]}")
        else:
            st.warning("Nenhum aluno encontrado com os filtros aplicados.")
    else:
        st.warning("Nenhum aluno cadastrado.")

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
                st.write(f"**Nome:** {aluno[1]}")
                st.write(f"**Matrícula:** {aluno[2]}")
                st.write(f"**Curso:** {aluno[3]}")
            with col2:
                st.write(f"**E-mail:** {aluno[4]}")
                st.write(f"**Telefone:** {aluno[5] or 'N/A'}")
                turmas_info = ", ".join([f"{t[2]} ({t[1]})" for t in turmas_aluno]) if turmas_aluno else "Sem turma"
                st.write(f"**Turmas:** {turmas_info}")
            
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
