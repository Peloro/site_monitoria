import streamlit as st
import pandas as pd
from database import (
    init_db, inserir_turma, consultar_turmas, consultar_turma_por_id, 
    atualizar_turma, deletar_turma, inserir_professor, consultar_professores, 
    consultar_professor_por_id, atualizar_professor, deletar_professor,
    inserir_aluno, consultar_alunos, consultar_aluno_por_id,
    consultar_aluno_por_matricula, atualizar_aluno, deletar_aluno
)

st.set_page_config(page_title="Sistema de Monitoria", page_icon="📚", layout="wide")

st.markdown("""
<style>
    div[data-baseweb="select"] > div {
        user-select: none;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
    }
</style>
""", unsafe_allow_html=True)

init_db()

st.title("Sistema de Gerenciamento de Monitoria")
st.markdown("---")

menu = st.sidebar.selectbox("Menu Principal", ["Início", "Turmas", "Professores", "Alunos"])

if menu == "Início":
    st.header("Bem-vindo ao Sistema de Monitoria!")
    st.write("""**Funcionalidades:** Gerenciar Turmas, Professores e Alunos (cadastrar, consultar, modificar, excluir)
    
    Cada turma tem apenas um professor. Cada aluno é designado a uma turma.""")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Turmas Cadastradas", len(consultar_turmas()))
    with col2:
        st.metric("Professores", len(consultar_professores()))
    with col3:
        st.metric("Alunos", len(consultar_alunos()))

