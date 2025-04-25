import streamlit as st
import fitz
from groq import Groq


GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)


def extract_text_from_pdfs(uploaded_pdfs):
    text = ""
    for pdf in uploaded_pdfs:
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text("text")
    return text


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
    st.image("logo.png", width=200, caption="logo.png")

    with st.sidebar:
        st.header("Upload de arquivos PDF")
        uploaded_pdfs = st.file_uploader("Adicione arquivos PDF", type="pdf", accept_multiple_files=True)

    if uploaded_pdfs:
        text = extract_text_from_pdfs(uploaded_pdfs)
        st.session_state["document_text"] = text

    if "document_text" in st.session_state:
        user_input = st.text_input("Digite sua pergunta:")
        if user_input:
            response = chat_with_groq(user_input, st.session_state["document_text"])
            st.write("Resposta do Assistente:")
            st.write(response)

if __name__ == "__main__":
    main()