import streamlit as st
from google import genai
import pypdf  # Biblioteca para ler arquivos PDF

# Configuração da página do aplicativo
st.set_page_config(page_title="Assistente de Polícia Civil - IA", page_icon="👮‍♂️", layout="wide")

# Título do App
st.title("👮‍♂️ Assistente Inteligente para Polícia Civil")
st.markdown("Automatize a redação de declarações, análises de procedimentos e gere textos prontos para uso.")

# Inicializa o cliente do Gemini puxando a chave secreta configurada no Streamlit
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def extrair_texto_pdf(arquivo_pdf):
    """Extrai todo o texto de um arquivo PDF enviado pelo usuário."""
    leitor = pypdf.PdfReader(arquivo_pdf)
    texto = ""
    for pagina in leitor.pages:
        texto += pagina.extract_text() or ""
    return texto

# Abas na tela para separar as duas funções
aba1, aba2 = st.tabs(["📄 Gerar Declaração (B.O.)", "🎯 Análise e Interrogatório"])

# --- ABA 1: GERADOR DE DECLARAÇÃO ---
with aba1:
    st.header("Transformar B.O. em Declaração Formal")
    st.markdown("Envie um arquivo PDF do B.O. ou cole o texto na caixa abaixo:")
    
    # Campo para upload de PDF
    arquivo_enviado = st.file_uploader("Anexar Boletim de Ocorrência (PDF)", type=["pdf"], key="pdf_bo")
    
    texto_bo = ""
    if arquivo_enviado is not None:
        texto_bo = extrair_texto_pdf(arquivo_enviado)
        st.success("PDF carregado e lido com sucesso!")
        with st.expander("Ver texto extraído do PDF"):
            st.write(texto_bo[:1000] + "..." if len(texto_bo) > 1000 else texto_bo)
    
    # Caixa de texto caso prefira colar manualmente
    texto_manual = st.text_area("Ou cole a narrativa informal do B.O. aqui:", height=120, placeholder="Ex: A vítima compareceu relatando que...")
    
    # Define qual texto usar (prioriza o PDF se houver, senão usa o texto digitado)
    texto_final_entrada = texto_bo if texto_bo.strip() != "" else texto_manual
    
    if st.button("Gerar Declaração em 3ª Pessoa (com 'QUE')", key="btn_declaração"):
        if texto_final_entrada.strip() == "":
            st.warning("Por favor, envie um arquivo PDF ou insira o texto do Boletim de Ocorrência.")
        else:
            with st.spinner("O Gemini está redigindo a declaração..."):
                try:
                    prompt = f"""
                    Atue como um escrivão de polícia experiente. 
                    Transforme a narrativa do Boletim de Ocorrência abaixo em uma declaração 
                    formal da vítima em terceira pessoa, narrando o fato e iniciando cada sentença 
                    com o pronome relativo "QUE".
                    
                    Texto do B.O.:
                    {texto_final_entrada}
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=prompt,
                    )
                    
                    st.success("Declaração gerada com sucesso!")
                    
                    # Exibe o resultado
                    resultado_declaracao = response.text
                    st.text_area("Resultado:", value=resultado_declaracao, height=200, key="res_decl")
                    
                    # Instrução amigável para cópia (o Streamlit possui botão nativo de copiar no canto superior direito da caixa de texto acima)
                    st.info("💡 **Dica:** Você pode clicar no ícone de cópia localizado no canto superior direito da caixa de texto acima para copiar o resultado instantaneamente.")
                    
                except Exception as e:
                    st.error(f"Erro ao processar: {e}")

# --- ABA 2: ANÁLISE E INTERROGATÓRIO ---
with aba2:
    st.header("Análise de Procedimento e Perguntas de Interrogatório")
    st.markdown("Envie o PDF do relatório/procedimento ou cole o resumo abaixo:")
    
    # Campo para upload de PDF na aba 2
    arquivo_proc_enviado = st.file_uploader("Anexar Procedimento/Relatório (PDF)", type=["pdf"], key="pdf_proc")
    
    texto_proc_pdf = ""
    if arquivo_proc_enviado is not None:
        texto_proc_pdf = extrair_texto_pdf(arquivo_proc_enviado)
        st.success("PDF do procedimento carregado com sucesso!")
        with st.expander("Ver texto extraído do procedimento"):
            st.write(texto_proc_pdf[:1000] + "..." if len(texto_proc_pdf) > 1000 else texto_proc_pdf)
            
    texto_proc_manual = st.text_area("Ou cole o resumo do procedimento aqui:", height=120, placeholder="Ex: Relatório de investigações aponta que...")
    
    texto_proc_final = texto_proc_pdf if texto_proc_pdf.strip() != "" else texto_proc_manual
    
    if st.button("Analisar e Gerar Perguntas", key="btn_interrogatorio"):
        if texto_proc_final.strip() == "":
            st.warning("Por favor, envie um PDF ou insira o texto do procedimento.")
        else:
            with st.spinner("Analisando o caso e cruzando dados..."):
                try:
                    prompt = f"""
                    Atue como um Delegado de Polícia experiente. 
                    Analise o procedimento policial abaixo, aponte os pontos-chave (contradições, 
                    provas materiais e fragilidades) e crie uma lista estratégica de perguntas 
                    para o interrogatório do investigado.
                    
                    Procedimento:
                    {texto_proc_final}
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=prompt,
                    )
                    
                    st.success("Análise concluída!")
                    resultado_analise = response.text
                    st.text_area("Pontos-Chave e Perguntas:", value=resultado_analise, height=300, key="res_inter")
                    
                    st.info("💡 **Dica:** Utilize o ícone de copiar no canto superior direito da caixa de texto para transferir as perguntas para a sua área de transferência.")
                    
                except Exception as e:
                    st.error(f"Erro ao processar: {e}")
