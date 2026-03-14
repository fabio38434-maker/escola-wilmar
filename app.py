import streamlit as st
import pandas as pd
import hashlib

# --- CONFIGURAÇÃO E IDENTIFICAÇÃO ---
st.set_page_config(page_title="Escola Mun. Wilmar Cava Barros", layout="wide")

# Dados da Unidade (Alimentação facilitada)
escola_info = {
    "nome": "Escola Municipal Wilmar Cava Barros",
    "diretora": "Denise Crespo",
    "pedagoga": "Mara",
    "criador": "Fábio Viana / Servidor Público Estatutário"
}

# --- FUNÇÃO PARA GERAR CORES AUTOMÁTICAS POR PROFESSOR ---
def gerar_cor_por_professor(nome_professor):
    """Gera uma cor de fundo pastel baseada no nome do professor para consistência."""
    if not nome_professor or nome_professor == "---":
        return ""
    # Gera um código único baseado no nome
    hash_nome = hashlib.md5(nome_professor.encode()).hexdigest()
    # Converte o hash em valores RGB pastéis (mais claros para leitura)
    r = int(hash_nome[:2], 16) % 128 + 127
    g = int(hash_nome[2:4], 16) % 128 + 127
    b = int(hash_nome[4:6], 16) % 128 + 127
    return f'background-color: rgb({r}, {g}, {b}); color: black; font-weight: bold;'

def aplicar_estilo_dinamico(val):
    """Extrai o nome do professor e aplica a cor correspondente."""
    if " - " in str(val):
        professor = val.split(" - ")[1]
        return gerar_cor_por_professor(professor)
    return ""

# --- INTERFACE DO USUÁRIO ---
st.title(f"🏫 {escola_info['nome']}")
st.sidebar.markdown(f"""
**Gestão 2026**
* **Diretora:** {escola_info['diretora']}
* **Pedagoga:** {escola_info['pedagoga']}
* **Desenvolvedor:** {escola_info['criador']}
""")

aba_horario, aba_merenda = st.tabs(["📅 Horários Automatizados", "📊 Mapa de Merenda"])

with aba_horario:
    st.subheader("Quadro de Horários - Ensino Fundamental 2")
    
    # Exemplo de Turma 601 (A alimentação pode vir de um CSV ou Excel futuramente)
    # Formato: "DISCIPLINA - PROFESSOR"
    dados_601 = {
        "Horário": ["07h às 08h", "08h às 09h", "09h às 10h", "10h às 11h", "11h às 12h", "12h às 13h"],
        "Segunda": ["HIS - LARA", "CIE - BIANCA", "CIE - BIANCA", "HIS - LARA", "HIS - LARA", "---"],
        "Terça": ["GEO - WESLEY", "GEO - WESLEY", "POR - ADAILMA", "POR - ADAILMA", "GEO - WESLEY", "POR - ADAILMA"],
        "Quarta": ["EF - LUDMILA", "EF - LUDMILA", "PRO INT - NELMA", "PRO COM - ANDREA", "MAT - ANDREA", "MAT - ANDREA"],
        "Quinta": ["MAT - ANDREA", "MAT - ANDREA", "POR - ADAILMA", "POR - ADAILMA", "ING - SIMONE", "EN RE - MARCIA"],
        "Sexta": ["ART - KAREN", "ART - KAREN", "PRO VI - SIMONE", "MAT - ANDREA", "ING - SIMONE", "CIE - BIANCA"]
    }
    
    df = pd.DataFrame(dados_601)
    
    # APLICAÇÃO DA LÓGICA DE CORES AUTOMÁTICAS
    # O sistema varre o DataFrame e pinta as células do mesmo professor com a mesma cor
    df_estilizado = df.style.applymap(aplicar_estilo_dinamico)
    
    st.table(df_estilizado)
    
    st.info("💡 **Automatização:** Note que sempre que 'LARA' ou 'ANDREA' aparecem, a cor é idêntica. Se você alterar o nome do professor no código ou na planilha, a cor mudará automaticamente para todos os horários dele.")

with aba_merenda:
    st.subheader("Controle de Frequência Diária")
    # Campo para entrada de dados conforme seu relatório de WhatsApp
    col1, col2 = st.columns(2)
    with col1:
        total_manhã = st.number_input("Total Manhã (Fund 2 + Pré)", value=217)
    with col2:
        total_tarde = st.number_input("Total Tarde (Fund 1 + Pré)", value=207)
    
    st.metric("Soma Geral de Alunos", total_manhã + total_tarde)
    if st.button("Gerar Mapa para Cozinha"):
        st.success("Dados prontos para o Mapa de Merenda!")
