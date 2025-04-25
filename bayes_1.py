# Importar as bibliotecas
import streamlit as st
import fitz
from groq import Groq
import os

# Caminho dinâmico da imagem e do PDF padrão
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(CURRENT_DIR, "logo.png")
DEFAULT_PDF_PATH = os.path.join(CURRENT_DIR, "base_de_dados.pdf")

# Configurar chave da Groq
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Função para extrair texto de PDFs
def extract_files(uploader):
    text = ""
    for pdf in uploader:
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text("text")
    return text


def load_default_pdf():
    if os.path.exists(DEFAULT_PDF_PATH):
        with open(DEFAULT_PDF_PATH, "rb") as f:
            text = ""
            with fitz.open(stream=f.read(), filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text("text")
            return text
    return None


def chat_with_groq(prompt, context):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Você é um assistente de biblioteca que responde com base em documentos fornecidos e ajuda os usuários a localizar materiais relevantes."},
            {"role": "user", "content": f"{context}\n\nPergunta: {prompt}"}
        ]
    )
    return response.choices[0].message.content


def main():
    st.title("Assistente Inteligente de Biblioteca")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(LOGO_PATH, width=200)
    with col2:
        st.title("Sistema Inteligente de Biblioteca")

    
    with st.sidebar:
        st.header("Gerenciamento de Arquivos")
        

        uploader = st.file_uploader("Adicione arquivos PDF", type="pdf", accept_multiple_files=True)
        

        if st.button("Carregar base de dados padrão"):
            default_text = load_default_pdf()
            if default_text:
                st.session_state["document-text"] = default_text
                st.success("Base de dados carregada!")
            else:
                st.error("Arquivo 'base_de_dados.pdf' não encontrado na pasta.")

        st.header("Preferências do Usuário")
        user_preferences = st.text_input("Digite suas preferências de leitura (ex.: gênero, autor)")

 
    if "document-text" not in st.session_state:
        default_text = load_default_pdf()
        if default_text:
            st.session_state["document-text"] = default_text

  
    if uploader:
        text = extract_files(uploader)
        st.session_state["document-text"] = text
        st.sidebar.success(f"{len(uploader)} arquivo(s) carregado(s)!")

    
    if "document-text" in st.session_state:
        user_input = st.text_input("Digite sua pergunta:")
        if user_input:
            response = chat_with_groq(user_input, st.session_state["document-text"])
            st.write("Resposta do Assistente:")
            st.write(response)

if __name__ == "__main__":
    main()