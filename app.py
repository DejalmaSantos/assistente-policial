import time
import streamlit as st
from google import genai

# Configuração da página do aplicativo
st.set_page_config(page_title="Assistente de Polícia Civil - IA", page_icon="👮‍♂️", layout="wide")

# Título do App
st.title("👮‍♂️ Assistente Inteligente para Polícia Civil")
st.markdown("Automatize a redação de declarações e prepare-se estrategicamente para interrogatórios.")

# Inicializa o cliente do Gemini puxando a chave secreta configurada no Streamlit
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def gerar_resposta_estavel(prompt):
    """
    Usa o alias 'gemini-flash-latest' com tentativas automáticas 
    caso ocorra instabilidade temporária (503).
    """
    erros = []
    # Tenta até 3 vezes com pequenas pausas caso o servidor esteja congestionado
    for tentativa in range(3):
        try:
            response = client.models.generate_content(
                model='gemini-flash-latest',
                contents=prompt,
            )
            return response.text
        except Exception as e:
            erro_msg = str(e)
            erros.append(f"Tentativa {tentativa+1}: {erro_msg}")
            
            # Se for instabilidade temporária (503), espera 3 segundos e tenta de novo
            if "503" in erro_msg or "UNAVAILABLE" in erro_msg:
                time.sleep(3)
                continue
            else:
                # Para qualquer outro erro, para e levanta o erro
                break
                
    raise Exception("Não foi possível obter resposta no momento. Detalhes: " + " | ".join(erros))

# Abas na tela para separar as duas funções
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
            with st.spinner("Processando com Gemini..."):
                try:
                    prompt = f"""
                    Atue como um escrivão de polícia experiente. 
                    Transforme a narrativa do Boletim de Ocorrência abaixo em uma declaração 
                    formal da vítima em terceira pessoa, narrando o fato e iniciando cada sentença 
                    com o pronome relativo "QUE".
                    
                    Texto do B.O.:
                    {texto_bo}
                    """
                    
                    resultado = gerar_resposta_estavel(prompt)
                    
                    st.success("Declaração gerada com sucesso!")
                    st.text_area("Resultado:", value=resultado, height=200)
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
            with st.spinner("Analisando o caso..."):
                try:
                    prompt = f"""
                    Atue como um Delegado de Polícia experiente. 
                    Analise o procedimento policial abaixo, aponte os pontos-chave (contradições, 
                    provas materiais e fragilidades) e crie uma lista estratégica de perguntas 
                    para o interrogatório do investigado.
                    
                    Procedimento:
                    {texto_proc}
                    """
                    
                    resultado = gerar_resposta_estavel(prompt)
                    
                    st.success("Análise concluída!")
                    st.text_area("Pontos-Chave e Perguntas:", value=resultado, height=300)
                except Exception as e:
                    st.error(f"Erro ao processar: {e}")
