import streamlit as st
from database import init_db, consultar_turmas, consultar_professores, consultar_alunos
from config.styles import get_custom_css
from modules import turmas, professores, alunos

st.set_page_config(page_title="Sistema de Monitoria", page_icon="📚", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)

init_db()

st.title("Sistema de Monitoria")

menu = st.sidebar.selectbox("Menu Principal", ["Início", "Turmas", "Professores", "Alunos"])

if menu == "Início":
    st.header("Bem-vindo!")
    st.write("**Funcionalidades:** Gerenciar Turmas, Professores e Alunos")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Turmas", len(consultar_turmas()))
    with col2:
        st.metric("Professores", len(consultar_professores()))
    with col3:
        st.metric("Alunos", len(consultar_alunos()))

elif menu in ["Turmas", "Professores", "Alunos"]:
    submenu = st.sidebar.radio("Opções", ["Cadastrar", "Consultar", "Modificar", "Excluir"])
    
    if menu == "Turmas":
        turmas.render(submenu)
    elif menu == "Professores":
        professores.render(submenu)
    elif menu == "Alunos":
        alunos.render(submenu)

st.markdown("---")
st.markdown("Sistema de Monitoria © 2025")
