import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

# Cores Oficiais Unicesumar
AZUL_UNI = (0, 98, 155)
CINZA_UNI = (117, 120, 123)

class PDF(FPDF):
    def header(self):
        # Logo aumentada para 50mm de largura
        try:
            self.image('logo.png', 10, 8, 50) 
        except:
            pass
        
        self.set_font("Arial", 'B', 14)
        self.set_text_color(*AZUL_UNI)
        
        # Aumentamos o recuo de 45 para 62 para acomodar a logo maior
        self.cell(62) 
        self.cell(0, 10, "RELATÓRIO DE EVIDÊNCIAS", ln=True, align='L')
        
        self.set_font("Arial", 'I', 9)
        self.cell(62)
        self.cell(0, 5, "Projeto de Atividade Extensionista", ln=True, align='L')
        
        # Ajustamos a linha divisória para começar um pouco mais abaixo
        self.set_draw_color(*AZUL_UNI)
        self.line(10, 35, 200, 35)
        self.ln(18)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Página {self.page_no()} de {{nb}}", align='C')

st.set_page_config(page_title="Gerador Unicesumar Oficial", layout="centered")

st.title("🎓 Gerador de Template de Evidências")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["👤 Identificação", "📷 Evidências", "✨ Finalização"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        atividade = st.text_input("NOME DA ATIVIDADE")
        matricula = st.text_input("MATRÍCULA (RA)")
    with col2:
        nome = st.text_input("NOME DO(A) ALUNO(A)")

with tab2:
    st.info("Limite de 8 imagens conforme instrução do template[cite: 5].")
    fotos = st.file_uploader("Upload das Fotos", accept_multiple_files=True, type=['jpg', 'png'])
    relato = st.text_area("Descrição da Atividade")

with tab3:
    termos = st.file_uploader("Anexar Termos (Opcional)", accept_multiple_files=True)

    if st.button("🚀 GERAR PDF PROFISSIONAL"):
        if not atividade or not nome or not matricula:
            st.error("Preencha os dados de identificação.")
        else:
            pdf = PDF()
            pdf.alias_nb_pages()
            pdf.set_auto_page_break(auto=True, margin=20)
            pdf.add_page()
            
            # Seção de Identificação com Fundo Cinza Claro
            pdf.set_fill_color(245, 245, 245)
            pdf.set_font("Arial", 'B', 10)
            pdf.set_text_color(*AZUL_UNI)
            pdf.cell(0, 8, " DADOS DO ACADÊMICO", ln=True, fill=True)
            
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", size=10)
            pdf.ln(2)
            # Correção de caracteres especiais para evitar erro Unicode
            def fix_txt(t): return t.encode('latin-1', 'replace').decode('latin-1')
            
            pdf.cell(0, 7, f"ATIVIDADE: {fix_txt(atividade.upper())}", ln=True)
            pdf.cell(0, 7, f"ALUNO: {fix_txt(nome.upper())}  |  RA: {matricula}", ln=True)
            pdf.ln(5)

            # Descrição
            if relato:
                pdf.set_font("Arial", 'B', 10)
                pdf.set_text_color(*AZUL_UNI)
                pdf.cell(0, 8, " DESCRIÇÃO DA ATIVIDADE", ln=True, fill=True)
                pdf.ln(2)
                pdf.set_text_color(50, 50, 50)
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 6, fix_txt(relato), align='L')
                pdf.ln(5)

            # Grid de Imagens (2 por linha [cite: 19, 22])
            if fotos:
                pdf.set_font("Arial", 'B', 10)
                pdf.set_text_color(*AZUL_UNI)
                pdf.cell(0, 8, " EVIDÊNCIAS FOTOGRÁFICAS", ln=True, fill=True)
                pdf.ln(5)
                
                col_w = 90
                for i, foto in enumerate(fotos[:8]):
                    img = Image.open(foto).convert("RGB")
                    img.thumbnail((800, 800))
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG")
                    
                    # Lógica de posicionamento X e Y
                    x = 10 if i % 2 == 0 else 105
                    if i % 2 == 0 and i > 0: pdf.ln(70)
                    
                    if pdf.get_y() > 230:
                        pdf.add_page()
                    
                    pdf.image(buf, x=x, y=pdf.get_y(), w=col_w)
                
            # Gerar PDF em Bytes
            pdf_bytes = bytes(pdf.output())
            st.success("PDF Estilizado Gerado com Sucesso!")
            st.download_button("📥 Baixar Relatório", pdf_bytes, f"Relatorio_{matricula}.pdf", "application/pdf")

