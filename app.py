import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import PyPDF2


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="My Chatbot",
    page_icon="🤖",
    initial_sidebar_state="expanded"
)
st.title("ChatBot")
st.header("mini chatbot")


if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


prompt = st.chat_input(
    "ask a question or enter something",
    accept_file=True,
    file_type=["pdf", "png", "jpg", "jpeg", "docx"]
)

if prompt:
    user_text = prompt.text
    extracted_text = ""

    with st.chat_message("user"):
        if user_text:
            st.write(user_text)

        if prompt.files:
            for file in prompt.files:
                if file.type.startswith("image"):
                    st.write("Uploaded image:", file.name)
                    st.image(file)

                elif file.type == "application/pdf":
                    st.write("Uploaded PDF:", file.name)
                    reader = PyPDF2.PdfReader(file)
                    for page in reader.pages:
                        extracted_text += page.extract_text()

    st.session_state.messages.append({"role": "user", "content": user_text or "(sent a file)"})

    if extracted_text:
        final_message = f"Document content:\n{extracted_text}\n\nQuestion: {user_text or 'Summarize this document'}"
    else:
        final_message = user_text

    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": final_message}]
        )
        answer = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)