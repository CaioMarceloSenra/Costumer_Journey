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
    # --- 3. EVIDÊNCIAS FOTOGRÁFICAS (A Lógica que você quer está AQUI) ---
if "fotos_upload" in st.session_state and st.session_state.fotos_upload:
    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(*AZUL_UNI)
    pdf.cell(0, 8, " EVIDÊNCIAS FOTOGRÁFICAS", ln=True, fill=True)
    pdf.ln(5)
    
    # Configuração da Moldura Azul Unicesumar
    pdf.set_draw_color(*AZUL_UNI) 
    pdf.set_line_width(0.5)
    
    # Definição das Dimensões da Grade (Grid)
    largura_moldura = 90
    altura_moldura = 65
    espacamento_entre_fotos = 5
    
    # Capturamos a posição Y atual após o texto da descrição
    y_referencia = pdf.get_y()
    
    # Filtramos para as primeiras 8 fotos conforme sua regra
    fotos_para_processar = st.session_state.fotos_upload[:8]
    
    for i, foto in enumerate(fotos_para_processar):
        # 1. Decidimos se vai para a Esquerda ou Direita
        coluna = i % 2 # 0 = Esquerda, 1 = Direita
        
        # 2. Gerenciamento de Páginas e Linhas
        if i > 0 and i % 4 == 0:
            pdf.add_page()
            y_referencia = 40 # Resetamos o Y para o topo da nova página
        elif i > 0 and i % 2 == 0:
            # Se for uma nova linha na mesma página, descemos o Y
            y_referencia += altura_moldura + espacamento_entre_fotos

        x_pos = 10 if coluna == 0 else 105
        
        # 3. Processamento da Imagem (Otimização)
        img = Image.open(foto).convert("RGB")
        img.thumbnail((800, 800))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        
        # 4. Desenho da Imagem e da Moldura Azul
        pdf.image(buf, x=x_pos, y=y_referencia, w=largura_moldura, h=altura_moldura)
        pdf.rect(x_pos, y_referencia, largura_moldura, altura_moldura)

    # Movemos o cursor para baixo de todas as fotos para o próximo bloco
    pdf.set_y(y_referencia + altura_moldura + 10)

# --- PASSO 2: FINALIZAÇÃO 
elif st.session_state.passo == 2:
    st.subheader("✅ Conclusão e Geração")
    termos = st.file_uploader("Anexar fotos dos Termos (Opcional)", accept_multiple_files=True, type=['jpg', 'png'], key="termos_upload")
    
    st.warning("O PDF agora é dinâmico: ele crescerá de acordo com o tamanho do seu texto e quantidade de fotos.")
    
    st.markdown("---")
    col_nav = st.columns(2)
    with col_nav[0]: st.button("⬅️ Voltar", on_click=passo_anterior)
    
    if st.button("🚀 GERAR PDF PROFISSIONAL"):
        with st.spinner("Gerando documento dinâmico..."):
            pdf = PDF()
            pdf.alias_nb_pages()
            pdf.set_auto_page_break(auto=True, margin=25) # Margem de segurança maior
            pdf.add_page()
            
            def fix(t): return t.encode('latin-1', 'replace').decode('latin-1')

            # 1. DADOS DO ALUNO
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

            # 2. DESCRIÇÃO (O PDF vai empurrar tudo para baixo automaticamente)
            if st.session_state.relato:
                pdf.set_font("Arial", 'B', 10)
                pdf.set_text_color(*AZUL_UNI)
                pdf.cell(0, 8, " DESCRIÇÃO DA ATIVIDADE", ln=True, fill=True)
                pdf.ln(2)
                pdf.set_text_color(50, 50, 50)
                pdf.set_font("Arial", size=10)
                # multi_cell gerencia quebras de página automáticas para textos longos
                pdf.multi_cell(0, 6, fix(st.session_state.relato), align='L')
                pdf.ln(10)

          # --- 3. EVIDÊNCIAS FOTOGRÁFICAS (Com Borda e Grade) ---
            if "fotos_upload" in st.session_state and st.session_state.fotos_upload:
                pdf.set_font("Arial", 'B', 10)
                pdf.set_text_color(*AZUL_UNI)
                pdf.cell(0, 8, " EVIDÊNCIAS FOTOGRÁFICAS", ln=True, fill=True)
                pdf.ln(5)
                
                # Configuração da borda
                pdf.set_draw_color(*AZUL_UNI) # Azul Oficial Unicesumar
                pdf.set_line_width(0.5)        # Espessura da borda (fina e elegante)
                
                fotos_grade = st.session_state.fotos_upload[:8]
                
                for i, foto in enumerate(fotos_grade):
                    img = Image.open(foto).convert("RGB")
                    # Forçamos um redimensionamento para manter a proporção na grade
                    img.thumbnail((800, 800))
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG", quality=85)
                    
                    # Lógica de Colunas
                    coluna = i % 2 
                    if i > 0 and i % 4 == 0: 
                        pdf.add_page()
                    elif i > 0 and i % 2 == 0: 
                        pdf.ln(75) 

                    x_pos = 10 if coluna == 0 else 105
                    y_pos = pdf.get_y()
                    largura_moldura = 90
                    altura_moldura = 65 # Altura fixa para manter a simetria da grade
                    
                    # 1. Desenha a Imagem
                    pdf.image(buf, x=x_pos, y=y_pos, w=largura_moldura, h=altura_moldura)
                    
                    # 2. Desenha a Borda Azul por cima
                    # rect(x, y, w, h)
                    pdf.rect(x_pos, y_pos, largura_moldura, altura_moldura)

                pdf.set_y(pdf.get_y() + 80)
            
# --- 4. TERMOS E ANEXOS (Página Inteira) ---
        if "termos_upload" in st.session_state and st.session_state.termos_upload:
            for termo in st.session_state.termos_upload:
                pdf.add_page() # Cada documento ganha sua própria página limpa
                pdf.set_font("Arial", 'B', 12)
                pdf.set_text_color(*AZUL_UNI)
                pdf.cell(0, 10, "ANEXO: DOCUMENTAÇÃO COMPLEMENTAR", ln=True, align='C')
                pdf.ln(5)
                
                img_t = Image.open(termo).convert("RGB")
                img_t.thumbnail((1200, 1600)) 
                buf_t = io.BytesIO()
                img_t.save(buf_t, format="JPEG", quality=90)
                
                pdf.image(buf_t, x=10, w=190)
            # <--- O LOOP TERMINA AQUI

        # --- 5. FINALIZAÇÃO (Deve estar ALINHADO com o 'if', fora do 'for') ---
        pdf_bytes = bytes(pdf.output())
        
        # --- 6. EXIBIÇÃO NO BROWSER ---
        st.success("✅ Relatório gerado com sucesso!")
        st.download_button(
            label="📥 Baixar Relatório Final", 
            data=pdf_bytes, 
            file_name=f"Relatorio_{st.session_state.matricula}.pdf", 
            mime="application/pdf"
        )

    









