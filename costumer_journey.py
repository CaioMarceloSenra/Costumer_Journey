import streamlit as st
from fpdf import FPDF

st.title("Teste do Sistema - Unicesumar")

nome = st.text_input("Digite seu nome para o teste:")

if st.button("Gerar PDF de Teste"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Teste de Geracao de PDF", ln=1, align='C')
    pdf.cell(200, 10, txt=f"Aluno: {nome}", ln=2, align='L')
    
    # Gerar o PDF em bytes para o Streamlit
    pdf_output = pdf.output(dest='S')
    
    st.success("PDF gerado com sucesso!")
    st.download_button(label="Baixar Teste", data=pdf_output, file_name="teste.pdf")