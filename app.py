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

# Lista de modelos válidos vigentes em ordem de preferência
MODELOS_DISPONIVEIS = [
    'gemini-3.8-flash',
    'gemini-3-flash',
    'gemini-2.5-flash'
]

def gerar_resposta_com_fallback(prompt):
    """
    Tenta gerar conteúdo testando a lista de modelos válidos.
    Caso encontre instabilidade de servidor (503), faz uma breve pausa e tenta novamente.
    """
    erros = []
    
    for modelo in MODELOS_DISPONIVEIS:
        # Tenta até 2 vezes cada modelo caso haja pico temporário de demanda (503)
        for tentativa in range(2):
            try:
                response = client.models.generate_content(
                    model=modelo,
                    contents=prompt,
                )
                return response.text
            except Exception as e:
                erro_msg = str(e)
                erros.append(f"{modelo} (tentativa {tentativa+1}): {erro_msg}")
                
                # Se for erro de indisponibilidade temporária (503), espera 2 segundos antes de tentar de novo
                if "503" in erro_msg or "UNAVAILABLE" in erro_msg:
                    time.sleep(2)
                    continue
                else:
                    # Se for outro erro (ex: 404), vai direto para o próximo modelo da lista
                    break
    
    raise Exception("Servidores indisponíveis no momento. Detalhes: " + " | ".join(erros))


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
            with st.spinner("Conectando ao Gemini e processando a declaração..."):
                try:
                    prompt = f"""
                    Atue como um escrivão de polícia experiente. 
                    Transforme a narrativa do Boletim de Ocorrência abaixo em uma declaração 
                    formal da vítima em terceira pessoa, narrando o fato e iniciando cada sentença 
                    com o pronome relativo "QUE".
                    
                    Texto do B.O.:
                    {texto_bo}
                    """
                    
                    resultado = gerar_resposta_com_fallback(prompt)
                    
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
            with st.spinner("Conectando ao Gemini e analisando o caso..."):
                try:
                    prompt = f"""
                    Atue como um Delegado de Polícia experiente. 
                    Analise o procedimento policial abaixo, aponte os pontos-chave (contradições, 
                    provas materiais e fragilidades) e crie uma lista estratégica de perguntas 
                    para o interrogatório do investigado.
                    
                    Procedimento:
                    {texto_proc}
                    """
                    
                    resultado = gerar_resposta_com_fallback(prompt)
                    
                    st.success("Análise concluída!")
                    st.text_area("Pontos-Chave e Perguntas:", value=resultado, height=300)
                except Exception as e:
                    st.error(f"Erro ao processar: {e}")
