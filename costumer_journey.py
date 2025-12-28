import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

# Cores Oficiais Unicesumar
AZUL_UNI = (0, 98, 155)
CINZA_UNI = (117, 120, 123)

# --- INICIALIZAÇÃO DA MEMÓRIA ---
if 'passo' not in st.session_state: st.session_state.passo = 0
if 'atividade' not in st.session_state: st.session_state.atividade = ""
if 'nome' not in st.session_state: st.session_state.nome = ""
if 'matricula' not in st.session_state: st.session_state.matricula = ""
if 'relato' not in st.session_state: st.session_state.relato = ""
if 'fotos_salvas' not in st.session_state: st.session_state.fotos_salvas = []
if 'termos_salvos' not in st.session_state: st.session_state.termos_salvos = []

# --- FUNÇÕES DE NAVEGAÇÃO ---
def proximo_passo(): st.session_state.passo += 1
def passo_anterior(): st.session_state.passo -= 1

# --- CLASSE DO PDF ESTILIZADA ---
class PDF(FPDF):
    def header(self):
        try:
            # Carrega a logo da Unicesumar
            self.image('logo.png', 10, 8, 50) 
        except:
            pass
        self.set_font("Arial", 'B', 14)
        self.set_text_color(*AZUL_UNI)
        self.cell(62) 
        self.cell(0, 10, "RELATÓRIO DE EVIDÊNCIAS", ln=True, align='L')
        self.set_font("Arial", 'I', 9)
        self.cell(62)
        self.set_text_color(*CINZA_UNI)
        self.cell(0, 5, "Projeto de Atividade Extensionista", ln=True, align='L')
        self.set_draw_color(*AZUL_UNI)
        self.line(10, 35, 200, 35)
        self.ln(18)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Página {self.page_no()} de {{nb}}", align='C')

st.set_page_config(page_title="Gerador Unicesumar Oficial", layout="centered")

# --- INTERFACE ---
st.title("🎓 Gerador de Template de Evidências")
passos = ["📍 Identificação", "📷 Evidências", "✨ Finalização"]
st.progress((st.session_state.passo + 1) / len(passos))
st.write(f"**Etapa:** {passos[st.session_state.passo]}")
st.markdown("---")

# --- PASSO 0: IDENTIFICAÇÃO ---
if st.session_state.passo == 0:
    st.subheader("👤 Dados do Acadêmico")
    st.session_state.atividade = st.text_input("NOME DA ATIVIDADE", value=st.session_state.atividade)
    st.session_state.nome = st.text_input("NOME COMPLETO DO(A) ALUNO(A)", value=st.session_state.nome)
    st.session_state.matricula = st.text_input("MATRÍCULA (RA)", value=st.session_state.matricula)
    st.button("Próximo ➡️", on_click=proximo_passo)

# --- PASSO 1: EVIDÊNCIAS ---
elif st.session_state.passo == 1:
    st.subheader("📷 Registro Fotográfico")
    st.session_state.relato = st.text_area("Descrição da Atividade", value=st.session_state.relato, height=200)
    
    fotos = st.file_uploader("Upload das Fotos (Máx 8)", accept_multiple_files=True, type=['jpg', 'png'], key="fotos_temp")
    if fotos:
        st.session_state.fotos_salvas = fotos

    if st.session_state.fotos_salvas:
        st.success(f"✅ {len(st.session_state.fotos_salvas)} foto(s) carregada(s)!")
    
    col_nav = st.columns(2)
    with col_nav[0]: st.button("⬅️ Voltar", on_click=passo_anterior)
    with col_nav[1]: st.button("Próximo ➡️", on_click=proximo_passo)

