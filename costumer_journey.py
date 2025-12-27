import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

# --- CLASSE CUSTOMIZADA PARA O PDF ---
class PDF(FPDF):
    def header(self):
        # Moldura da página
        self.rect(5, 5, 200, 287) 
        # Título Profissional
        self.set_font("Helvetica", 'B', 14)
        self.cell(0, 10, "UNICESUMAR - CENTRO UNIVERSITÁRIO CESUMAR", ln=True, align='C')
        self.set_font("Helvetica", 'I', 10)
        self.cell(0, 5, "Relatório de Atividade de Extensão - Projeto de Doação", ln=True, align='C')
        self.ln(10)

    def footer(self):
        # Posição a 1.5 cm do fim
        self.set_y(-15)
        self.set_font("Helvetica", 'I', 8)
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align='C')

# --- CONFIGURAÇÃO STREAMLIT ---
st.set_page_config(page_title="Gerador Unicesumar Pro", layout="centered")

st.title("🎓 Gerador de Projeto (Versão Pro)")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📍 Identificação", "📦 Coleta", "🏢 Destino", "📄 Finalizar"])

with tab1:
    nome = st.text_input("Nome Completo")
    ra = st.text_input("RA")
    projeto = st.text_input("Nome do Projeto")

with tab2:
    desc_coleta = st.text_area("Relato da Coleta (O que foi feito?)")
    fotos_coleta = st.file_uploader("Fotos da Coleta", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])

with tab3:
    unidade = st.text_input("Instituição Recebedora")
    cnpj_end = st.text_input("CNPJ e Endereço da Unidade")
    desc_entrega = st.text_area("Relato da Entrega (Como foi?)")
    fotos_entrega = st.file_uploader("Fotos da Entrega", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])

with tab4:
    if st.button("🚀 GERAR RELATÓRIO PROFISSIONAL"):
        if not nome or not ra:
            st.error("Preencha os dados básicos na primeira aba!")
        else:
            # Inicializa PDF com numeração total de páginas
            pdf = PDF()
            pdf.alias_nb_pages()
            pdf.set_auto_page_break(auto=True, margin=20)
            pdf.add_page()
            
            # 1. BLOCO DE IDENTIFICAÇÃO (Com fundo cinza claro para destaque)
            pdf.set_fill_color(240, 240, 240)
            pdf.set_font("Helvetica", 'B', 12)
            pdf.cell(0, 10, " IDENTIFICAÇÃO DO ACADÊMICO", ln=True, fill=True)
            pdf.set_font("Helvetica", size=11)
            pdf.ln(2)
            pdf.cell(0, 8, f"ALUNO: {nome.upper()}", ln=True)
            pdf.cell(0, 8, f"RA: {ra} | PROJETO: {projeto.upper()}", ln=True)
            pdf.ln(10)

            # 2. SEÇÃO DE COLETA
            pdf.set_font("Helvetica", 'B', 12)
            pdf.cell(0, 10, " 1. RELATÓRIO DA ETAPA DE COLETA", ln=True, border='B')
            pdf.ln(4)
            pdf.set_font("Helvetica", size=11)
            # Alinhamento 'L' (Left) evita que o texto estique como no seu print
            pdf.multi_cell(0, 7, desc_coleta, align='L')
            pdf.ln(5)

            # Grid de Fotos da Coleta (2 por linha)
            if fotos_coleta:
                col_width = 90
                x_start = 10
                for i, foto in enumerate(fotos_coleta):
                    img = Image.open(foto).convert("RGB")
                    img.thumbnail((800, 800))
                    img_buf = io.BytesIO()
                    img.save(img_buf, format="JPEG")
                    
                    # Lógica de posicionamento (Lado a Lado)
                    x = x_start if i % 2 == 0 else x_start + col_width + 10
                    if i % 2 == 0 and i > 0: pdf.ln(70) # Pula linha após cada par
                    
                    curr_y = pdf.get_y()
                    # Verifica se a imagem vai estourar a página
                    if curr_y > 220: 
                        pdf.add_page()
                        curr_y = pdf.get_y()
                    
                    pdf.image(img_buf, x=x, y=curr_y, w=col_width)
                pdf.ln(75) # Espaço após o bloco de fotos

            # 3. SEÇÃO DE DESTINO
            pdf.add_page()
            pdf.set_font("Helvetica", 'B', 12)
            pdf.cell(0, 10, " 2. RELATÓRIO DA INSTITUIÇÃO E ENTREGA", ln=True, border='B')
            pdf.ln(4)
            pdf.set_font("Helvetica", size=11)
            pdf.cell(0, 8, f"INSTITUIÇÃO: {unidade}", ln=True)
            pdf.cell(0, 8, f"DADOS: {cnpj_end}", ln=True)
            pdf.ln(2)
            pdf.multi_cell(0, 7, desc_entrega, align='L')
            pdf.ln(5)

            # Grid de Fotos da Entrega
            if fotos_entrega:
                col_width = 90
                x_start = 10
                for i, foto in enumerate(fotos_entrega):
                    img = Image.open(foto).convert("RGB")
                    img.thumbnail((800, 800))
                    img_buf = io.BytesIO()
                    img.save(img_buf, format="JPEG")
                    
                    x = x_start if i % 2 == 0 else x_start + col_width + 10
                    if i % 2 == 0 and i > 0: pdf.ln(70)
                    
                    curr_y = pdf.get_y()
                    if curr_y > 220:
                        pdf.add_page()
                        curr_y = pdf.get_y()
                        
                    pdf.image(img_buf, x=x, y=curr_y, w=col_width)

            # Gerar download
            pdf_bytes = bytes(pdf.output())
            st.success("Relatório Profissional Gerado!")
            st.download_button("📥 Baixar PDF Formatado", pdf_bytes, f"Relatorio_{ra}.pdf", "application/pdf")
