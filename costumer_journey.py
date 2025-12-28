import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

# Cores Oficiais Unicesumar
AZUL_UNI = (0, 98, 155)
CINZA_UNI = (117, 120, 123)

# --- INICIALIZAÇÃO DA MEMÓRIA (Session State) ---
# Isso garante que os dados não sumam entre os passos
if 'passo' not in st.session_state: st.session_state.passo = 0
if 'atividade' not in st.session_state: st.session_state.atividade = ""
if 'nome' not in st.session_state: st.session_state.nome = ""
if 'matricula' not in st.session_state: st.session_state.matricula = ""
if 'relato' not in st.session_state: st.session_state.relato = ""

# --- FUNÇÕES DE NAVEGAÇÃO ---
def proximo_passo(): st.session_state.passo += 1
def passo_anterior(): st.session_state.passo -= 1

# --- CLASSE DO PDF ESTILIZADA ---
class PDF(FPDF):
    def header(self):
        try:
            # Logo aumentada para 50mm de largura
            self.image('logo.png', 10, 8, 50) 
        except:
            pass
        self.set_font("Arial", 'B', 14)
        self.set_text_color(*AZUL_UNI) # Azul Oficial
        self.cell(62) 
        self.cell(0, 10, "RELATÓRIO DE EVIDÊNCIAS", ln=True, align='L')
        self.set_font("Arial", 'I', 9)
        self.cell(62)
        self.set_text_color(*CINZA_UNI) # Cinza Oficial
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

# --- PASSO 0: IDENTIFICAÇÃO (Verticalizada) ---
if st.session_state.passo == 0:
    st.subheader("👤 Dados do Acadêmico")
    st.session_state.atividade = st.text_input("NOME DA ATIVIDADE", value=st.session_state.atividade)
    st.session_state.nome = st.text_input("NOME COMPLETO DO(A) ALUNO(A)", value=st.session_state.nome)
    st.session_state.matricula = st.text_input("MATRÍCULA (RA)", value=st.session_state.matricula)
    
    st.markdown("---")
    st.button("Próximo ➡️", on_click=proximo_passo)

# --- PASSO 1: EVIDÊNCIAS ---
elif st.session_state.passo == 1:
    st.subheader("📷 Registro Fotográfico")
    st.info("O template permite no máximo 8 imagens.")
    
    st.session_state.relato = st.text_area("Descrição da Atividade", value=st.session_state.relato)
    fotos = st.file_uploader("Upload das Fotos (Máx 8)", accept_multiple_files=True, type=['jpg', 'png'], key="fotos_upload")
    
    st.markdown("---")
    col_nav = st.columns(2)
    with col_nav[0]: st.button("⬅️ Voltar", on_click=passo_anterior)
    with col_nav[1]: st.button("Próximo ➡️", on_click=proximo_passo)

# --- PASSO 2: FINALIZAÇÃO ---
elif st.session_state.passo == 2:
    st.subheader("✅ Conclusão")
    termos = st.file_uploader("Anexar fotos dos Termos (Opcional)", accept_multiple_files=True, type=['jpg', 'png'], key="termos_upload")
    
    st.warning("Verifique se os dados estão corretos. Ao clicar, o PDF será gerado instantaneamente.")
    
    st.markdown("---")
    col_nav = st.columns(2)
    with col_nav[0]: st.button("⬅️ Voltar", on_click=passo_anterior)
    
    if st.button("🚀 GERAR PDF PROFISSIONAL"):
        with st.spinner("Otimizando imagens e criando documento..."):
            pdf = PDF()
            pdf.alias_nb_pages()
            pdf.set_auto_page_break(auto=True, margin=20)
            pdf.add_page()
            
            # Helper para evitar erro de Unicode (ç, ã, etc)
            def fix(t): return t.encode('latin-1', 'replace').decode('latin-1')

            # Cabeçalho de Identificação
            pdf.set_fill_color(245, 245, 245)
            pdf.set_font("Arial", 'B', 10)
            pdf.set_text_color(*AZUL_UNI)
            pdf.cell(0, 8, " DADOS DO ACADÊMICO", ln=True, fill=True)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", size=10)
            pdf.ln(2)
            pdf.cell(0, 7, f"ATIVIDADE: {fix(st.session_state.atividade.upper())}", ln=True)
            pdf.cell(0, 7, f"ALUNO: {fix(st.session_state.nome.upper())} | RA: {st.session_state.matricula}", ln=True)
            pdf.ln(5)

            # Descrição (Justificada à Esquerda para evitar espaços grandes)
            if st.session_state.relato:
                pdf.set_font("Arial", 'B', 10)
                pdf.set_text_color(*AZUL_UNI)
                pdf.cell(0, 8, " DESCRIÇÃO DA ATIVIDADE", ln=True, fill=True)
                pdf.ln(2)
                pdf.set_text_color(50, 50, 50)
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 6, fix(st.session_state.relato), align='L')
                pdf.ln(5)

            # Processamento das Fotos (Otimizado)
            if "fotos_upload" in st.session_state and st.session_state.fotos_upload:
                pdf.set_font("Arial", 'B', 10)
                pdf.set_text_color(*AZUL_UNI)
                pdf.cell(0, 8, " EVIDÊNCIAS FOTOGRÁFICAS", ln=True, fill=True)
                pdf.ln(5)
                
                for i, foto in enumerate(st.session_state.fotos_upload[:8]):
                    img = Image.open(foto).convert("RGB")
                    img.thumbnail((700, 700)) # Otimiza o tamanho para o PDF não travar
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG", quality=80) # Qualidade 80 para ser rápido
                    
                    x = 10 if i % 2 == 0 else 105
                    if i % 2 == 0 and i > 0: pdf.ln(70)
                    if pdf.get_y() > 230: pdf.add_page()
                    pdf.image(buf, x=x, y=pdf.get_y(), w=90)
                pdf.ln(75)

            # Termos (Páginas extras)
            if "termos_upload" in st.session_state and st.session_state.termos_upload:
                for termo in st.session_state.termos_upload:
                    pdf.add_page()
                    pdf.set_font("Arial", 'B', 12)
                    pdf.cell(0, 10, "ANEXO: TERMO DE CESSÃO", ln=True, align='C')
                    img_t = Image.open(termo).convert("RGB")
                    img_t.thumbnail((1000, 1000))
                    buf_t = io.BytesIO()
                    img_t.save(buf_t, format="JPEG")
                    pdf.image(buf_t, x=15, w=180)

            pdf_bytes = bytes(pdf.output())
            st.success("✅ Tudo pronto! Seu PDF profissional foi gerado.")
            st.download_button("📥 Baixar Relatório Final", pdf_bytes, f"Relatorio_{st.session_state.matricula}.pdf", "application/pdf")
