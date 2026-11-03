import streamlit as st
from google import genai

# Configuração da página do aplicativo
st.set_page_config(page_title="Assistente de Polícia Civil - IA", page_icon="👮‍♂️", layout="wide")

# Título do App
st.title("👮‍♂️ Assistente Inteligente para Polícia Civil")
st.markdown("Automatize a redação de declarações e prepare-se estrategicamente para interrogatórios.")

# Inicializa o cliente do Gemini
# (Certifique-se de ter configurado sua variável de ambiente GEMINI_API_KEY)
client = genai.Client()

# Abas na tela para separar as duas funções que você faz
aba1, aba2 = st.tabs(["📄 Gerar Declaração (B.O.)", "🎯 Análise e Interrogatório"])

# --- ABA 1: GERADOR DE DECLARAÇÃO ---
with aba1:
    st.header("Transformar B.O. em Declaração Formal")
    st.markdown("Cole a narrativa informal do Boletim de Ocorrência abaixo:")
    
    texto_bo = st.text_area("Narrativa do B.O.", height=150, placeholder="Ex: A vítima compareceu relatando que...")
    
    if st.button("Gerar Declaração em 3ª Pessoa (com 'QUE')"):
        if texto_bo.strip() == "":
            st.warning("Por favor, insira o texto do Boletim de Ocorrência.")
        else:
            with st.spinner("O Gemini está redigindo a declaração..."):
                try:
                    prompt = f"""
                    Atue como um escrivão de polícia experiente. 
                    Transforme a narrativa do Boletim de Ocorrência abaixo em uma declaração 
                    formal da vítima em terceira pessoa, narrando o fato e iniciando cada sentença 
                    com o pronome relativo "QUE".
                    
                    Texto do B.O.:
                    {texto_bo}
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=prompt,
                    )
                    
                    st.success("Declaração gerada com sucesso!")
                    st.text_area("Resultado:", value=response.text, height=200)
                except Exception as e:
                    st.error(f"Erro ao processar: {e}")

# --- ABA 2: ANÁLISE E INTERROGATÓRIO ---
with aba2:
    st.header("Análise de Procedimento e Perguntas de Interrogatório")
    st.markdown("Cole o resumo do procedimento ou das peças investigativas:")
    
    texto_proc = st.text_area("Resumo do Procedimento", height=150, placeholder="Ex: Relatório de investigações aponta que...")
    
    if st.button("Analisar e Gerar Perguntas"):
        if texto_proc.strip() == "":
            st.warning("Por favor, insira o texto do procedimento.")
        else:
            with st.spinner("Analisando o caso e cruzando dados..."):
                try:
                    prompt = f"""
                    Atue como um Delegado de Polícia experiente. 
                    Analise o procedimento policial abaixo, aponte os pontos-chave (contradições, 
                    provas materiais e fragilidades) e crie uma lista estratégica de perguntas 
                    para o interrogatório do investigado.
                    
                    Procedimento:
                    {texto_proc}
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=prompt,
                    )
                    
                    st.success("Análise concluída!")
                    st.text_area("Pontos-Chave e Perguntas:", value=response.text, height=300)
                except Exception as e:
                    st.error(f"Erro ao processar: {e}")
