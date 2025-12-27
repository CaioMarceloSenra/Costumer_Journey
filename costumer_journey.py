import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

# Configuração da página para ficar bem no celular
st.set_page_config(page_title="Gerador Unicesumar", layout="centered")

st.title("🎓 Gerador de Projeto de Extensão")
st.info("Preencha as informações abaixo e gere seu PDF pronto para envio.")

# 1. Criação das Abas (Conforme sua estrutura)
tab1, tab2, tab3, tab4 = st.tabs([
    "📍 Identificação", 
    "📦 Coleta", 
    "🏢 Destino", 
    "📄 Gerar PDF"
])

# --- ABA 1: IDENTIFICAÇÃO ---
with tab1:
    st.header("Identificação do Aluno")
    nome = st.text_input("Nome Completo")
    ra = st.text_input("RA (Registro Acadêmico)")
    projeto = st.text_input("Nome do Projeto de Extensão")

# --- ABA 2: COLETA ---
with tab2:
    st.header("Etapa de Coleta")
    desc_coleta = st.text_area("Descreva como foi a coleta dos artigos")
    fotos_coleta = st.file_uploader("Fotos da Coleta", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])

# --- ABA 3: DESTINO ---
with tab3:
    st.header("Entrega e Instituição")
    unidade = st.text_input("Instituição que recebeu")
    cnpj = st.text_input("CNPJ e Endereço")
    fotos_entrega = st.file_uploader("Fotos da Doação Realizada", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])

# --- ABA 4: GERAR O ARQUIVO ---
with tab4:
    st.header("Finalização")
    st.write("Verifique se todos os campos foram preenchidos antes de clicar.")
    
    if st.button("🚀 CRIAR PROJETO FINAL"):
        if not nome or not ra:
            st.error("Ops! Você esqueceu de colocar o Nome ou o RA na primeira aba.")
        else:
            # Início da criação do PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            
            # Cabeçalho
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, "Relatório de Atividade de Extensão", ln=True, align='C')
            pdf.ln(10)
            
            # Dados do Aluno
            pdf.set_font("Arial", size=12)
            pdf.cell(190, 10, f"Aluno: {nome}", ln=True)
            pdf.cell(190, 10, f"RA: {ra}", ln=True)
            pdf.cell(190, 10, f"Projeto: {projeto}", ln=True)
            pdf.ln(5)
            
            # Conteúdo da Coleta
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(190, 10, "1. Descrição da Coleta", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 10, desc_coleta)
            
            # Fotos da Coleta (Tratamento de Imagem)
            if fotos_coleta:
                for foto in fotos_coleta:
                    img = Image.open(foto).convert("RGB")
                    img.thumbnail((600, 600)) # Redimensiona para não pesar
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format="JPEG")
                    pdf.image(img_buffer, w=90) # Coloca a foto no PDF
            
            # Conteúdo do Destino
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(190, 10, "2. Instituição e Entrega", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.cell(190, 10, f"Destino: {unidade}", ln=True)
            pdf.multi_cell(0, 10, f"Dados da Unidade: {cnpj}")
            
            if fotos_entrega:
                for foto in fotos_entrega:
                    img = Image.open(foto).convert("RGB")
                    img.thumbnail((600, 600))
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format="JPEG")
                    pdf.image(img_buffer, w=90)

            # --- O PULO DO GATO: DOWNLOAD ---
            pdf_bytes = bytes(pdf.output()) # Transforma em bytes para o Streamlit
            
            st.success("✅ PDF Gerado com sucesso!")
            st.download_button(
                label="📥 Clique aqui para Baixar o PDF",
                data=pdf_bytes,
                file_name=f"Projeto_Extensao_{ra}.pdf",
                mime="application/pdf"
            )