# --- PASSO 2: FINALIZAÇÃO ---
elif st.session_state.passo == 2:
    st.subheader("✅ Conclusão e Geração")
    
    # 1. Uploader de Termos com Verificação de Segurança
    termos = st.file_uploader("Anexar fotos dos Termos (Opcional)", accept_multiple_files=True, type=['jpg', 'png'], key="termos_temp")
    
    if termos:
        st.session_state.termos_salvos = termos

    # Verificação segura: só exibe sucesso se a lista não estiver vazia
    if "termos_salvos" in st.session_state and st.session_state.termos_salvos:
        st.success(f"✅ {len(st.session_state.termos_salvos)} termo(s) carregado(s)!")
    
    st.warning("Verifique se todos os dados estão corretos antes de gerar o PDF.")
    
    col_nav = st.columns(2)
    with col_nav[0]: st.button("⬅️ Voltar", on_click=passo_anterior)
    
    # 2. O Processo de Geração
    if st.button("🚀 GERAR RELATÓRIO"):
        with st.spinner("Construindo seu relatório..."):
            try:
                pdf = PDF()
                pdf.alias_nb_pages()
                pdf.set_auto_page_break(auto=True, margin=25)
                pdf.add_page()
                
                # Função interna para tratar caracteres especiais (acentos)
                def fix(t): return str(t).encode('latin-1', 'replace').decode('latin-1')

                # --- PARTE 1: DADOS DO ACADÊMICO ---
                pdf.set_fill_color(245, 245, 245)
                pdf.set_font("Arial", 'B', 10)
                pdf.set_text_color(*AZUL_UNI)
                pdf.cell(0, 8, fix(" DADOS DO ACADÊMICO"), ln=True, fill=True)
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("Arial", size=10)
                pdf.ln(2)
                pdf.cell(0, 7, fix(f"ATIVIDADE: {st.session_state.atividade.upper()}"), ln=True)
                pdf.cell(0, 7, fix(f"ALUNO: {st.session_state.nome.upper()} | RA: {st.session_state.matricula}"), ln=True)
                pdf.ln(5)

                # --- PARTE 2: DESCRIÇÃO ---
                if st.session_state.relato:
                    pdf.set_font("Arial", 'B', 10)
                    pdf.set_text_color(*AZUL_UNI)
                    pdf.cell(0, 8, fix(" DESCRIÇÃO DA ATIVIDADE"), ln=True, fill=True)
                    pdf.ln(2)
                    pdf.set_text_color(50, 50, 50)
                    pdf.set_font("Arial", size=10)
                    pdf.multi_cell(0, 6, fix(st.session_state.relato), align='L')
                    pdf.ln(10)

                # --- PARTE 3: EVIDÊNCIAS (Fotos Salvas) ---
                if "fotos_salvas" in st.session_state and st.session_state.fotos_salvas:
                    pdf.set_font("Arial", 'B', 10)
                    pdf.set_text_color(*AZUL_UNI)
                    pdf.cell(0, 8, fix(" EVIDÊNCIAS FOTOGRÁFICAS"), ln=True, fill=True)
                    pdf.ln(5)
                    pdf.set_draw_color(*AZUL_UNI)
                    
                    for i, foto in enumerate(st.session_state.fotos_salvas[:8]):
                        img = Image.open(foto).convert("RGB")
                        img.thumbnail((800, 800))
                        buf = io.BytesIO()
                        img.save(buf, format="JPEG", quality=85)
                        
                        col = i % 2
                        if i > 0 and i % 2 == 0: pdf.ln(70)
                        
                        x_pos = 10 if col == 0 else 105
                        y_pos = pdf.get_y()
                        
                        if y_pos > 220:
                            pdf.add_page()
                            y_pos = pdf.get_y()

                        pdf.image(buf, x=x_pos, y=y_pos, w=90, h=65)
                        pdf.rect(x_pos, y_pos, 90, 65)
                    
                    pdf.set_y(pdf.get_y() + 75)

                # --- PARTE 4: ANEXOS (Termos Salvos) ---
                if "termos_salvos" in st.session_state and st.session_state.termos_salvos:
                    for termo in st.session_state.termos_salvos:
                        pdf.add_page()
                        pdf.set_font("Arial", 'B', 12)
                        pdf.set_text_color(*AZUL_UNI)
                        pdf.cell(0, 10, fix("ANEXO: DOCUMENTAÇÃO COMPLEMENTAR"), ln=True, align='C')
                        pdf.ln(5)
                        
                        img_t = Image.open(termo).convert("RGB")
                        img_t.thumbnail((1200, 1600))
                        buf_t = io.BytesIO()
                        img_t.save(buf_t, format="JPEG", quality=90)
                        pdf.image(buf_t, x=10, w=190)

                # --- FINALIZAÇÃO E DOWNLOAD ---
                pdf_output = pdf.output(dest='S')
                pdf_bytes = pdf_output.encode('latin-1') if isinstance(pdf_output, str) else bytes(pdf_output)

                st.success("✅ Relatório gerado!")
                st.download_button(
                    label="📥 Baixar Relatório Final",
                    data=pdf_bytes,
                    file_name=f"Relatorio_{st.session_state.matricula}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")



