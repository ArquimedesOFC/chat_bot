import streamlit as st
import sqlite3
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import HuggingFaceHub
from dotenv import load_dotenv
import time

load_dotenv()

# Conectar ao banco de dados SQLite
conn = sqlite3.connect("chat_history.db")
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_message TEXT,
        ai_response TEXT
    )
""")
conn.commit()

st.set_page_config(page_title="Assistente Virtual 🤖", page_icon="🤖")
st.title("Assistente Virtual")
st.sidebar.header("Escolha seu modelo de IA")

model_class = st.sidebar.selectbox("Selecione o modelo", ["hf_hub", "openai", "ollama"])

def model_hf_hub(model="meta-llama/Meta-Llama-3-8B-Instruct", temperature=0.1):
    return HuggingFaceHub(
        repo_id=model,
        model_kwargs={"temperature": temperature, "return_full_text": False, "max_new_tokens": 512}
    )

def model_openai(model="gpt-4o-mini", temperature=0.1):
    return ChatOpenAI(model=model, temperature=temperature)

def model_ollama(model="phi3", temperature=0.1):
    return ChatOllama(model=model, temperature=temperature)

def model_response(user_query, model_class):
    llm = model_hf_hub() if model_class == "hf_hub" else model_openai() if model_class == "openai" else model_ollama()
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente prestativo e responde perguntas gerais em português."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])

    chain = prompt_template | llm | StrOutputParser()
    return chain.invoke({"chat_history": [], "input": user_query})

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_query = st.text_area("Digite sua mensagem aqui...", height=100)

col1, col2 = st.columns([3, 1])

with col1:
    if st.button("Enviar"):
        if user_query.strip():
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            with st.chat_message("Human", avatar="🧑"):
                st.markdown(f"<div style='color: white;'>{user_query}</div>", unsafe_allow_html=True)
            
            with st.chat_message("AI", avatar="💻"):
                progress_bar = st.progress(0)
                for percent in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(percent + 1)
                
                response = model_response(user_query, model_class)
                st.markdown(f"<div style='color: white;'>{response}</div>", unsafe_allow_html=True)
            
            st.session_state.chat_history.append(AIMessage(content=response))
            
            cursor.execute("INSERT INTO messages (user_message, ai_response) VALUES (?, ?)", (user_query, response))
            conn.commit()

with col2:
    if st.button("Limpar Chat"):
        st.session_state.chat_history = []
        st.rerun()

st.sidebar.subheader("Histórico de Conversas")
if st.sidebar.button("Ver histórico"):
    st.session_state.show_history = True

if "show_history" in st.session_state and st.session_state.show_history:
    cursor.execute("SELECT id, user_message, ai_response FROM messages")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            st.sidebar.write(f"ID: {row[0]}")
            st.sidebar.write(f"Usuário: {row[1]}")
            st.sidebar.write(f"Assistente: {row[2]}")
            st.sidebar.write("---")
    else:
        st.sidebar.write("Nenhum histórico encontrado.")
    
    if st.sidebar.button("Sair do histórico"):
        st.session_state.show_history = False
        st.rerun()
