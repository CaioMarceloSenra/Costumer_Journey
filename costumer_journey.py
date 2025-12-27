import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

# --- CLASSE CUSTOMIZADA PARA O TEMPLATE OFICIAL ---
class PDF(FPDF):
    def header(self):
        # Tenta carregar a logo. 'logo.png' deve estar no seu GitHub.
        # Parâmetros: caminho do arquivo, x, y, largura (w)
        try:
            self.image('logo.png', 10, 8, 35) 
        except:
            # Caso você ainda não tenha subido a imagem, o código não trava
            pass
            
        self.set_font("Arial", 'B', 12)
        # Move o título para a direita para não sobrepor a logo
        self.cell(40) 
        self.cell(0, 10, "RELATÓRIO DE EVIDÊNCIAS - ATIVIDADE EXTENSIONISTA", ln=True, align='L')
        self.ln(10)

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Gerador Unicesumar Oficial", layout="centered")

st.title("📄 Gerador de Template de Evidências")
st.caption("Siga as orientações: Máximo 8 fotos e 2 páginas de relatório.")

tab1, tab2, tab3 = st.tabs(["👤 Identificação", "📷 Evidências (Máx 8)", "📝 Termos e Finalização"])

with tab1:
    atividade = st.text_input("NOME DA ATIVIDADE EXTENSIONISTA")
    nome = st.text_input("NOME COMPLETO DO(A) ALUNO(A)")
    matricula = st.text_input("MATRÍCULA (RA)")

with tab2:
    st.info("As imagens devem comprovar claramente a realização da atividade.")
    # Limite de 8 imagens conforme instrução [cite: 5]
    fotos = st.file_uploader("Selecione até 8 fotos (JPG/PNG)", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])
    if len(fotos) > 8:
        st.warning("Atenção: O sistema aceitará apenas as 8 primeiras imagens.")
    
    relato = st.text_area("Breve descrição da atividade (Opcional)")

with tab3:
    st.write("Se outras pessoas aparecerem, anexe o Termo de Cessão de Uso de Imagem abaixo.")
    termos = st.file_uploader("Anexar Termos assinados (PDF/JPG)", accept_multiple_files=True)

    if st.button("✨ GERAR PDF OFICIAL"):
        if not atividade or not nome or not matricula:
            st.error("Preencha os campos de identificação obrigatórios.")
        else:
            pdf = PDF()
            pdf.set_auto_page_break(auto=True, margin=20)
            pdf.add_page()
            
            # 1. IDENTIFICAÇÃO (Nomes exatos do template )
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 7, f"NOME DA ATIVIDADE EXTENSIONISTA: {atividade.upper()}", ln=True)
            pdf.cell(0, 7, f"NOME COMPLETO DO(A) ALUNO(A): {nome.upper()}", ln=True)
            pdf.cell(0, 7, f"MATRÍCULA: {matricula}", ln=True)
            pdf.ln(5)

            # 2. RELATO 
            if relato:
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(0, 7, "DESCRIÇÃO DA ATIVIDADE:", ln=True)
                pdf.set_font("Arial", size=10)
                # Alinhamento 'L' corrige o erro de espaçamento do seu print
                pdf.multi_cell(0, 6, relato, align='L') 
                pdf.ln(5)

            # 3. GRID DE IMAGENS (Limite de 8 [cite: 5])
            if fotos:
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(0, 7, "EVIDÊNCIAS DA ATIVIDADE:", ln=True)
                
                col_w = 90
                spacing = 5
                # Pega apenas as 8 primeiras fotos
                for i, foto in enumerate(fotos[:8]):
                    img = Image.open(foto).convert("RGB")
                    img.thumbnail((800, 800))
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG")
                    
                    # Lógica de 2 fotos por linha (estilo tabela [cite: 19])
                    x = 10 if i % 2 == 0 else 10 + col_w + spacing
                    if i % 2 == 0 and i > 0: pdf.ln(65)
                    
                    # Se for estourar a página, pula (mantendo limite de 2 páginas [cite: 8])
                    if pdf.get_y() > 230:
                        pdf.add_page()
                    
                    pdf.image(buf, x=x, y=pdf.get_y(), w=col_w)
                
                pdf.ln(70)

            # 4. ANEXO DE TERMOS [cite: 21]
            if termos:
                pdf.add_page()
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, "ANEXOS: TERMOS DE CESSÃO DE IMAGEM", ln=True, align='C')
                for termo in termos:
                    # Lógica simples para anexar imagens de termos
                    try:
                        t_img = Image.open(termo).convert("RGB")
                        t_img.thumbnail((1000, 1000))
                        t_buf = io.BytesIO()
                        t_img.save(t_buf, format="JPEG")
                        pdf.image(t_buf, x=10, w=190)
                        pdf.add_page()
                    except:
                        pass # Ignora se for PDF (precisaria de lógica extra para fundir PDFs)

            pdf_bytes = bytes(pdf.output())
            st.success("Documento pronto para o Ambiente Virtual!")
            st.download_button("📥 Baixar Relatório PDF", pdf_bytes, f"Evidencias_{matricula}.pdf", "application/pdf")
