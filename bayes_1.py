# Importar as bibliotecas
import streamlit as st
import fitz
from groq import Groq
import os

# Caminho dinâmico da imagem
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(CURRENT_DIR, "logo.png")

# Configurar chave da Groq
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Função para extrair texto dos PDFs
def extract_files(uploader):
    text = ""
    for pdf in uploader:
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text("text")
    return text

# Motor de inferência para o sistema inteligente
def chat_with_groq(prompt, context):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Você é um assistente de biblioteca que responde com base em documentos fornecidos e ajuda os usuários a localizar materiais relevantes."},
            {"role": "user", "content": f"{context}\n\nPergunta: {prompt}"}
        ]
    )
    return response.choices[0].message.content

# Criar a interface
def main():
    st.title("Assistente Inteligente de Biblioteca")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(LOGO_PATH, width=200)
    with col2:
        st.title("Sistema Inteligente de Biblioteca")

    # Sidebar para upload de arquivos e preferências do usuário
    with st.sidebar:
        st.header("Uploader de Arquivos")
        uploader = st.file_uploader("Adicione arquivos PDF", type="pdf", accept_multiple_files=True)
        st.header("Preferências do Usuário")
        user_preferences = st.text_input("Digite suas preferências de leitura (ex.: gênero, autor)")

    # Processar arquivos e preferências
    if uploader:
        text = extract_files(uploader)
        st.session_state["document-text"] = text

    if "document-text" in st.session_state:
        user_input = st.text_input("Digite sua pergunta:")
        if user_input:
            response = chat_with_groq(user_input, st.session_state["document-text"])
            st.write("Resposta do Assistente:")
            st.write(response)

if __name__ == "__main__":
    main()