elif menu == "Turmas":
    submenu = st.sidebar.radio("Opções", ["Cadastrar", "Consultar", "Modificar", "Excluir"])
    
    if submenu == "Cadastrar":
        st.header("Cadastrar Nova Turma")
        with st.form("form_cad_turma"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome da Turma *", placeholder="Ex: Eng. Software 2025.1")
                codigo = st.text_input("Código *", placeholder="Ex: ES2025-1")
            with col2:
                periodo = st.text_input("Período *", placeholder="Ex: 2025.1 - Noturno")
                sala = st.text_input("Sala", placeholder="Ex: Sala 101")
            
            if st.form_submit_button("Cadastrar Turma", use_container_width=True):
                if nome and codigo and periodo:
                    sucesso, msg = inserir_turma(nome, codigo, periodo, sala)
                    st.success(msg) if sucesso else st.error(msg)
                else:
                    st.error("Preencha todos os campos obrigatórios!")
    
    elif submenu == "Consultar":
        st.header("Consultar Turmas")
        turmas = consultar_turmas()
        
        if turmas:
            df = pd.DataFrame(turmas, columns=["ID", "Nome", "Código", "Período", "Sala", "Data Cadastro"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.info(f"Total: {len(turmas)} turmas")
            
            st.markdown("### Detalhes por Turma")
            turma_sel = st.selectbox("Selecione:", [f"{t[2]} - {t[1]}" for t in turmas])
            
            if turma_sel:
                turma_id = next(t[0] for t in turmas if t[2] == turma_sel.split(" - ")[0])
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Professor")
                    prof = [p for p in consultar_professores() if p[5] == turma_id]
                    if prof:
                        st.write(f"**Nome:** {prof[0][1]}\n**E-mail:** {prof[0][3]}")
                    else:
                        st.write("Nenhum professor atribuído")
                
                with col2:
                    st.markdown("#### Alunos")
                    alunos_turma = [a for a in consultar_alunos() if a[6] == turma_id]
                    st.write(f"Total: {len(alunos_turma)} alunos")
                    for aluno in alunos_turma[:5]:
                        st.write(f"• {aluno[1]} ({aluno[2]})")
                    if len(alunos_turma) > 5:
                        st.write(f"... e mais {len(alunos_turma) - 5}")
        else:
            st.warning("Nenhuma turma cadastrada.")
    
    elif submenu == "Modificar":
        st.header("Modificar Turma")
        turmas = consultar_turmas()
        
        if turmas:
            turma_sel = st.selectbox("Selecione:", [f"{t[2]} - {t[1]}" for t in turmas])
            turma = next(t for t in turmas if t[2] == turma_sel.split(" - ")[0])
            
            if turma:
                st.markdown("### Dados Atuais")
                with st.form("form_mod_turma"):
                    col1, col2 = st.columns(2)
                    with col1:
                        novo_nome = st.text_input("Nome *", value=turma[1])
                        novo_periodo = st.text_input("Período *", value=turma[3])
                    with col2:
                        st.text_input("Código", value=turma[2], disabled=True)
                        nova_sala = st.text_input("Sala", value=turma[4] or "")
                    
                    st.info("O código não pode ser alterado.")
                    
                    if st.form_submit_button("Salvar", use_container_width=True):
                        if novo_nome and novo_periodo:
                            sucesso, msg = atualizar_turma(turma[0], novo_nome, novo_periodo, nova_sala)
                            if sucesso:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
                        else:
                            st.error("Preencha os campos obrigatórios!")
        else:
            st.warning("Nenhuma turma cadastrada.")
    
    elif submenu == "Excluir":
        st.header("Excluir Turma")
        turmas = consultar_turmas()
        
        if turmas:
            turma_sel = st.selectbox("Selecione:", [f"{t[2]} - {t[1]}" for t in turmas])
            turma = next(t for t in turmas if t[2] == turma_sel.split(" - ")[0])
            
            if turma:
                st.markdown("### Dados da Turma")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Nome:** {turma[1]}\n**Código:** {turma[2]}")
                with col2:
                    st.write(f"**Período:** {turma[3]}\n**Sala:** {turma[4]}")
                
                st.warning("Ação irreversível! Só pode excluir se não houver vínculos.")
                
                if st.button("Confirmar Exclusão", type="primary"):
                    sucesso, msg = deletar_turma(turma[0])
                    if sucesso:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
        else:
            st.warning("Nenhuma turma cadastrada.")

elif menu == "Professores":
    submenu = st.sidebar.radio("Opções", ["Cadastrar", "Consultar", "Modificar", "Excluir"])
    
    if submenu == "Cadastrar":
        st.header("Cadastrar Professor")
        with st.form("form_cad_prof"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome *", placeholder="Ex: Dr. João Silva")
                matricula = st.text_input("Matrícula *", placeholder="Ex: PROF001")
                email = st.text_input("E-mail *", placeholder="Ex: joao@email.com")
            with col2:
                telefone = st.text_input("Telefone", placeholder="Ex: (11) 98765-4321")
                turmas = consultar_turmas()
                turmas_com_prof = [p[5] for p in consultar_professores() if p[5]]
                turmas_disp = [t for t in turmas if t[0] not in turmas_com_prof]
                
                if turmas_disp:
                    opts = ["Nenhuma"] + [f"{t[2]} - {t[1]}" for t in turmas_disp]
                    turma_sel = st.selectbox("Turma", opts)
                else:
                    st.warning("Todas as turmas já têm professor!")
                    turma_sel = "Nenhuma"
            
            st.info("1 professor por turma, 1 turma por professor.")
            
            if st.form_submit_button("Cadastrar", use_container_width=True):
                if nome and matricula and email:
                    turma_id = None
                    if turma_sel != "Nenhuma":
                        turma_id = next(t[0] for t in turmas_disp if t[2] == turma_sel.split(" - ")[0])
                    sucesso, msg = inserir_professor(nome, matricula, email, telefone, turma_id)
                    st.success(msg) if sucesso else st.error(msg)
                else:
                    st.error("Preencha os campos obrigatórios!")
    
    elif submenu == "Consultar":
        st.header("Consultar Professores")
        profs = consultar_professores()
        
        if profs:
            dados = [[p[1], p[2], p[3], p[4] or "N/A", 
                     f"{p[8]} ({p[7]})" if p[7] else "Sem turma", p[6]] for p in profs]
            df = pd.DataFrame(dados, columns=["Nome", "Matrícula", "E-mail", "Telefone", "Turma", "Data Cadastro"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.info(f"Total: {len(profs)} professores")
        else:
            st.warning("Nenhum professor cadastrado.")
    
    elif submenu == "Modificar":
        st.header("Modificar Professor")
        profs = consultar_professores()
        
        if profs:
            prof_sel = st.selectbox("Selecione:", [f"{p[2]} - {p[1]}" for p in profs])
            prof = next(p for p in profs if p[2] == prof_sel.split(" - ")[0])
            
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
                    turmas_com_prof = [p[5] for p in profs if p[5] and p[0] != prof[0]]
                    turmas_disp = [t for t in turmas if t[0] not in turmas_com_prof]
                    opts = ["Nenhuma"] + [f"{t[2]} - {t[1]}" for t in turmas_disp]
                    
                    idx = 0
                    if prof[5]:
                        turma_atual = next((t for t in turmas if t[0] == prof[5]), None)
                        if turma_atual:
                            idx = next((i for i, opt in enumerate(opts) if turma_atual[2] in opt), 0)
                    
                    nova_turma = st.selectbox("Turma", opts, index=idx)
                    st.info("Matrícula não pode ser alterada.")
                    
                    if st.form_submit_button("Salvar", use_container_width=True):
                        if novo_nome and novo_email:
                            turma_id = None
                            if nova_turma != "Nenhuma":
                                turma_id = next(t[0] for t in turmas_disp if t[2] == nova_turma.split(" - ")[0])
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
    
    elif submenu == "Excluir":
        st.header("Excluir Professor")
        profs = consultar_professores()
        
        if profs:
            prof_sel = st.selectbox("Selecione:", [f"{p[2]} - {p[1]}" for p in profs])
            prof = next(p for p in profs if p[2] == prof_sel.split(" - ")[0])
            
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

elif menu == "Alunos":
    submenu = st.sidebar.radio("Opções", ["Cadastrar", "Consultar", "Modificar", "Excluir"])
    
    if submenu == "Cadastrar":
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
                    opts = ["Nenhuma"] + [f"{t[2]} - {t[1]}" for t in turmas]
                    turma_sel = st.selectbox("Turma", opts)
                else:
                    st.warning("Nenhuma turma cadastrada!")
                    turma_sel = "Nenhuma"
            
            if st.form_submit_button("Cadastrar", use_container_width=True):
                if nome and matricula and curso and email:
                    turma_id = None
                    if turma_sel != "Nenhuma":
                        turma_id = next(t[0] for t in turmas if t[2] == turma_sel.split(" - ")[0])
                    sucesso, msg = inserir_aluno(nome, matricula, curso, email, telefone, turma_id)
                    st.success(msg) if sucesso else st.error(msg)
                else:
                    st.error("Preencha os campos obrigatórios!")
    
    elif submenu == "Consultar":
        st.header("Consultar Alunos")
        tipo = st.radio("Tipo:", ["Todos", "Buscar por Matrícula"])
        
        if tipo == "Todos":
            alunos = consultar_alunos()
            if alunos:
                dados = [[a[1], a[2], a[3], a[4], a[5] or "N/A",
                         f"{a[8]} ({a[7]})" if a[7] else "Sem turma", a[6]] for a in alunos]
                df = pd.DataFrame(dados, columns=["Nome", "Matrícula", "Curso", "E-mail", "Telefone", "Turma", "Data Cadastro"])
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.info(f"Total: {len(alunos)} alunos")
            else:
                st.warning("Nenhum aluno cadastrado.")
        else:
            mat = st.text_input("Digite a matrícula:", placeholder="Ex: 20231234")
            if st.button("Buscar"):
                if mat:
                    aluno = consultar_aluno_por_matricula(mat)
                    if aluno:
                        st.success("Aluno encontrado!")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Nome:** {aluno[1]}\n**Matrícula:** {aluno[2]}\n**Curso:** {aluno[3]}\n**E-mail:** {aluno[4]}")
                        with col2:
                            turma_info = f"{aluno[8]} ({aluno[7]})" if aluno[7] else "Sem turma"
                            st.write(f"**Telefone:** {aluno[5] or 'N/A'}\n**Turma:** {turma_info}\n**Data:** {aluno[6]}")
                    else:
                        st.error("Aluno não encontrado!")
                else:
                    st.warning("Digite uma matrícula.")
    
    elif submenu == "Modificar":
        st.header("Modificar Aluno")
        alunos = consultar_alunos()
        
        if alunos:
            aluno_sel = st.selectbox("Selecione:", [f"{a[2]} - {a[1]}" for a in alunos])
            aluno = consultar_aluno_por_matricula(aluno_sel.split(" - ")[0])
            
            if aluno:
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
                        opts = ["Nenhuma"] + [f"{t[2]} - {t[1]}" for t in turmas]
                        
                        idx = 0
                        if aluno[6]:
                            turma_atual = consultar_turma_por_id(aluno[6])
                            if turma_atual:
                                idx = next((i for i, opt in enumerate(opts) if turma_atual[2] in opt), 0)
                        
                        nova_turma = st.selectbox("Turma", opts, index=idx)
                    
                    st.info("Matrícula não pode ser alterada.")
                    
                    if st.form_submit_button("Salvar", use_container_width=True):
                        if novo_nome and novo_curso and novo_email:
                            turma_id = None
                            if nova_turma != "Nenhuma":
                                turma_id = next(t[0] for t in turmas if t[2] == nova_turma.split(" - ")[0])
                            sucesso, msg = atualizar_aluno(aluno[0], novo_nome, novo_curso, novo_email, novo_tel, turma_id)
                            if sucesso:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
                        else:
                            st.error("Preencha os campos obrigatórios!")
        else:
            st.warning("Nenhum aluno cadastrado.")
    
    elif submenu == "Excluir":
        st.header("Excluir Aluno")
        alunos = consultar_alunos()
        
        if alunos:
            aluno_sel = st.selectbox("Selecione:", [f"{a[2]} - {a[1]}" for a in alunos])
            aluno = consultar_aluno_por_matricula(aluno_sel.split(" - ")[0])
            
            if aluno:
                st.markdown("### Dados")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Nome:** {aluno[1]}\n**Matrícula:** {aluno[2]}\n**Curso:** {aluno[3]}")
                with col2:
                    turma_info = f"{aluno[8]} ({aluno[7]})" if aluno[7] else "Sem turma"
                    st.write(f"**E-mail:** {aluno[4]}\n**Telefone:** {aluno[5] or 'N/A'}\n**Turma:** {turma_info}")
                
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

st.markdown("---")
st.markdown("Sistema de Monitoria © 2025")
