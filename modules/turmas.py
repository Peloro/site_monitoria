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
                if sucesso:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.error("Preencha os campos obrigatórios!")

def consultar():
    st.header("Consultar Turmas")
    
    turmas = consultar_turmas()
    
    if turmas:
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            busca = st.text_input("🔍 Pesquisar", placeholder="Nome ou código...")
        with col2:
            turno_filtro = st.selectbox("Turno", ["Todos", "Matutino", "Vespertino", "Noturno"])
        with col3:
            ano_filtro = st.selectbox("Ano", ["Todos"] + sorted(list(set([str(t[4]) for t in turmas])), reverse=True))
        
        # Aplicar filtros
        turmas_filtradas = turmas
        
        if busca:
            turmas_filtradas = [t for t in turmas_filtradas if 
                              busca.lower() in t[1].lower() or busca.lower() in t[2].lower()]
        
        if turno_filtro != "Todos":
            turmas_filtradas = [t for t in turmas_filtradas if t[3] == turno_filtro]
        
        if ano_filtro != "Todos":
            turmas_filtradas = [t for t in turmas_filtradas if str(t[4]) == ano_filtro]
        
        if turmas_filtradas:
            dados = [[t[1], t[2], t[3], t[4], t[5]] for t in turmas_filtradas]
            df = pd.DataFrame(dados, columns=["Nome", "Código", "Turno", "Ano", "Data Cadastro"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.info(f"Mostrando {len(turmas_filtradas)} de {len(turmas)} turmas")
            
            # Detalhes de turma selecionada
            st.markdown("---")
            st.markdown("### Detalhes da Turma")
            turma_sel = st.selectbox("Selecione para ver detalhes:", 
                                    [f"{t[2]} - {t[1]}" for t in turmas_filtradas])
            
            if turma_sel:
                turma = next(t for t in turmas_filtradas if t[2] == turma_sel.split(" - ")[0])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Nome:** {turma[1]}")
                    st.write(f"**Código:** {turma[2]}")
                    st.write(f"**Turno:** {turma[3]}")
                with col2:
                    st.write(f"**Ano:** {turma[4]}")
                    st.write(f"**Data:** {turma[5]}")
                
                st.markdown("#### Alunos e Professor")
                conn = conectar_db()
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(DISTINCT a.id) FROM alunos a INNER JOIN aluno_turma at ON a.id = at.aluno_id WHERE at.turma_id = ?", (turma[0],))
                total_alunos = cursor.fetchone()[0]
                conn.close()
                
                prof = consultar_professor_por_turma(turma[0])
                prof_nome = prof[1] if prof else "Sem professor"
                st.write(f"**Professor:** {prof_nome}")
                st.write(f"**Alunos:** {total_alunos}")
        else:
            st.warning("Nenhuma turma encontrada com os filtros aplicados.")
    else:
        st.warning("Nenhuma turma cadastrada.")

def modificar():
    st.header("Modificar Turma")
    turmas = consultar_turmas()
    
    if turmas:
        turma_sel = st.selectbox("Selecione:", [f"{t[2]} - {t[1]}" for t in turmas])
        turma = consultar_turma_por_codigo(turma_sel.split(" - ")[0])
        
        if turma:
            st.markdown("### Dados Atuais")
            
            # Obter professor atual e professores disponíveis
            prof = consultar_professor_por_turma(turma[0])
            todos_profs = consultar_professores()
            profs_disponiveis = [p for p in todos_profs if not p[5] or p[5] == turma[0]]
            
            with st.form("form_mod_turma"):
                col1, col2 = st.columns(2)
                with col1:
                    novo_nome = st.text_input("Nome *", value=turma[1])
                    novo_turno = st.selectbox("Turno *", ["Matutino", "Vespertino", "Noturno"], 
                                            index=["Matutino", "Vespertino", "Noturno"].index(turma[3]))
                with col2:
                    st.text_input("Código", value=turma[2], disabled=True)
                    novo_ano = st.number_input("Ano *", min_value=2020, max_value=2030, value=int(turma[4]), step=1)
                
                # Dropdown de professor dentro do formulário
                if profs_disponiveis:
                    opts = ["Sem Professor"] + [f"{p[2]} - {p[1]}" for p in profs_disponiveis]
                    prof_atual_idx = 0
                    if prof:
                        prof_atual_idx = next((i for i, p in enumerate(profs_disponiveis) if p[0] == prof[0]), 0) + 1
                    
                    novo_prof = st.selectbox("Professor", opts, index=prof_atual_idx)
                else:
                    st.info("Nenhum professor disponível")
                    novo_prof = "Sem Professor"
                
                st.info("Código não pode ser alterado.")
                
                if st.form_submit_button("Salvar", use_container_width=True):
                    if novo_nome:
                        # Atualizar dados da turma
                        sucesso, msg = atualizar_turma(turma[0], novo_nome, novo_turno, novo_ano)
                        if sucesso:
                            # Atualizar professor
                            prof_id = None
                            if novo_prof != "Sem Professor":
                                prof_id = next(p[0] for p in profs_disponiveis if p[2] == novo_prof.split(" - ")[0])
                            sucesso_prof, msg_prof = atribuir_professor_turma(turma[0], prof_id)
                            
                            if sucesso_prof:
                                st.success(f"✅ {msg} | {msg_prof}")
                            else:
                                st.warning(f"✅ {msg} | ⚠️ {msg_prof}")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
                    else:
                        st.error("❌ Preencha os campos obrigatórios!")
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
                st.write(f"**Nome:** {turma[1]}")
                st.write(f"**Código:** {turma[2]}")
            with col2:
                st.write(f"**Turno:** {turma[3]}")
                st.write(f"**Ano:** {turma[4]}")
            
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
